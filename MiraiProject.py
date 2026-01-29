import streamlit as st
import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cognitive Science of Learning",
    page_icon="🧠",
    layout="wide"
)

# --- CUSTOM CSS FOR "ATTRACTIVE DOORS" ---
st.markdown("""
<style>
    .big-text { font-size:18px !important; line-height: 1.6; }
    
    /* Custom style for the Door Buttons */
    .stButton>button { 
        height: 4em; 
        font-size: 24px; 
        font-weight: bold; 
        border-radius: 10px;
        border: 2px solid #eee;
        transition: transform 0.1s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        border-color: #ff4b4b;
    }
    
    /* Host Dialogue Box */
    .host-box {
        background-color: #f0f2f6;
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        font-size: 18px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- TRANSLATIONS ---
translations = {
    "English": {
        "title": "🧠 Cognitive Science of Learning:\nInteractive Probability Visualization",
        "section1_title": "Why 'Explorable Explanations'?",
        "section1_text": """
        This project is inspired by **Explorable Explanations** (pioneered by creators like Nicky Case).
        
        Traditionally, we learn complex mathematical and physical theorems by **memorizing formulas**. 
        However, Explorable Explanations allow you to **play with the system first**, building intuition before diving into the formal learning.
        """,
        "section2_title": "The Experiment: The Monty Hall Paradox",
        "section2_text": """
        As an introduction to this concept, I present a fun, game-like experiment.
        **The Monty Hall Problem** is a famous paradox that appears simple but is deeply counter-intuitive.
        
        **The Rules:**
        1. There are 3 doors. Behind one is a **Supercar** 🏎️; behind the others are **Goats** 🐐.
        2. You pick a door.
        3. The Host (who knows what's behind every door) opens one of the *other* doors to **reveal a Goat**.
        4. The Host asks: **"Do you want to stick with your choice or switch?"**
        
        Most people assume it is a 50/50 chance. However, probabilistically, **switching is the winning strategy!**
        """,
        "table_intro": "See the logic below. Switching wins in 2 out of 3 scenarios:",
        "start_btn": "🚀 Start Experiment",
        "game_tab": "🕹️ Play Game",
        "sim_tab": "📊 Simulation (Proof)",
        "pick_msg": "Pick a door! The Car 🏎️ is hidden behind one.",
        "switch_msg": "The Host opened ALL other doors except one! Do you Switch?",
        "stay": "🛑 Stick",
        "switch": "🔀 Switch",
        "win": "🎉 YOU WON! Found the Car!",
        "lose": "🐐 You got a Goat.",
        "door_select": "Number of Doors (Difficulty):",
        "host_name": "🎩 Host Monty",
        "host_intro": "Welcome to the show! I have hidden a car behind one of these doors...",
        "host_reveal": "Ha! Look! There was a GOAT behind that door! Now... do you trust your gut?",
    },
    "Japanese": {
        "title": "🧠 学習の認知科学：\n対話的な確率の可視化",
        "section1_title": "なぜ「探索可能な説明」なのか？",
        "section1_text": """
        本プロジェクトは、**Explorable Explanations**（Nicky Caseらが提唱）に触発されました。
        
        通常、私たちは数学や物理の複雑な定理を**公式の暗記**によって学ぼうとします。
        しかし、Explorable Explanations（探索可能な説明）では、まずシステムを**触って遊ぶ**ことで直感を構築し、その後に理論を学びます。
        """,
        "section2_title": "実験：モンティ・ホール問題",
        "section2_text": """
        この概念の導入として、ゲーム形式の実験を用意しました。
        **モンティ・ホール問題**は、シンプルでありながら非常に直感に反する有名なパラドックスです。
        
        **ルール：**
        1. 3つのドアがあります。1つは**スーパーカー**🏎️、残りは**ヤギ**🐐です。
        2. あなたはドアを1つ選びます。
        3. 司会者（正解を知っている）は、残りのドアの1つを開けて**必ずヤギを見せます**。
        4. 司会者は尋ねます：**「選んだドアを変えますか？ そのままにしますか？」**
        
        多くの人は確率は50/50だと考えます。しかし確率論的には、**「変更する」ほうが勝てる戦略なのです！**
        """,
        "table_intro": "以下の論理を見てください。「変更」は3回中2回勝ちます。",
        "start_btn": "🚀 実験を開始する",
        "game_tab": "🕹️ ゲームをプレイ",
        "sim_tab": "📊 シミュレーション (証明)",
        "pick_msg": "ドアを選んでください！ 車🏎️が隠されています。",
        "switch_msg": "司会者が「残り1枚」になるまでハズレのドアをすべて開けました！ 変更しますか？",
        "stay": "🛑 そのまま",
        "switch": "🔀 変更する",
        "win": "🎉 大当たり！ 車でした！",
        "lose": "🐐 残念、ヤギでした。",
        "door_select": "ドアの枚数 (難易度)：",
        "host_name": "🎩 モンティ司会者",
        "host_intro": "ショーへようこそ！ このドアのどれかに新車が隠されています...",
        "host_reveal": "ハハ！ 見てください、そこにはヤギがいました！ さあ、あなたは直感を信じますか？",
    }
}

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    lang = st.radio("Language / 言語", ["English", "Japanese"])
    txt = translations[lang]
    
    st.markdown("---")
    
    # DOOR SELECTOR
    num_doors = st.selectbox(
        txt["door_select"], 
        options=[3, 100, 1000], 
        index=0
    )
    
    # Reset logic if doors change
    if 'last_doors' not in st.session_state: st.session_state.last_doors = num_doors
    if st.session_state.last_doors != num_doors:
        st.session_state.step = 1
        st.session_state.last_doors = num_doors
        if st.session_state.page == "game":
            st.rerun()

    if st.button("🏠 Home / Reset"):
        st.session_state.page = "home"
        st.session_state.step = 1
        st.session_state.score = {'wins': 0, 'losses': 0}
        st.rerun()

# --- INITIALIZE STATE ---
if "page" not in st.session_state: st.session_state.page = "home"
if 'step' not in st.session_state: st.session_state.step = 1
if 'score' not in st.session_state: st.session_state.score = {'wins': 0, 'losses': 0}

# ==========================================
# PAGE 1: HOME (UNCHANGED)
# ==========================================
if st.session_state.page == "home":
    st.title(txt["title"])
    st.markdown("---")

    # Section 1: Intro
    st.markdown(f"### {txt['section1_title']}")
    st.markdown(f"<div class='big-text'>{txt['section1_text']}</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # Section 2: The Game Explanation
    st.markdown(f"### {txt['section2_title']}")
    st.markdown(f"<div class='big-text'>{txt['section2_text']}</div>", unsafe_allow_html=True)

    st.write("")

    # Section 3: The Visual Table (Teaser)
    st.info(f"💡 {txt['table_intro']}")
    
    table_data = [
        ["🚗 Car", "🐐 Goat", "🐐 Goat", "✅ WIN (Car)", "❌ LOSE (Goat)"],
        ["🐐 Goat", "🚗 Car", "🐐 Goat", "❌ LOSE (Goat)", "✅ WIN (Car)"],
        ["🐐 Goat", "🐐 Goat", "🚗 Car", "❌ LOSE (Goat)", "✅ WIN (Car)"]
    ]
    df_preview = pd.DataFrame(table_data, columns=["Door 1 (Pick)", "Door 2", "Door 3", "If Switch", "If Stay"])
    st.table(df_preview)

    st.write("")
    st.write("")

    if st.button(txt["start_btn"], use_container_width=True):
        st.session_state.page = "game"
        st.rerun()

# ==========================================
# PAGE 2: GAME (ATTRACTIVE VERSION)
# ==========================================
elif st.session_state.page == "game":
    
    # Setup Variables
    if 'prize' not in st.session_state: st.session_state.prize = random.randint(1, num_doors)
    if 'user_pick' not in st.session_state: st.session_state.user_pick = None
    if 'host_left_closed' not in st.session_state: st.session_state.host_left_closed = None

    def reset_game():
        st.session_state.step = 1
        st.session_state.prize = random.randint(1, num_doors)
        st.session_state.user_pick = None

    # SCOREBOARD
    col_score1, col_score2, col_score3 = st.columns([1,2,1])
    with col_score2:
        st.metric("Your Score / スコア", f"🏆 {st.session_state.score['wins']} Wins", f"{st.session_state.score['wins'] + st.session_state.score['losses']} Played")

    tab1, tab2 = st.tabs([txt["game_tab"], txt["sim_tab"]])

    # --- TAB 1: PLAY ---
    with tab1:
        st.write("") # Spacer
        
        # STEP 1: Pick
        if st.session_state.step == 1:
            # Host Dialogue
            st.markdown(f"<div class='host-box'><b>{txt['host_name']}:</b> {txt['host_intro']}</div>", unsafe_allow_html=True)
            
            # If 3 doors, show BIG GRAPHIC BUTTONS
            if num_doors == 3:
                c1, c2, c3 = st.columns(3)
                for i, col in enumerate([c1, c2, c3], 1):
                    # Use a big emoji for the door
                    if col.button(f"🚪 {i}", use_container_width=True):
                        st.session_state.user_pick = i
                        st.session_state.step = 2
                        st.rerun()
            else:
                # Slider for 100/1000 doors
                st.info(f"Imagine {num_doors} doors lined up...")
                user_input = st.number_input(f"Choose a door (1-{num_doors})", min_value=1, max_value=num_doors, step=1)
                if st.button("Confirm Choice"):
                    st.session_state.user_pick = user_input
                    st.session_state.step = 2
                    st.rerun()
        
        # STEP 2: Switch
        elif st.session_state.step == 2:
            
            # Logic calculation
            if st.session_state.user_pick == st.session_state.prize:
                remaining = [d for d in range(1, num_doors+1) if d != st.session_state.user_pick]
                st.session_state.host_left_closed = random.choice(remaining)
            else:
                st.session_state.host_left_closed = st.session_state.prize
            
            # Host Dialogue
            st.markdown(f"<div class='host-box'><b>{txt['host_name']}:</b> {txt['host_reveal']}</div>", unsafe_allow_html=True)
            
            # Visual Representation of the State
            col_left, col_right = st.columns(2)
            with col_left:
                st.info(f"You picked **Door {st.session_state.user_pick}**")
                # Show Door Emoji
                st.markdown(f"<h1 style='text-align: center;'>🚪 {st.session_state.user_pick}</h1>", unsafe_allow_html=True)
                if st.button(txt["stay"], use_container_width=True):
                    st.session_state.final = st.session_state.user_pick
                    st.session_state.step = 3
                    st.rerun()
            
            with col_right:
                st.success(f"Host left closed **Door {st.session_state.host_left_closed}**")
                # Show Door Emoji
                st.markdown(f"<h1 style='text-align: center;'>🚪 {st.session_state.host_left_closed}</h1>", unsafe_allow_html=True)
                if st.button(txt["switch"], use_container_width=True):
                    st.session_state.final = st.session_state.host_left_closed
                    st.session_state.step = 3
                    st.rerun()

        # STEP 3: Result
        elif st.session_state.step == 3:
            win = (st.session_state.final == st.session_state.prize)
            
            # Host Dialogue (Result)
            if win:
                st.balloons()
                msg = "UNBELIEVABLE! You found the car!"
                st.markdown(f"<div class='host-box' style='border-color: green;'><b>{txt['host_name']}:</b> {msg}</div>", unsafe_allow_html=True)
                st.success(f"{txt['win']} (Door {st.session_state.prize})")
                
                # Update Score (Only once per game)
                if 'counted' not in st.session_state:
                    st.session_state.score['wins'] += 1
                    st.session_state.counted = True
            else:
                msg = "Sorry! It was a Goat."
                st.markdown(f"<div class='host-box' style='border-color: gray;'><b>{txt['host_name']}:</b> {msg}</div>", unsafe_allow_html=True)
                st.error(f"{txt['lose']} (Car was in Door {st.session_state.prize})")
                
                if 'counted' not in st.session_state:
                    st.session_state.score['losses'] += 1
                    st.session_state.counted = True
            
            # Reveal Visualization
            c1, c2, c3 = st.columns(3)
            with c2:
                if win:
                    st.markdown(f"<div style='text-align:center; font-size: 80px;'>🏎️</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align:center; font-size: 80px;'>🐐</div>", unsafe_allow_html=True)

            if st.button("🔄 Play Again", use_container_width=True):
                if 'counted' in st.session_state: del st.session_state.counted
                reset_game()
                st.rerun()

    # --- TAB 2: SIMULATION (Proof) ---
    with tab2:
        st.header(f"{txt['sim_tab']} ({num_doors} Doors)")
        st.write(f"Simulating {num_doors} doors...")
        
        if st.button("🚀 Run Simulation (1000 Games)"):
            sims = 1000
            prizes = [random.randint(1, num_doors) for _ in range(sims)]
            picks = [random.randint(1, num_doors) for _ in range(sims)]
            
            df = pd.DataFrame({'prize': prizes, 'pick': picks})
            stay_wins = (df['prize'] == df['pick']).mean() * 100
            switch_wins = (df['prize'] != df['pick']).mean() * 100
            
            col_a, col_b = st.columns(2)
            col_a.metric("Win Rate (Stay)", f"{stay_wins:.1f}%")
            col_b.metric("Win Rate (Switch)", f"{switch_wins:.1f}%")
            
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.barplot(x=['Stay', 'Switch'], y=[stay_wins, switch_wins], palette=['#ff4b4b', '#00cc00'], ax=ax)
            ax.set_ylim(0, 100)
            ax.set_ylabel("Win Rate (%)")
            for i, v in enumerate([stay_wins, switch_wins]):
                ax.text(i, v+5, f"{v:.1f}%", ha='center', fontweight='bold')
            st.pyplot(fig)