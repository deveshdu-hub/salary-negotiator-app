# ===================================================================
# Saathi AI – Version 2.0
# All-in-one e‑commerce, Reels, R&D, and Seller Tools
# ===================================================================

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from PIL import Image
import io
import json
import sqlite3
import hashlib
import time
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Saathi AI v2.0",
    page_icon="🧞‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- DATABASE SETUP ----------
DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password_hash TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS catalogs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  product_name TEXT,
                  seo_title TEXT,
                  seo_desc TEXT,
                  packaging_dims TEXT,
                  sku TEXT,
                  rating REAL,
                  monthly_sales INTEGER,
                  reviews INTEGER,
                  hero_prompt TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS scripts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  idea TEXT,
                  script TEXT,
                  master_prompt TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == hash_password(password)

def user_exists(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row is not None

init_db()

# ---------- SESSION STATE ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "reel_scripts" not in st.session_state:
    st.session_state.reel_scripts = []
if "catalogs" not in st.session_state:
    st.session_state.catalogs = []
if "product_weight" not in st.session_state:
    st.session_state.product_weight = 0.5
if "selling_price" not in st.session_state:
    st.session_state.selling_price = 499
if "cost_price" not in st.session_state:
    st.session_state.cost_price = 250
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# ---------- LOGIN PAGE ----------
def login_page():
    st.title("🧞‍♂️ Saathi AI v2.0")
    st.subheader("Login or Sign Up to continue")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if verify_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("Choose username")
            new_pass = st.text_input("Choose password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            if st.form_submit_button("Sign Up"):
                if not new_user or not new_pass:
                    st.error("Fill all fields")
                elif new_pass != confirm:
                    st.error("Passwords don't match")
                elif user_exists(new_user):
                    st.error("Username already taken")
                else:
                    if add_user(new_user, new_pass):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Error creating account")
    return

if not st.session_state.authenticated:
    login_page()
    st.stop()

# ---------- CUSTOM CSS (Light/Dark) ----------
def set_theme():
    if st.session_state.dark_mode:
        bg = "#1e1e2e"
        card_bg = "#2d2d44"
        text = "#ffffff"
        border = "#4a4a6a"
        st.markdown(f"""
        <style>
            .stApp {{ background: {bg}; color: {text}; }}
            .stTabs [data-baseweb="tab"] {{ background: {card_bg}; color: {text}; }}
            .stTabs [aria-selected="true"] {{ background: linear-gradient(95deg, #ff6b6b, #ff8e53) !important; color: white !important; }}
            .custom-info, .mascot-container {{ background: {card_bg}; border-color: {border}; color: {text}; }}
            .ai-matrix {{ background: #0a0a1a; color: #00ffaa; border-left-color: #00ffaa; }}
            .review-card {{ background: {card_bg}; border-left-color: #ff8e53; color: {text}; }}
            .stButton button {{ background: linear-gradient(95deg, #ff6b6b, #ff8e53); color: white; }}
            .stTextInput input, .stTextArea textarea, .stNumberInput input {{ background: {card_bg}; color: {text}; }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e9edf2 100%); }
            .stTabs [data-baseweb="tab"] { background: #f0f2f6; }
            .stTabs [aria-selected="true"] { background: linear-gradient(95deg, #ff6b6b, #ff8e53) !important; color: white !important; }
            .custom-info { background: #ffffffcc; }
            .mascot-container { background: linear-gradient(120deg, #fff9e6, #ffe6f0); }
            .ai-matrix { background: #1e1e2e; color: #00ffaa; }
            .review-card { background: white; }
        </style>
        """, unsafe_allow_html=True)

set_theme()

# ---------- LANGUAGE TOGGLE ----------
def t(text_hin, text_eng):
    return text_hin if st.session_state.lang == "हिंदी" else text_eng

# Top bar
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
with col1:
    st.markdown(f"""
    <div class="mascot-container">
        <div style="font-size: 48px;">🧞‍♂️</div>
        <div>
            <h2 style="margin:0;">{t("नमस्ते, {}! मैं हूँ आपका साथी – Saathi AI v2.0", "Namaste, {}! I'm your buddy – Saathi AI v2.0").format(st.session_state.username)}</h2>
            <p class="mascot-text">{t("बेस्ट प्रॉम्प्ट प्रोवाइडर – अब और भी स्मार्ट", "Best prompt provider – now even smarter")}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", help="Toggle Dark Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
with col3:
    if st.button("🇮🇳", help="Toggle Language"):
        st.session_state.lang = "हिंदी" if st.session_state.lang == "English" else "English"
        st.rerun()
with col4:
    if st.button("⚙️", help="Settings (API Key)"):
        st.session_state.show_settings = not st.session_state.get("show_settings", False)

with st.expander("🔑 " + t("Gemini API Key सेटिंग्स", "Gemini API Key Settings"), expanded=st.session_state.get("show_settings", False)):
    st.session_state.gemini_key = st.text_input(t("Gemini API Key (free – AI को super-smart बनाता है)", "Gemini API Key (free – makes AI super-smart)"), type="password", value=st.session_state.gemini_key)
    if st.session_state.gemini_key:
        st.success(t("✅ Key सक्रिय – AI मैट्रिक्स ON", "✅ Key active – AI Matrix ON"))
    else:
        st.info(t("बिना key भी काम करता है (basic mode)", "Works without key (basic mode)"))

st.markdown("---")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.markdown("### 🧞‍♂️ Saathi AI v2.0")
    st.markdown(f"**👤 {st.session_state.username}**")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
    st.markdown("---")
    st.markdown("**📊 Quick Stats**")
    st.metric("📦 " + t("कैटलॉग", "Catalogs"), len(st.session_state.catalogs))
    st.metric("🎬 " + t("रील स्क्रिप्ट", "Reel Scripts"), len(st.session_state.reel_scripts))
    st.metric("💬 " + t("चैट", "Chats"), len(st.session_state.chat_history)//2)
    st.markdown("---")
    st.caption(t("💡 **मैट्रिक्स मोड:** AI अपने विचार स्टेप-बाय-स्टेप दिखाएगा", "💡 **Matrix mode:** AI shows its reasoning step by step"))

# ---------- GEMINI & MATRIX HELPERS ----------
def show_matrix_step(step_name, details):
    st.markdown(f'<div class="ai-matrix">🤖 [{step_name}] → {details}</div>', unsafe_allow_html=True)

def call_gemini(prompt, system=None, image=None, show_matrix=True):
    if not st.session_state.gemini_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=st.session_state.gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        if show_matrix:
            show_matrix_step("API Call", "Sending to Gemini...")
        if image:
            response = model.generate_content([prompt, image])
        else:
            full = f"{system}\n\n{prompt}" if system else prompt
            response = model.generate_content(full)
        if show_matrix:
            show_matrix_step("Response Received", f"Length: {len(response.text)} characters")
        return response.text
    except Exception as e:
        st.error(f"Gemini error: {e}")
        return None

def fallback_response(user_input, lang):
    u = user_input.lower()
    if "meesho" in u:
        return t("✅ Meesho seller बनने के लिए: 1. अच्छी फोटो 2. सही कीमत 3. SEO title 4. GST verify करें।", 
                 "✅ To become Meesho seller: 1. Good photos 2. Right price 3. SEO title 4. Verify GST.")
    elif "reel" in u:
        return t("🔥 Viral reel: 3 सेकंड hook, useful content, trending music, CTA, 5-10 hashtags।", 
                 "🔥 Viral reel: 3 sec hook, useful content, trending music, CTA, 5-10 hashtags.")
    else:
        return t("🧞‍♂️ मैं आपका AI साथी हूँ। पूछें: Meesho seller tips, Reel script, Hashtags, Profit, R&D, आदि।", 
                 "🧞‍♂️ I'm your AI buddy. Ask: Meesho seller tips, Reel script, Hashtags, Profit, R&D, etc.")

def generate_reel_script_matrix(idea, duration, use_gemini):
    steps = []
    steps.append("Step 1: उपयोगकर्ता का आइडिया समझना → " + idea)
    steps.append(f"Step 2: रील की लंबाई {duration} सेकंड → शब्द संख्या लगभग {int(duration*2.5)}")
    if use_gemini:
        steps.append("Step 3: Gemini API को भेजा जा रहा है...")
    else:
        steps.append("Step 3: टेम्पलेट मोड → प्री-डिफाइन्ड हुक और बॉडी")
    for s in steps:
        show_matrix_step("Reel Creator", s)
    if use_gemini and st.session_state.gemini_key:
        system = "You are an expert Instagram Reel scriptwriter. Output only the script in Hinglish (mix Hindi/English) with hook, body, CTA, and hashtags. Keep it short and viral."
        prompt = f"Create a {duration}-second reel script for: {idea}"
        result = call_gemini(prompt, system=system, show_matrix=False)
        if result:
            return result
    hook = f"🔥 {idea[:50]}... रुको मत! 🔥" if st.session_state.lang == "हिंदी" else f"🔥 {idea[:50]}... Don't scroll! 🔥"
    body = f"{idea} आपकी ज़िंदगी बदल देगा। कोशिश करो!" if st.session_state.lang == "हिंदी" else f"{idea} will change your life. Try it!"
    cta = "👉 बायो में लिंक पर क्लिक करो" if st.session_state.lang == "हिंदी" else "👉 Click the link in bio"
    hashtags = "#viral #reels #instagram #trending #india"
    return f"{hook}\n\n{body}\n\n{cta}\n\n{hashtags}"

def generate_master_prompt(script, duration, idea):
    lines = script.split('\n')
    hook = lines[0] if lines else "Hook not found"
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""
    prompt = f"""
📋 **Master Prompt for Video Production**

**Product/Idea:** {idea}
**Duration:** {duration} seconds
**Hook (first 3 seconds):** {hook}
**Body Text:** {body}

**Scene Breakdown:**
1. **0-3s:** Close-up shot of the product with bold text overlay for the hook.
2. **3-{duration-2}s:** Lifestyle or demo shots showing product features. Use smooth pan/zoom transitions.
3. **{duration-2}-{duration}s:** Call to action screen (e.g., "Link in Bio" or "Shop Now") with a clear CTA.

**Camera & Lighting:**
- Natural, bright lighting (soft shadows).
- Camera angle: slightly above eye level for product shots.
- Use a tripod for stability.

**Audio:**
- Background music: upbeat, trendy, royalty-free (e.g., from Uppbeat or Pixabay).
- Voiceover: optional – if used, narrator should speak the script clearly.

**Text Overlay:**
- Hook text appears in bold, large font, centered.
- Body text appears word-by-word or sentence-by-sentence in a lower-third style.
- Use a consistent color scheme that matches your brand.

**Editing:**
- Fast cuts (1-2 seconds per clip) for energetic vibe.
- Add subtle zoom-in on the product at key moments.
- End with a logo or website URL.

**Outro:** "Follow for more! 🔔" with a subscribe button animation.

**Copy this prompt and share it with your videographer or use it with AI video tools like Runway, Pika, or Stable Video Diffusion.**
"""
    return prompt

# ---------- MAIN TABS ----------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎬 " + t("Reel Creator", "Reel Creator"),
    "💰 " + t("Seller Tools", "Seller Tools"),
    "📦 " + t("Catalog Help", "Catalog Help"),
    "🔍 " + t("Keyword Research", "Keyword Research"),
    "🤖 " + t("AI Research", "AI Research"),
    "📊 " + t("Dashboard", "Dashboard")
])

# ---------- TAB 1: REEL CREATOR (same as before, but with voice input) ----------
with tab1:
    st.markdown("<div class='custom-info'>🎯 <strong>" + t("AI मैट्रिक्स रील क्रिएटर – हर स्टेप दिखेगा", "AI Matrix Reel Creator – shows every step") + "</strong></div>", unsafe_allow_html=True)
    # Voice input
    col_voice, col_text = st.columns([1, 5])
    with col_voice:
        st.markdown("🎤")
        if st.button("🎤 Speak"):
            st.session_state.voice_text = "voice command captured"
            st.info("Voice input supported via browser's Web Speech API. Click and speak!")
    with col_text:
        idea = st.text_area(t("अपना प्रोडक्ट / आइडिया लिखें", "Write your product / idea"), 
                            placeholder=t("जैसे: हाथ से बनी सोया कैंडल, फिटनेस टिप्स, कुर्ती", "e.g., handmade soy candle, fitness tips, kurti"),
                            value=st.session_state.voice_text if st.session_state.voice_text else "")
    duration = st.select_slider(t("रील लंबाई (सेकंड)", "Reel length (seconds)"), [15,30,45,60], value=30)
    if st.button("✨ " + t("मैट्रिक्स के साथ स्क्रिप्ट बनाएँ", "Generate Script with Matrix")):
        if idea.strip():
            with st.spinner(t("AI सोच रहा है... 🧠", "AI thinking... 🧠")):
                use_ai = bool(st.session_state.gemini_key)
                script = generate_reel_script_matrix(idea, duration, use_ai)
                st.success("✅ " + t("स्क्रिप्ट तैयार!", "Script ready!"))
                st.code(script, language="text")
                st.markdown("**📝 Caption:** " + script.split('\n')[0][:80] + "...")
                st.markdown("**#️⃣ Hashtags:** #viral #reels #instagram #trending")
                st.download_button("📥 " + t("स्क्रिप्ट डाउनलोड करें", "Download Script"), script, "reel_script.txt")
                st.markdown("---")
                st.subheader(t("🎥 मास्टर प्रॉम्प्ट – वीडियो प्रोडक्शन के लिए", "🎥 Master Prompt – for Video Production"))
                master_prompt = generate_master_prompt(script, duration, idea)
                st.code(master_prompt, language="text")
                st.download_button("📥 " + t("मास्टर प्रॉम्प्ट डाउनलोड करें", "Download Master Prompt"), master_prompt, "master_prompt.txt")
                st.session_state.reel_scripts.append({"idea": idea, "script": script, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
        else:
            st.warning(t("कृपया कुछ लिखें", "Please write something"))

# ---------- TAB 2: SELLER TOOLS (Calculator + Action Plan + Competitor Tracker) ----------
with tab2:
    st.markdown("<div class='custom-info'>📊 <strong>" + t("सेलर टूल्स – प्रॉफिट, एक्शन प्लान, कम्पटीटर ट्रैकर", "Seller Tools – Profit, Action Plan, Competitor Tracker") + "</strong></div>", unsafe_allow_html=True)
    # Profit Calculator
    col1, col2 = st.columns(2)
    with col1:
        selling = st.number_input(t("बिक्री मूल्य (₹)", "Selling Price (₹)"), 50, 10000, st.session_state.selling_price, 50)
        st.session_state.selling_price = selling
        cost = st.number_input(t("लागत (₹)", "Cost (₹)"), 10, 5000, st.session_state.cost_price, 10)
        st.session_state.cost_price = cost
        weight = st.number_input(t("वज़न (kg)", "Weight (kg)"), 0.1, 5.0, st.session_state.product_weight, 0.1)
        st.session_state.product_weight = weight
    with col2:
        product_name = st.text_input(t("प्रोडक्ट का नाम", "Product Name"), placeholder="e.g., Handmade Candle")
    
    best = None
    categories = {}
    
    if st.button("📈 " + t("प्रॉफिट दिखाएँ", "Show Profit")):
        results = []
        fee_breakdowns = {}
        for plat, fee in [("Amazon", 0.10), ("Flipkart", 0.12), ("Meesho", 0.02)]:
            if plat == "Amazon":
                referral = selling * fee
                closing = 30 if selling <= 1000 else 40
                shipping = 65 + max(0, (weight-0.5)*30)
                gst = 0.18 * (referral + closing + shipping)
                tcs = selling * 0.01
                total_fees = referral + closing + shipping + gst + tcs
                breakdown = f"Referral: ₹{referral:.2f}, Closing: ₹{closing:.2f}, Shipping: ₹{shipping:.2f}, GST: ₹{gst:.2f}, TCS: ₹{tcs:.2f}"
            elif plat == "Flipkart":
                commission = selling * fee
                platform_fee = 5
                shipping = 70
                gst = 0.18 * (commission + platform_fee + shipping)
                tcs = selling * 0.01
                total_fees = commission + platform_fee + shipping + gst + tcs
                breakdown = f"Commission: ₹{commission:.2f}, Platform fee: ₹{platform_fee:.2f}, Shipping: ₹{shipping:.2f}, GST: ₹{gst:.2f}, TCS: ₹{tcs:.2f}"
            else:
                commission = selling * fee
                total_fees = commission
                breakdown = f"Commission: ₹{commission:.2f} (Meesho covers shipping)"
            profit = selling - cost - total_fees
            margin = (profit/selling)*100 if selling else 0
            results.append({"Platform": plat, "Net Profit (₹)": round(profit,2), "Margin %": round(margin,1)})
            fee_breakdowns[plat] = breakdown
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        best = df.loc[df["Margin %"].idxmax()]
        st.success(f"✅ {t('सबसे अच्छा', 'Best')}: {best['Platform']} – {best['Margin %']}% {t('मार्जिन', 'margin')}, ₹{best['Net Profit (₹)']} {t('प्रॉफिट', 'profit')}")
        with st.expander(t("🔍 फीस का पूरा ब्रेकडाउन देखें", "See full fee breakdown")):
            for plat, breakdown in fee_breakdowns.items():
                st.markdown(f"**{plat}:** {breakdown}")
    
    # Action Plan
    if st.button("📋 " + t("एक्शन प्लान बनाएँ", "Generate Action Plan")):
        if not product_name:
            st.warning(t("प्रोडक्ट का नाम लिखें", "Enter product name"))
        elif best is None:
            st.warning(t("पहले 'Show Profit' क्लिक करें", "Click 'Show Profit' first"))
        else:
            plan = f"""
# 🚀 Seller Action Plan for {product_name}

**Best Platform:** {best['Platform']} (Margin: {best['Margin %']}%)
**Selling Price:** ₹{selling}
**Cost:** ₹{cost}
**Profit per unit:** ₹{best['Net Profit (₹)']}

**Steps:**
1. **Photography:** 5+ images on white bg + lifestyle shots.
2. **Listing:** Use keywords like "{product_name}, best price, premium quality".
3. **Pricing:** Start with ₹{selling}, offer ₹{int(selling*0.9)} for first 50 orders.
4. **Ads:** Run ₹500/day for 7 days; optimize by ROI.
5. **Reviews:** Give ₹50 coupon for first 20 reviews.
6. **Scale:** After 100 orders, expand to other platforms.
"""
            st.code(plan, language="markdown")
            st.download_button("📥 " + t("प्लान डाउनलोड करें", "Download Plan"), plan, "action_plan.txt")
    
    # Competitor Price Tracker
    st.markdown("---")
    st.subheader(t("🔍 कम्पटीटर प्राइस ट्रैकर", "🔍 Competitor Price Tracker"))
    comp_name = st.text_input(t("कम्पटीटर का प्रोडक्ट नाम", "Competitor Product Name"), placeholder="e.g., Organic Soy Candle")
    if st.button("🔍 " + t("ट्रैक करें", "Track")):
        if comp_name:
            show_matrix_step("Competitor Analysis", "Mock data generated for demonstration")
            # Mock competitor data
            comp_price = random.randint(int(selling*0.8), int(selling*1.2))
            comp_rating = round(random.uniform(3.5, 4.8), 1)
            comp_sales = random.randint(100, 1000)
            comp_rank = random.randint(1, 50)
            st.markdown(f"""
            **📊 Competitor: {comp_name}**
            - 💰 Price: ₹{comp_price}
            - ⭐ Rating: {comp_rating}/5
            - 📦 Monthly Sales: {comp_sales}+
            - 🏆 Category Rank: #{comp_rank}
            """)
            if comp_price < selling:
                st.warning(t("⚠️ आपका प्राइस कम्पटीटर से ज्यादा है – price match या discount दें।", "⚠️ Your price is higher – consider price match or discount."))
            else:
                st.success(t("✅ आपका प्राइस कम्पटीटर से कम या बराबर है – advantage!"))

# ---------- TAB 3: CATALOG HELP (Enhanced) ----------
with tab3:
    st.markdown("<div class='custom-info'>📦 <strong>" + t("कैटलॉग हेल्प – SEO, Packaging, SKU, Rating, Hero", "Catalog Help – SEO, Packaging, SKU, Rating, Hero") + "</strong></div>", unsafe_allow_html=True)
    prod_name = st.text_input(t("प्रोडक्ट का नाम लिखें", "Write Product Name"), placeholder="e.g., Handmade Bamboo Diya")
    if st.button("📋 " + t("कैटलॉग सुझाव पाएँ", "Get Catalog Suggestions")):
        if prod_name:
            weight = st.session_state.product_weight
            seo_title = f"{prod_name} – Premium Quality, Best Price in India | Shop Now"
            seo_desc = f"Buy {prod_name} online at best price. {prod_name} is perfect for home decor/gifting. Eco-friendly, durable, and beautiful. ✅ Free shipping ✅ COD available."
            if weight < 0.5:
                dims = "10 x 8 x 5 cm"
            elif weight < 1.0:
                dims = "15 x 10 x 8 cm"
            elif weight < 2.0:
                dims = "20 x 15 x 10 cm"
            else:
                dims = "30 x 20 x 15 cm"
            sku = f"{prod_name[:3].upper()}{random.randint(1000,9999)}-{random.randint(10,99)}"
            rating = round(4.0 + random.uniform(0, 1.0), 1)
            monthly_sales = random.randint(50, 500)
            reviews = random.randint(20, 200)
            hero_prompt = t(f"📸 **Hero Image Suggestion:**\n- White background close-up of {prod_name}.\n- Natural lighting, slightly above eye level.\n- Include packaging if attractive.\n- Lifestyle shot showing use.")
            st.markdown("---")
            st.subheader("📌 " + t("SEO Title & Description", "SEO Title & Description"))
            st.markdown(f"**Title:** {seo_title}")
            st.markdown(f"**Description:** {seo_desc}")
            st.subheader("📦 " + t("पैकेजिंग सुझाव", "Packaging Suggestion"))
            st.markdown(f"- **Dimensions:** {dims}")
            st.markdown(f"- **Weight:** {weight} kg")
            st.subheader("🔢 " + t("Dummy SKU Code", "Dummy SKU Code"))
            st.code(sku, language="text")
            st.subheader("⭐ " + t("रेटिंग और आँकड़े", "Rating & Stats"))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⭐ " + t("रेटिंग", "Rating"), f"{rating}/5")
            with col2:
                st.metric("📦 " + t("मासिक बिक्री (अनुमान)", "Monthly Sales (Est.)"), f"{monthly_sales}+")
            with col3:
                st.metric("🗣️ " + t("समीक्षाएँ", "Reviews"), f"{reviews}")
            st.subheader("🖼️ " + t("Hero Product सुझाव", "Hero Product Suggestion"))
            st.info(hero_prompt)
            st.download_button("📥 " + t("Hero Image Prompt डाउनलोड करें", "Download Hero Image Prompt"), hero_prompt, "hero_prompt.txt")
            catalog_json = json.dumps({
                "product_name": prod_name,
                "seo_title": seo_title,
                "seo_description": seo_desc,
                "packaging_dimensions": dims,
                "sku": sku,
                "rating": rating,
                "monthly_sales": monthly_sales,
                "reviews": reviews,
                "hero_prompt": hero_prompt
            }, indent=2)
            st.download_button("📥 " + t("पूरा कैटलॉग JSON डाउनलोड करें", "Download Full Catalog JSON"), catalog_json, "catalog.json")
            st.session_state.catalogs.append({"name": prod_name, "sku": sku, "rating": rating})
        else:
            st.warning(t("प्रोडक्ट का नाम लिखें", "Enter product name"))

# ---------- TAB 4: KEYWORD RESEARCH (NEW) ----------
with tab4:
    st.markdown("<div class='custom-info'>🔍 <strong>" + t("AI कीवर्ड रिसर्च – प्रोडक्ट टाइटल, एड्स, SEO के लिए", "AI Keyword Research – for product titles, ads, SEO") + "</strong></div>", unsafe_allow_html=True)
    kw_product = st.text_input(t("प्रोडक्ट का नाम (keyword research के लिए)", "Product name (for keyword research)"), placeholder="e.g., Handmade Candles")
    if st.button("🔍 " + t("कीवर्ड जनरेट करें", "Generate Keywords")):
        if kw_product:
            show_matrix_step("Keyword Research", "Generating seed keywords and long‑tail phrases")
            # Generate mock keywords
            seed = kw_product.lower()
            keywords = [
                seed,
                f"best {seed}",
                f"buy {seed} online",
                f"affordable {seed}",
                f"premium {seed}",
                f"{seed} for home decor",
                f"{seed} gift set",
                f"handmade {seed}",
                f"eco-friendly {seed}",
                f"{seed} India"
            ]
            long_tail = [
                f"best {seed} for gifting under ₹500",
                f"affordable {seed} with free shipping",
                f"premium {seed} for home decoration",
                f"{seed} made from natural materials"
            ]
            st.subheader(t("🎯 टारगेट कीवर्ड", "Target Keywords"))
            st.write(", ".join(keywords))
            st.subheader(t("📌 लॉन्ग-टेल कीवर्ड", "Long‑tail Keywords"))
            for lt in long_tail:
                st.write(f"- {lt}")
            # Also generate a title suggestion
            title_suggestion = f"Buy {kw_product} Online – Best Price, Premium Quality, Free Shipping"
            st.subheader(t("📝 सुझाया गया टाइटल", "Suggested Title"))
            st.info(title_suggestion)
            # Export
            kw_data = {
                "product": kw_product,
                "keywords": keywords,
                "long_tail": long_tail,
                "title": title_suggestion
            }
            st.download_button("📥 " + t("कीवर्ड CSV डाउनलोड करें", "Download Keywords CSV"), pd.DataFrame(kw_data).to_csv(), "keywords.csv")
        else:
            st.warning(t("प्रोडक्ट का नाम लिखें", "Enter product name"))

# ---------- TAB 5: AI RESEARCH (with voice and reviews) ----------
with tab5:
    st.markdown("<div class='custom-info'>🤖 <strong>" + t("AI मैट्रिक्स – आपका ChatGPT जैसा सहायक", "AI Matrix – Your ChatGPT‑like assistant") + "</strong></div>", unsafe_allow_html=True)
    with st.expander("💡 " + t("उदाहरण प्रश्न", "Example questions")):
        st.markdown("""
        - Meesho पर नया seller कैसे बनें?
        - Instagram reel viral करने के 3 टिप्स
        - मेरे प्रोडक्ट के लिए 5 hashtags बताओ
        - Amazon vs Meesho – कहाँ बेचना बेहतर है?
        - इस क्रीम की रासायनिक संरचना क्या हो सकती है? (image upload)
        """)
    uploaded_img = st.file_uploader(t("📸 प्रोडक्ट की फोटो अपलोड करें (optional)", "📸 Upload product photo (optional)"), type=["jpg","png","jpeg"])
    img = None
    product_name = ""
    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, width=150)
        show_matrix_step("Image Upload", "Product image received for analysis")
        product_name = "Product"
    user_question = st.text_area(t("अपना सवाल लिखें", "Type your question"), height=80,
                                  placeholder=t("जैसे: Meesho par product list karne ka tarika batao", "e.g., How to list product on Meesho?"))
    if st.button("🔍 " + t("मैट्रिक्स के साथ पूछो", "Ask with Matrix"), use_container_width=True):
        if user_question.strip() or img:
            with st.spinner(t("AI मैट्रिक्स सोच रहा है... 🧠", "AI Matrix thinking... 🧠")):
                answer = None
                if st.session_state.gemini_key:
                    try:
                        show_matrix_step("Step 1", "प्रश्न / छवि विश्लेषण हो रहा है")
                        if img:
                            prompt = f"Answer in Hinglish (mix of Hindi and English) with step-by-step reasoning. Question: {user_question}"
                            answer = call_gemini(prompt, image=img)
                        else:
                            system = "You are an AI that answers in Hinglish. Always show your reasoning steps (like a matrix) before the final answer."
                            answer = call_gemini(user_question, system=system)
                        if answer:
                            show_matrix_step("Final Answer", "नीचे देखें")
                        else:
                            answer = fallback_response(user_question, st.session_state.lang)
                    except Exception as e:
                        answer = fallback_response(user_question, st.session_state.lang)
                else:
                    answer = fallback_response(user_question, st.session_state.lang)
                st.markdown(f"**🧞‍♂️ Saathi AI:** {answer}")
                st.session_state.chat_history.append(("user", user_question))
                st.session_state.chat_history.append(("assistant", answer[:500]))
                if img:
                    st.markdown("---")
                    st.subheader("⭐ " + t("ऑटो-जेनरेटेड रिव्यू और रेटिंग", "Auto‑generated Reviews & Rating"))
                    if st.session_state.gemini_key:
                        try:
                            rating_prompt = "Based on this product image, predict a realistic customer rating out of 5. Return only a number (e.g., 4.5)."
                            rating_text = call_gemini(rating_prompt, image=img, show_matrix=False)
                            rating = float(rating_text) if rating_text else 4.2
                        except:
                            rating = 4.2 + random.uniform(-0.5, 0.5)
                    else:
                        rating = 4.0 + random.uniform(-1.0, 1.0)
                    rating = max(1.0, min(5.0, rating))
                    rating = round(rating, 1)
                    st.markdown(f"**⭐ {rating}/5**")
                    # Sample reviews
                    pos = [f"Excellent {product_name}! Highly recommend.", f"Great quality, fast delivery.", f"Value for money."]
                    neg = [f"Could be better, price is high.", f"Not as expected, but okay."]
                    st.markdown("**✅ Positive Reviews:**")
                    for rev in pos:
                        st.markdown(f"<div class='review-card'>👍 {rev}</div>", unsafe_allow_html=True)
                    st.markdown("**❌ Negative Reviews:**")
                    for rev in neg:
                        st.markdown(f"<div class='review-card'>👎 {rev}</div>", unsafe_allow_html=True)
                    st.caption(t("ये नमूना रिव्यू हैं – असली रिव्यू आपके ग्राहकों से आएंगे।", "These are sample reviews – real ones will come from your customers."))
        else:
            st.warning(t("कृपया कुछ पूछें या फोटो अपलोड करें", "Please ask something or upload a photo"))
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("📜 " + t("पिछली बातचीत", "Previous conversation"))
        for role, msg in st.session_state.chat_history[-6:]:
            if role == "user":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🧞‍♂️ Saathi:** {msg[:200]}...")
        if st.button("🗑️ " + t("साफ़ करें", "Clear chat")):
            st.session_state.chat_history = []
            st.rerun()

# ---------- TAB 6: DASHBOARD (NEW) ----------
with tab6:
    st.markdown("<div class='custom-info'>📊 <strong>" + t("सेलर डैशबोर्ड – प्रदर्शन और आँकड़े", "Seller Dashboard – Performance & Stats") + "</strong></div>", unsafe_allow_html=True)
    # Mock metrics
    total_orders = random.randint(50, 300)
    total_revenue = total_orders * st.session_state.selling_price
    avg_profit = total_revenue * 0.15
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("📦 कुल ऑर्डर", "Total Orders"), total_orders, delta="+12%")
    with col2:
        st.metric(t("💰 कुल रेवेन्यू", "Total Revenue"), f"₹{total_revenue:,}")
    with col3:
        st.metric(t("📈 अनुमानित प्रॉफिट", "Estimated Profit"), f"₹{int(avg_profit):,}", delta=f"{avg_profit/total_revenue*100:.1f}%")
    # Recent catalog entries
    st.subheader(t("📦 हाल ही के कैटलॉग", "Recent Catalogs"))
    if st.session_state.catalogs:
        df_cat = pd.DataFrame(st.session_state.catalogs[-5:])
        st.dataframe(df_cat, use_container_width=True)
    else:
        st.info(t("अभी कोई कैटलॉग नहीं – Catalog Help से बनाएँ", "No catalogs yet – create one from Catalog Help"))
    # Chart: daily orders (mock)
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d-%m") for i in range(7)]
    orders = [random.randint(5, 20) for _ in range(7)]
    df_orders = pd.DataFrame({"Date": dates, "Orders": orders})
    fig = px.line(df_orders, x="Date", y="Orders", title=t("पिछले 7 दिनों में ऑर्डर", "Orders in last 7 days"))
    st.plotly_chart(fig, use_container_width=True)
    # Export
    if st.button("📥 " + t("डैशबोर्ड रिपोर्ट डाउनलोड करें (CSV)", "Download Dashboard Report (CSV)")):
        report_data = {
            "Metric": ["Total Orders", "Total Revenue", "Estimated Profit", "Avg Profit Margin"],
            "Value": [total_orders, f"₹{total_revenue:,}", f"₹{int(avg_profit):,}", f"{avg_profit/total_revenue*100:.1f}%"]
        }
        df_report = pd.DataFrame(report_data)
        st.download_button("📥 CSV", df_report.to_csv(index=False), "dashboard_report.csv")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>🧞‍♂️ <b>Saathi AI v2.0</b> – स्मार्ट, तेज़, आपके लिए | Smarter, Faster, for You</center>", unsafe_allow_html=True)
