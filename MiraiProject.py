import streamlit as st
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Monty Hall Paradox", page_icon="🚪")

st.title("🚪 The Monty Hall Paradox")
st.markdown("""
**Data Science Perspective:** intuitive probability vs. conditional probability.
Use this tool to play the game yourself, then simulate it 1,000 times to see the Law of Large Numbers in action.
""")

# --- PART 1: INTERACTIVE GAME ---
st.header("1. Play the Game")

# Initialize Session State variables to track the game
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: Pick Door, 2: Decide Switch/Stay, 3: Result
if 'prize_door' not in st.session_state:
    st.session_state.prize_door = random.randint(1, 3)
if 'user_pick' not in st.session_state:
    st.session_state.user_pick = None
if 'goat_door' not in st.session_state:
    st.session_state.goat_door = None

def reset_game():
    st.session_state.step = 1
    st.session_state.prize_door = random.randint(1, 3)
    st.session_state.user_pick = None
    st.session_state.goat_door = None

# UI for Step 1: Pick a Door
if st.session_state.step == 1:
    st.subheader("Pick a door:")
    cols = st.columns(3)
    for i in range(1, 4):
        if cols[i-1].button(f"Door {i}", use_container_width=True):
            st.session_state.user_pick = i
            # Host logic: Open a door that is NOT the prize and NOT the user pick
            possible_goats = [d for d in [1, 2, 3] if d != st.session_state.prize_door and d != i]
            st.session_state.goat_door = random.choice(possible_goats)
            st.session_state.step = 2
            st.rerun()

# UI for Step 2: Switch or Stay?
elif st.session_state.step == 2:
    st.info(f"You picked **Door {st.session_state.user_pick}**.")
    st.warning(f"⚠️ The Host opens **Door {st.session_state.goat_door}** to reveal a GOAT! 🐐")
    
    st.subheader("Do you want to Switch?")
    
    col1, col2 = st.columns(2)
    
    # STAY Button
    if col1.button("Stay with original pick"):
        if st.session_state.user_pick == st.session_state.prize_door:
            st.session_state.result = "WIN"
        else:
            st.session_state.result = "LOSE"
        st.session_state.final_choice = st.session_state.user_pick
        st.session_state.step = 3
        st.rerun()

    # SWITCH Button
    if col2.button("Switch Door"):
        # Find the remaining door
        new_pick = [d for d in [1, 2, 3] if d != st.session_state.user_pick and d != st.session_state.goat_door][0]
        if new_pick == st.session_state.prize_door:
            st.session_state.result = "WIN"
        else:
            st.session_state.result = "LOSE"
        st.session_state.final_choice = new_pick
        st.session_state.step = 3
        st.rerun()

# UI for Step 3: Result
elif st.session_state.step == 3:
    if st.session_state.result == "WIN":
        st.success(f"🎉 YOU WON! The car was behind Door {st.session_state.prize_door}. (You chose {st.session_state.final_choice})")
    else:
        st.error(f"🐐 You got a Goat. The car was behind Door {st.session_state.prize_door}. (You chose {st.session_state.final_choice})")
    
    if st.button("Play Again"):
        reset_game()
        st.rerun()

st.markdown("---")

# --- PART 2: MONTE CARLO SIMULATION (SEABORN) ---
st.header("2. The Simulation (Monte Carlo)")
st.write("Does switching actually help? Let's simulate N games.")

num_sims = st.slider("Number of games to simulate:", min_value=100, max_value=5000, value=1000)

if st.button("Run Simulation"):
    # Run the math
    results = []
    for _ in range(num_sims):
        prize = random.randint(1, 3)
        initial_pick = random.randint(1, 3)
        
        # Strategy: STAY (Wins if pick == prize)
        results.append({'Strategy': 'Stay', 'Outcome': 1 if initial_pick == prize else 0})
        
        # Strategy: SWITCH (Wins if pick != prize)
        results.append({'Strategy': 'Switch', 'Outcome': 1 if initial_pick != prize else 0})

    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Calculate win rates
    win_rates = df.groupby('Strategy')['Outcome'].mean().reset_index()
    win_rates['Win Rate %'] = win_rates['Outcome'] * 100

    # PLOT WITH SEABORN
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Seaborn Barplot
    sns.barplot(data=win_rates, x='Strategy', y='Win Rate %', palette=['#ff9999', '#66b3ff'], ax=ax)
    
    # Add labels
    for index, row in win_rates.iterrows():
        ax.text(index, row['Win Rate %'] + 1, f"{row['Win Rate %']:.1f}%", color='black', ha="center", fontdict={'weight': 'bold'})

    ax.set_ylim(0, 100)
    ax.axhline(33.3, color='red', linestyle='--', alpha=0.5)
    ax.axhline(66.6, color='blue', linestyle='--', alpha=0.5)
    ax.set_title(f"Win Rate after {num_sims} Games")
    
    # Display in Streamlit
    st.pyplot(fig)
    
    st.write(f"**Conclusion:** Switching gives you a ~{win_rates[win_rates['Strategy']=='Switch']['Win Rate %'].values[0]:.1f}% win rate, while Staying is only ~{win_rates[win_rates['Strategy']=='Stay']['Win Rate %'].values[0]:.1f}%.")