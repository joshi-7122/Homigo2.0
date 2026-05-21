import streamlit as st
import cv2
import numpy as np
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SESSION STATE INITIALIZATION ---
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 'selection'
if 'subscription_data' not in st.session_state:
    st.session_state.subscription_data = {}

st.set_page_config(page_title="Homigo | Smart Hub", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM UI INJECTION (CSS for Header, Grid, Hover Effects, and Footer) ---
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; max-width: 100%; padding-left: 0; padding-right: 0;}
        
        /* Navbar (Matches Image 1) */
        .navbar {
            background-color: #4a148c; 
            padding: 15px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
        
        /* Hero Section */
        .hero {
            background-color: #6a1b9a; 
            padding: 60px 20px;
            text-align: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .hero h1 { font-weight: 300; margin-bottom: 10px; color: white; font-size: 30px; line-height: 1.2; }
        .hero .highlight { color: #ffab40; font-size: 56px; font-weight: 900; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; } 
        .hero h2 { color: white; font-size: 26px; font-weight: 500; }
        
        /* Explore Our Services Grid */
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
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .service-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
        }
        /* Realistic Image Circles with Hover Pop-up */
        .img-circle {
            width: 110px; height: 110px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            border: 3px solid #f3e5f5;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s, box-shadow 0.3s;
        }
        .service-card:hover .img-circle {
            transform: scale(1.15) translateY(-8px); /* Pop up effect */
            border-color: #ffab40;
            box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        }
        .card-label { color: #333; font-size: 15px; font-weight: 600; transition: color 0.3s; }
        .service-card:hover .card-label { color: #6a1b9a; }

        /* Footer (Matches Image 2) */
        .custom-footer {
            background-color: #161619;
            color: #a0a0a0;
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

        /* Streamlit Content Container Padding */
        .st-emotion-cache-1jicfl2 { padding: 0 5%; }
        
        div.stButton > button:first-child {
            background-color: #6a1b9a; color: white; border: none; font-weight: bold; padding: 12px 28px; border-radius: 8px; font-size: 16px; 
        }
        div.stButton > button:hover { background-color: #4a148c; color: #ffab40; }
    </style>
""", unsafe_allow_html=True)


# --- 2. SIDEBAR STATUS & NAVIGATION ---
st.sidebar.title("🏠 Homigo")
if st.session_state.is_subscribed:
    st.sidebar.success(f"🛡️ Shield Active: {st.session_state.subscription_data['brand']} {st.session_state.subscription_data['appliance']}")
else:
    st.sidebar.warning("🛡️ Status: No Active Plan")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["🏠 Home / AMC Hub", "🛡️ Guardian Live Feed", "📷 AI Diagnostics"])


# ----------------------------------------
# PAGE 1: HOME / AMC HUB
# ----------------------------------------
if menu == "🏠 Home / AMC Hub":
    
    # --- RENDER THE HEADER, HERO & SERVICES GRID ---
    st.markdown("""
        <div class="navbar">
            <div class="nav-logo">Homigo<span>●</span></div>
            <div class="nav-right">
                <a href="#" class="nav-link">Device & Plans</a>
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
            <h1>Say goodbye to unexpected repair costs with</h1>
            <div class="highlight">Homigo Shield</div>
            <h2>Premier Care For Your Home Devices</h2>
        </div>

        <div class="services-section">
            <h2>Explore Our Services</h2>
            <div class="grid-container">
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1610552050890-fe99536c2615?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Air Conditioner</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Television</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Mobile Phone</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Refrigerator</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Washing Machine</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1585659722983-3a6750f2fd82?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Microwave</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Printer</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Audio System</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Laptop</div>
                </div>
                <div class="service-card">
                    <img src="https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=200&q=80" class="img-circle">
                    <div class="card-label">Digital Camera</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)
    
    # We wrap the Streamlit logic in a container to respect margins
    with st.container():
        # VIEW A: DASHBOARD (Shown after purchase)
        if st.session_state.is_subscribed and st.session_state.checkout_step == 'selection':
            data = st.session_state.subscription_data
            st.header(f"Welcome back, {data['name']} 👋")
            
            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("🛡️ Active Subscription")
                    st.write(f"**Appliance:** {data['brand']} {data['appliance']} ({data['timeline']})")
                    st.write(f"**Contract:** {data['duration']}")
                    st.write(f"**Valid Until:** :green[{data['expiry']}]") 
                    st.write(f"**Ref ID:** #HMGO-{data['order_id']}")
                with col2:
                    st.metric("Unit Health", "94%", delta="Optimal")
                    st.button("🔧 Request Service", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Protect Another Appliance"):
                st.session_state.is_subscribed = False
                st.session_state.checkout_step = 'selection'
                st.rerun()

        # VIEW B: THE CHECKOUT FLOW
        else:
            if st.session_state.checkout_step == 'selection':
                st.markdown("<h3 style='text-align:center;'>Activate a Plan Now</h3><br>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    app_type = st.selectbox("Select Appliance:", ["Air Conditioner (AC)", "Refrigerator", "Washing Machine", "RO Purifier", "Microwave Oven"])
                brands = {"Air Conditioner (AC)": ["Daikin", "Voltas", "LG", "Blue Star", "Samsung"], "Refrigerator": ["Samsung", "LG", "Whirlpool"], "Washing Machine": ["IFB", "LG", "Samsung"], "RO Purifier": ["Kent", "Aquaguard"], "Microwave Oven": ["Samsung", "LG"]}
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
                        st.session_state.temp_data = {"app": app_type, "brand": brand_name, "timeline": selected_timeline, "price": final_price, "duration": duration}
                        st.session_state.checkout_step = 'details'
                        st.rerun()

            elif st.session_state.checkout_step == 'details':
                st.header("📋 Billing Details")
                with st.form("details_form"):
                    u_name = st.text_input("Name")
                    u_email = st.text_input("Email")
                    u_mobile = st.text_input("Mobile")
                    u_addr = st.text_area("Address")
                    if st.form_submit_button("Proceed to Payment"):
                        if u_name and u_email and u_mobile and u_addr:
                            st.session_state.temp_name = u_name
                            st.session_state.checkout_step = 'payment'
                            st.rerun()
                        else:
                            st.error("⚠️ All fields are mandatory to proceed.")

            elif st.session_state.checkout_step == 'payment':
                st.header("💳 Secure Payment")
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Homigo", width=150)
                if st.button("Verify & Pay"):
                    with st.spinner("Processing..."): 
                        time.sleep(1)
                    st.session_state.checkout_step = 'success'
                    st.rerun()

            elif st.session_state.checkout_step == 'success':
                st.balloons()
                st.header("✅ Payment Confirmed")
                if st.button("Go to Dashboard"):
                    dur_str = st.session_state.temp_data['duration']
                    months_map = {"6 Months": 6, "9 Months": 9, "1.5 Years": 18, "2 Years": 24, "3 Years": 36}
                    now = datetime.now()
                    add_months = months_map[dur_str]
                    new_month = (now.month + add_months - 1) % 12 + 1
                    new_year = now.year + (now.month + add_months - 1) // 12
                    expiry_date = now.replace(year=new_year, month=new_month, day=28).strftime("%d %b %Y")
                    
                    st.session_state.is_subscribed = True
                    st.session_state.subscription_data = {
                        "name": st.session_state.temp_name, "appliance": st.session_state.temp_data['app'], 
                        "brand": st.session_state.temp_data['brand'], "timeline": st.session_state.temp_data['timeline'], 
                        "duration": st.session_state.temp_data['duration'], "expiry": expiry_date, "order_id": np.random.randint(1000, 9999)
                    }
                    st.session_state.checkout_step = 'selection'
                    st.rerun()

# ----------------------------------------
# PAGE 2 & 3: (IoT & AI Logic)
# ----------------------------------------
elif menu == "🛡️ Guardian Live Feed":
    with st.container():
        st.header("🛡️ Guardian Live IoT Monitoring")
        if st.session_state.is_subscribed:
            data = st.session_state.subscription_data
            st.subheader(f"Telemetry Stream: {data['brand']} {data['appliance']}")
            m1, m2, m3 = st.columns(3)
            v1 = m1.empty(); v2 = m2.empty(); v3 = m3.empty()
            chart_space = st.empty()
            
            if st.button("Start Live Monitoring"):
                pulse = pd.DataFrame(np.random.randn(20, 1), columns=['Vibration Pulse'])
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
        else:
            st.warning("Please activate a Homigo Shield to access the Guardian Live Feed.")

elif menu == "📷 AI Diagnostics":
    with st.container():
        st.header("📷 AI Diagnostics")
        st.write("Scan your appliance components for structural health verification.")
        up = st.file_uploader("Upload Component Image...", type=["jpg", "png", "jpeg"])
        
        if up:
            img = cv2.imdecode(np.asarray(bytearray(up.read()), dtype=np.uint8), 1)
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
                st.markdown("1. **Immediate Shutdown Required.**\n2. **Technician Visit:** Covered under Shield.")
                with st.form("service_booking"):
                    day = st.selectbox("Select Preferred Day:", ["Today", "Tomorrow", "Monday", "Tuesday"])
                    slot = st.selectbox("Select Time Slot:", ["Morning", "Afternoon", "Evening"])
                    if st.form_submit_button("Confirm Slot & Book Technician"):
                        st.success(f"✅ Technician Booked for {day} during the {slot}!")
            else:
                st.success("**Finding: HEALTHY COMPONENT**")
            st.metric("AI Confidence", f"{round(92 + (density * 10), 2)}%")


# --- COMMON FOOTER (Appears on all pages at the bottom) ---
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
            <div>Secure Payment: 💳 VISA | MasterCard | AMEX | Net Banking </div>
            <div>2010-2026 © Homigo. All Rights Reserved</div>
        </div>
    </div>
""", unsafe_allow_html=True)
