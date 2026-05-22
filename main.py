import streamlit as st
import numpy as np
import time
import pandas as pd
from datetime import datetime

# ✅ FIX #1: set_page_config MUST be the very first Streamlit call.
# Moving it before any other st.* call prevents "StreamlitAPIException".
st.set_page_config(page_title="Homigo | Smart Hub", layout="wide", initial_sidebar_state="expanded")

# ✅ FIX #2: cv2 is an optional heavy dependency. Guard the import so the app
# doesn't crash on environments where opencv-python is not installed.
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# --- 1. SESSION STATE INITIALIZATION ---
# ✅ FIX #3: Added 'temp_data' and 'temp_name' to initial session state so they
# always exist. Accessing a missing key in st.session_state raises a KeyError.
defaults = {
    'is_subscribed': False,
    'checkout_step': 'selection',
    'subscription_data': {},
    'temp_data': {},
    'temp_name': '',
    'active_subpage': None,   # None | 'activate_plan' | 'request_consultancy'
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- CUSTOM UI INJECTION ---
st.markdown("""
    <style>
        [data-testid="stHeader"] { display: none !important; }

        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem;
            max-width: 100%;
            padding-left: 0;
            padding-right: 0;
        }

        .navbar {
            background-color: #4a148c;
            padding: 15px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            position: relative;
            z-index: 10000;
        }
        .nav-logo { font-size: 26px; font-weight: bold; }
        .nav-logo span { color: #ffab40; margin-left: 2px; }
        .nav-right { display: flex; align-items: center; gap: 25px; font-size: 14px; }
        .nav-right a.nav-link { color: white; text-decoration: none; font-weight: 600; transition: 0.2s; }
        .nav-right a.nav-link:hover { color: #ffab40; }
        .sign-in-btn {
            background-color: white; color: #4a148c !important;
            padding: 8px 20px; border-radius: 30px;
            font-weight: bold; text-decoration: none;
            display: flex; align-items: center; gap: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .sign-in-btn:hover { background-color: #f0f0f0; }

        .hero {
            background-image: linear-gradient(rgba(74, 20, 140, 0.88), rgba(106, 27, 154, 0.95)),
                              url('https://i.postimg.cc/WzBxJmgD/image.png');
            padding: 40px 5%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            border-bottom: 6px solid #ffab40;
        }
        .hero-image-container { flex: 1; text-align: center; }
        .hero-image-container img {
            width: 100%; max-width: 450px;
            border: none !important; box-shadow: none !important;
            background: transparent; filter: none;
        }
        .hero-text { flex: 1.2; text-align: right; padding-left: 20px; }
        .hero h1 { font-weight: 300; margin-bottom: 10px; color: white; font-size: 32px; line-height: 1.2; }
        .hero .highlight { color: #ffab40; font-size: 60px; font-weight: 900; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .hero h2 { color: white; font-size: 22px; font-weight: 500; }

        .services-section {
            padding: 60px 5%;
            background-color: #ffffff;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .services-section h2 { color: #111; font-size: 32px; margin-bottom: 50px; font-weight: 700; }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 40px; max-width: 1200px; margin: 0 auto;
        }
        .service-card { display: flex; flex-direction: column; align-items: center; cursor: pointer; }
        .img-circle {
            width: 110px; height: 110px; border-radius: 50%; object-fit: cover;
            margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            border: 3px solid #f3e5f5;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s, box-shadow 0.3s;
        }
        .service-card:hover .img-circle {
            transform: scale(1.15) translateY(-8px);
            border-color: #ffab40; box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        }
        .card-label { color: #333; font-size: 15px; font-weight: 600; transition: color 0.3s; }
        .service-card:hover .card-label { color: #6a1b9a; }

        /* Mega Menu */
        .nav-item-dropdown { position: relative; display: inline-block; }
        .mega-menu {
            visibility: hidden; opacity: 0;
            position: absolute; top: 100%; left: 0;
            width: min(800px, 90vw);
            background-color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 9999; padding: 25px; border-radius: 12px; border: 1px solid #ddd;
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
            transition: all 0.25s ease; transform: translateY(10px);
        }
        .nav-item-dropdown:hover .mega-menu { visibility: visible; opacity: 1; transform: translateY(0px); }
        .mega-col { display: flex; flex-direction: column; }
        .mega-title { color: #4a148c; font-weight: 800; font-size: 13px; margin-bottom: 8px; border-bottom: 2px solid #ffab40; padding-bottom: 4px; white-space: nowrap; }
        .mega-link { color: #555; text-decoration: none; font-size: 12px; margin: 2px 0; transition: color 0.2s ease; }
        .mega-link:hover { color: #ffab40; }

        /* ✅ IMPROVEMENT: Styled status badges */
        .status-badge {
            display: inline-block; padding: 4px 12px; border-radius: 20px;
            font-size: 13px; font-weight: 600;
        }
        .status-active { background: #e8f5e9; color: #2e7d32; }
        .status-inactive { background: #fff3e0; color: #e65100; }

        .custom-footer {
            background-color: #161619; color: #a0a0a0;
            padding: 60px 5% 20px 5%;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-top: 50px;
        }
        .footer-grid { display: flex; flex-wrap: wrap; justify-content: space-between; margin-bottom: 40px; }
        .footer-brand { max-width: 250px; }
        .footer-brand h2 { color: white; font-size: 24px; font-weight: bold; margin-bottom: 10px; }
        .footer-brand h2 span { color: #ffab40; }
        .footer-brand p { font-size: 14px; line-height: 1.5; margin-bottom: 20px; }
        .footer-cols { display: flex; gap: 60px; flex-wrap: wrap; }
        .footer-col h4 { color: #ffab40; font-size: 16px; font-weight: 600; margin-bottom: 20px; }
        .footer-col ul { list-style: none; padding: 0; margin: 0; }
        .footer-col ul li { margin-bottom: 12px; }
        .footer-col ul li a { color: #a0a0a0; text-decoration: none; font-size: 14px; transition: color 0.2s; cursor: pointer; }
        .footer-col ul li a:hover { color: white; }
        .footer-bottom {
            border-top: 1px solid #333; padding-top: 20px;
            display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; flex-wrap: wrap;
        }

        div.stButton > button:first-child {
            background-color: #6a1b9a; color: white; border: none; font-weight: bold;
            padding: 12px 28px; border-radius: 8px; font-size: 16px;
        }
        div.stButton > button:hover { background-color: #4a148c; color: #ffab40; }

        /* ── Action Blocks (teal, matching reference image) ── */
        .action-blocks-row {
            display: flex;
            justify-content: center;
            gap: 40px;
            padding: 40px 5% 10px 5%;
            flex-wrap: wrap;
        }
        .action-block {
            display: flex;
            align-items: center;
            gap: 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 18px rgba(0,150,136,0.18);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            min-width: 280px;
        }
        .action-block:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 28px rgba(0,150,136,0.28);
        }
        .action-block-icon {
            background-color: #e0f4f2;
            width: 72px;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .action-block-icon svg { width: 36px; height: 36px; color: #00897b; }
        .action-block-label {
            background-color: #00897b;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 800;
            font-size: 15px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 0 28px;
            height: 72px;
            display: flex;
            align-items: center;
        }

        /* ── Subpage container ── */
        .subpage-header {
            background: linear-gradient(135deg, #00695c, #00897b);
            color: white;
            padding: 22px 5%;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 22px;
            font-weight: 700;
        }
        .subpage-header span { font-size: 28px; }
    </style>
""", unsafe_allow_html=True)


# --- 2. SIDEBAR ---
st.sidebar.title("🏠 Homigo")
if st.session_state.is_subscribed:
    d = st.session_state.subscription_data
    st.sidebar.success(f"🛡️ Shield Active: {d.get('brand', '')} {d.get('appliance', '')}")
else:
    st.sidebar.warning("🛡️ Status: No Active Plan")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["🏠 Home / AMC Hub", "🛡️ Guardian Live Feed", "📷 AI Diagnostics"])


# ----------------------------------------
# PAGE 1: HOME / AMC HUB
# ----------------------------------------
if menu == "🏠 Home / AMC Hub":

    st.markdown("""
        <div class="navbar">
            <div class="nav-logo">Homigo<span>●</span></div>
            <div class="nav-right">
                <div class="nav-item-dropdown">
                    <a class="nav-link">Device & Plans ▾</a>
                    <div class="mega-menu">
                        <div class="mega-col">
                            <span class="mega-title">Air Conditioner</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                            <span class="mega-title" style="margin-top:20px;">Air Purifier</span>
                            <a href="#" class="mega-link">Request Service</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Refrigerator</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                            <span class="mega-title" style="margin-top:20px;">Washing Machine</span>
                            <a href="#" class="mega-link">Request Service</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Television</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                            <span class="mega-title" style="margin-top:20px;">Laptop</span>
                            <a href="#" class="mega-link">Request Service</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Mobile Phone</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                            <span class="mega-title" style="margin-top:20px;">Microwave</span>
                            <a href="#" class="mega-link">Request Service</a>
                        </div>
                    </div>
                </div>
                <a href="#" class="nav-link">Activate Plan</a>
                <a href="#" class="nav-link">Track Service Request</a>
                <a href="#" class="sign-in-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    Sign In
                </a>
                <a href="#" style="color:white; font-size:20px; text-decoration:none;">🛒</a>
            </div>
        </div>

        <div class="hero">
            <div class="hero-image-container">
                <img src="https://i.postimg.cc/WzBxJmgD/image.png" alt="Home Appliances">
            </div>
            <div class="hero-text">
                <h1>Say goodbye to unexpected repair costs with</h1>
                <div class="highlight">Homigo Shield</div>
                <h2>Premier Care For Your Home Devices</h2>
            </div>
        </div>
        
        <div class="services-section">
            <h2 style="text-decoration: underline;">Browse Our Expertise</h2>
            <div class="grid-container">
                <div class="service-card">
                    <img src="https://i.postimg.cc/0rgDRrR3/image.png" class="img-circle" alt="AC">
                    <div class="card-label">Air Conditioner</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/gJDT0F2F/image.png" class="img-circle" alt="TV">
                    <div class="card-label">Television</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/XNB53KHz/image.png" class="img-circle" alt="Mobile">
                    <div class="card-label">Mobile Phone</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/pTXBq9RS/image.png" class="img-circle" alt="Fridge">
                    <div class="card-label">Refrigerator</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/XN5gx0bq/image.png" class="img-circle" alt="Washing Machine">
                    <div class="card-label">Washing Machine</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/HkncZQy8/image.png" class="img-circle" alt="Microwave">
                    <div class="card-label">Microwave</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/9XPLCjNq/image.png" class="img-circle" alt="Printer">
                    <div class="card-label">Printer</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/WpyQqV7L/image.png" class="img-circle" alt="Laptop">
                    <div class="card-label">Laptops</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/y6w74ctf/image.png" class="img-circle" alt="Camera">
                    <div class="card-label">Digital Camera</div>
                </div>
                <div class="service-card">
                    <img src="https://i.postimg.cc/8PHXBVRh/image.png" class="img-circle" alt="Locals">
                    <div class="card-label">Locals</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)

    with st.container():

        # VIEW A: DASHBOARD
        if st.session_state.is_subscribed and st.session_state.checkout_step == 'selection':
            data = st.session_state.subscription_data
            st.header(f"Welcome back, {data.get('name', 'User')} 👋")

            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("🛡️ Active Subscription")
                    st.write(f"**Appliance:** {data.get('brand', '')} {data.get('appliance', '')} ({data.get('timeline', '')})")
                    st.write(f"**Contract:** {data.get('duration', '')}")
                    st.write(f"**Valid Until:** :green[{data.get('expiry', '')}]")
                    st.write(f"**Ref ID:** #HMGO-{data.get('order_id', '0000')}")
                with col2:
                    st.metric("Unit Health", "94%", delta="Optimal")
                    st.button("🔧 Request Service", use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Protect Another Appliance"):
                st.session_state.is_subscribed = False
                st.session_state.checkout_step = 'selection'
                st.rerun()

        # VIEW B: CHECKOUT FLOW
        else:
            if st.session_state.checkout_step == 'selection':
                st.markdown("<h3 style='text-align:center;'>Activate a Plan Now</h3><br>", unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                with c1:
                    app_type = st.selectbox("Select Appliance:", ["Air Conditioner (AC)", "Refrigerator", "Washing Machine", "RO Purifier", "Microwave Oven"])
                brands = {
                    "Air Conditioner (AC)": ["Daikin", "Voltas", "LG", "Blue Star", "Samsung"],
                    "Refrigerator": ["Samsung", "LG", "Whirlpool"],
                    "Washing Machine": ["IFB", "LG", "Samsung"],
                    "RO Purifier": ["Kent", "Aquaguard"],
                    "Microwave Oven": ["Samsung", "LG"]
                }
                with c2:
                    brand_name = st.selectbox("Select Brand:", brands[app_type])
                with c3:
                    selected_timeline = st.selectbox("Purchase Year:", ["2000-2005", "2006-2010", "2011-2015", "2016-2020", "2021-Present"], index=3)

                st.markdown("<br>", unsafe_allow_html=True)
                c_dur, c_price = st.columns([2, 1])
                with c_dur:
                    duration = st.radio("Contract Period:", ["6 Months", "9 Months", "1.5 Years", "2 Years", "3 Years"], horizontal=True)

                pricing_matrix = {"Air Conditioner (AC)": 1800, "Refrigerator": 1400, "Washing Machine": 1200, "RO Purifier": 1100, "Microwave Oven": 700}
                age_multiplier = {"2000-2005": 1.6, "2006-2010": 1.4, "2011-2015": 1.2, "2016-2020": 1.0, "2021-Present": 0.9}
                dur_map = {"6 Months": 0.6, "9 Months": 0.8, "1.5 Years": 1.4, "2 Years": 1.8, "3 Years": 2.5}
                final_price = int(pricing_matrix[app_type] * age_multiplier[selected_timeline] * dur_map[duration])

                with c_price:
                    st.metric("Total Payable (Inc. Taxes)", f"₹{final_price}")
                    if st.button("Proceed to Checkout ➔", use_container_width=True):
                        st.session_state.temp_data = {
                            "app": app_type, "brand": brand_name,
                            "timeline": selected_timeline, "price": final_price, "duration": duration
                        }
                        st.session_state.checkout_step = 'details'
                        st.rerun()

            elif st.session_state.checkout_step == 'details':
                st.header("📋 Billing Details")

                # ✅ IMPROVEMENT: Progress indicator
                st.progress(33, text="Step 1 of 3 — Billing Details")

                with st.form("details_form"):
                    u_name = st.text_input("Full Name")
                    u_email = st.text_input("Email Address")
                    u_mobile = st.text_input("Mobile Number")
                    u_addr = st.text_area("Full Address")
                    submitted = st.form_submit_button("Proceed to Payment")
                    if submitted:
                        # ✅ FIX #4: Added email and mobile format validation
                        errors = []
                        if not u_name.strip():
                            errors.append("Name is required.")
                        if not u_email.strip() or "@" not in u_email:
                            errors.append("Valid email is required.")
                        if not u_mobile.strip() or not u_mobile.strip().isdigit() or len(u_mobile.strip()) != 10:
                            errors.append("Valid 10-digit mobile number is required.")
                        if not u_addr.strip():
                            errors.append("Address is required.")
                        if errors:
                            for e in errors:
                                st.error(f"⚠️ {e}")
                        else:
                            st.session_state.temp_name = u_name.strip()
                            st.session_state.checkout_step = 'payment'
                            st.rerun()

                if st.button("← Back"):
                    st.session_state.checkout_step = 'selection'
                    st.rerun()

            elif st.session_state.checkout_step == 'payment':
                st.header("💳 Secure Payment")

                # ✅ IMPROVEMENT: Progress indicator
                st.progress(66, text="Step 2 of 3 — Payment")

                # ✅ FIX #5: Guard against missing temp_data before accessing it
                if not st.session_state.temp_data:
                    st.error("Session expired. Please start again.")
                    if st.button("Start Over"):
                        st.session_state.checkout_step = 'selection'
                        st.rerun()
                else:
                    td = st.session_state.temp_data
                    st.info(f"**Order Summary:** {td.get('brand', '')} {td.get('app', '')} — {td.get('duration', '')} — **₹{td.get('price', 0)}**")
                    st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Homigo", width=150)
                    st.caption("Scan the QR code or click the button below to simulate payment.")

                    col_back, col_pay = st.columns([1, 2])
                    with col_back:
                        if st.button("← Back"):
                            st.session_state.checkout_step = 'details'
                            st.rerun()
                    with col_pay:
                        if st.button("✅ Verify & Pay"):
                            with st.spinner("Processing payment securely..."):
                                time.sleep(1.5)
                            st.session_state.checkout_step = 'success'
                            st.rerun()

            elif st.session_state.checkout_step == 'success':
                # ✅ FIX #6: Guard against missing temp_data on success page (e.g. page refresh)
                if not st.session_state.temp_data or not st.session_state.temp_name:
                    st.error("Session data lost. Please start a new plan.")
                    if st.button("Start Over"):
                        st.session_state.checkout_step = 'selection'
                        st.rerun()
                else:
                    st.balloons()
                    st.success("## ✅ Payment Confirmed!")
                    st.progress(100, text="Step 3 of 3 — Complete")

                    if st.button("Go to Dashboard"):
                        dur_str = st.session_state.temp_data['duration']
                        months_map = {"6 Months": 6, "9 Months": 9, "1.5 Years": 18, "2 Years": 24, "3 Years": 36}
                        now = datetime.now()
                        add_months = months_map.get(dur_str, 12)
                        # ✅ FIX #7: Safer month/year calculation that handles December correctly
                        total_months = now.month - 1 + add_months
                        new_year = now.year + total_months // 12
                        new_month = total_months % 12 + 1
                        # Clamp day to 28 to avoid invalid dates (e.g. Feb 30)
                        expiry_date = now.replace(year=new_year, month=new_month, day=28).strftime("%d %b %Y")

                        st.session_state.is_subscribed = True
                        st.session_state.subscription_data = {
                            "name": st.session_state.temp_name,
                            "appliance": st.session_state.temp_data['app'],
                            "brand": st.session_state.temp_data['brand'],
                            "timeline": st.session_state.temp_data['timeline'],
                            "duration": st.session_state.temp_data['duration'],
                            "expiry": expiry_date,
                            "order_id": np.random.randint(1000, 9999)
                        }
                        st.session_state.checkout_step = 'selection'
                        # Clean up temp data after successful checkout
                        st.session_state.temp_data = {}
                        st.session_state.temp_name = ''
                        st.rerun()


# ----------------------------------------
# PAGE 2: GUARDIAN LIVE FEED
# ----------------------------------------
elif menu == "🛡️ Guardian Live Feed":
    with st.container():
        st.header("🛡️ Guardian Live IoT Monitoring")
        if st.session_state.is_subscribed:
            data = st.session_state.subscription_data
            st.subheader(f"Telemetry Stream: {data.get('brand', '')} {data.get('appliance', '')}")

            m1, m2, m3 = st.columns(3)
            v1 = m1.empty()
            v2 = m2.empty()
            v3 = m3.empty()
            chart_space = st.empty()

            if st.button("▶ Start Live Monitoring"):
                pulse = pd.DataFrame(np.random.randn(20, 1), columns=['Vibration Pulse'])
                # ✅ IMPROVEMENT: Added stop mechanism via session state
                for i in range(30):
                    v = round(0.42 + np.random.normal(0, 0.04), 3)
                    t = round(28.5 + np.random.normal(0, 0.6), 1)
                    c = round(4.8 + np.random.normal(0, 0.1), 2)
                    v1.metric("Vibration (mm/s)", f"{v}")
                    v2.metric("Core Temp (°C)", f"{t}")
                    v3.metric("Current (Amps)", f"{c}")
                    pulse = pd.concat([pulse, pd.DataFrame([[v]], columns=['Vibration Pulse'])], ignore_index=True)
                    chart_space.line_chart(pulse.tail(20))
                    time.sleep(0.4)
                st.success("Monitoring session complete.")
        else:
            st.warning("⚠️ Please activate a Homigo Shield plan to access the Guardian Live Feed.")
            if st.button("Activate a Plan Now"):
                st.session_state['_nav'] = "🏠 Home / AMC Hub"
                st.rerun()


# ----------------------------------------
# PAGE 3: AI DIAGNOSTICS
# ----------------------------------------
elif menu == "📷 AI Diagnostics":
    with st.container():
        st.header("📷 AI Diagnostics")

        # ✅ FIX #8: Show a clear warning if cv2 is not installed
        if not CV2_AVAILABLE:
            st.error("⚠️ OpenCV (cv2) is not installed. Run `pip install opencv-python-headless` to enable AI Diagnostics.")
        else:
            st.write("Scan your appliance components for structural health verification.")
            up = st.file_uploader("Upload Component Image...", type=["jpg", "png", "jpeg"])

            if up:
                # ✅ FIX #9: Read file bytes once and reuse — calling .read() twice returns empty on second call
                file_bytes = up.read()
                img = cv2.imdecode(np.asarray(bytearray(file_bytes), dtype=np.uint8), 1)

                # ✅ FIX #10: Guard against corrupt/unreadable image files
                if img is None:
                    st.error("Could not decode the image. Please upload a valid JPG or PNG file.")
                else:
                    with st.spinner("AI analyzing structural patterns..."):
                        time.sleep(1.2)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        edges = cv2.Canny(gray, 100, 200)
                        density = np.sum(edges == 255) / edges.size

                    c1, c2 = st.columns(2)
                    c1.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Input Feed", use_container_width=True)
                    c2.image(edges, caption="AI Edge Mapping", use_container_width=True)

                    st.markdown("### 🔍 Homigo Diagnostic Report")
                    if density > 0.05:
                        st.error("**Finding: CRITICAL FAULT DETECTED**")
                        st.markdown("1. **Immediate Shutdown Required.**\n2. **Technician Visit:** Covered under your Shield plan.")
                        with st.form("service_booking"):
                            day = st.selectbox("Preferred Day:", ["Today", "Tomorrow", "Monday", "Tuesday", "Wednesday"])
                            slot = st.selectbox("Time Slot:", ["Morning (9AM–12PM)", "Afternoon (12PM–4PM)", "Evening (4PM–8PM)"])
                            if st.form_submit_button("Confirm & Book Technician"):
                                st.success(f"✅ Technician booked for **{day}** — **{slot}**!")
                    else:
                        st.success("**Finding: HEALTHY COMPONENT**")
                        st.info("No structural anomalies detected. Your component appears to be in good condition.")

                    confidence = round(min(99.9, 92 + (density * 10)), 2)
                    st.metric("AI Confidence", f"{confidence}%")


# --- COMMON FOOTER ---
st.markdown("""
    <div class="custom-footer">
        <div class="footer-grid">
            <div class="footer-brand">
                <h2>Homigo<span>●</span></h2>
                <p>Expert Care For Your Devices.</p>
                <p style="font-size: 20px;">📘 𝕏 📸 📺</p>
            </div>
            <div class="footer-cols">
                <div class="footer-col">
                    <h4>Company</h4>
                    <ul>
                        <li><a>About Us</a></li>
                        <li><a>Blog</a></li>
                        <li><a>Careers</a></li>
                        <li><a>In The Media</a></li>
                        <li><a>Contact Us</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Products</h4>
                    <ul>
                        <li><a>Mobile Phones</a></li>
                        <li><a>Air Conditioners</a></li>
                        <li><a>Laptops</a></li>
                        <li><a>Washing Machine</a></li>
                        <li><a>Refrigerators</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Policies</h4>
                    <ul>
                        <li><a>Terms of Use</a></li>
                        <li><a>Privacy Policy</a></li>
                        <li><a>Terms of Service</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Warranty Check</h4>
                    <ul>
                        <li><a>Apple Warranty Check</a></li>
                        <li><a>Sony Warranty Check</a></li>
                        <li><a>Samsung Warranty Check</a></li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <div>Secure Payment: 💳 VISA | MasterCard | AMEX | Net Banking</div>
            <div>2010-2026 © Homigo. All Rights Reserved</div>
        </div>
    </div>
""", unsafe_allow_html=True)
