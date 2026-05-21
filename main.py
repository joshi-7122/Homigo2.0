import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="Homigo UI", page_icon="🔧", layout="wide")

# --- 1. Navigation Bar (Using HTML/CSS for the exact teal replica) ---
st.markdown("""
    <style>
    .navbar {
        background-color: #169ba6;
        padding: 15px 40px;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 40px;
    }
    .logo { font-size: 26px; font-weight: bold; }
    .logo span { color: #ffc107; }
    .links { display: flex; gap: 20px; align-items: center; font-size: 14px;}
    .sign-in { background: white; color: #169ba6; padding: 8px 15px; border-radius: 20px; font-weight: bold; }
    </style>
    <div class="navbar">
        <div class="logo">onsite<span>go</span></div>
        <div class="links">
            <span>Device & Plans</span>
            <span>Activate Plan</span>
            <span>Track Service Request</span>
            <span class="sign-in">Sign In</span>
            <span>🛒</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. AI Predictive Diagnostics ---
st.markdown("<h2 style='text-align: center;'>AI Predictive Diagnostics</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; margin-bottom: 30px;'>Identify the likely issue before the technician even arrives.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    appliance = st.selectbox("Select Appliance", ["AC", "Washing Machine", "Water Purifier"])
with col2:
    symptom = st.selectbox("Primary Symptom", ["Not Cooling", "Making Noise", "Won't Turn On", "Leaking Water"])

# Streamlit makes button logic incredibly easy
if st.button("Run AI Analysis", type="primary", use_container_width=True):
    if appliance == "AC" and symptom == "Not Cooling":
        st.error("Prediction: 85% chance of Low Refrigerant/Gas Leak. Recommended Action: Dispatch tech with R32 Gas cylinder.")
    elif appliance == "Washing Machine" and symptom == "Making Noise":
        st.warning("Prediction: 90% chance of Worn Drum Bearings. Recommended Action: Dispatch tech with replacement bearing kit.")
    else:
        st.info(f"Analyzing {appliance} for '{symptom}'... (ML Model needs more data)")

st.divider()

# --- 3. Testimonials Section ---
st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>What our customers say</h3>", unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.info("**Snehan P Rajan** (Mumbai)  \n⭐⭐⭐⭐⭐  \n*\"A friend recommended your InstaRepair service so I booked a service online for my water purifier and it was a good experience. Service was cashless and convenient.\"*")
with t2:
    st.info("**Shivani Choudhary** (New Delhi)  \n⭐⭐⭐⭐⭐  \n*\"Good service. Your technician came with all tools and followed safety norms. He was polite and professional.\"*")

st.divider()

# --- 4. Aggregate Ratings ---
r1, r2, r3 = st.columns(3)
r1.metric(label="Amazon Rating", value="4.5 ★", delta="6,000+ Reviews", delta_color="off")
r2.metric(label="Facebook Rating", value="4.5 ★", delta="1,500+ Reviews", delta_color="off")
r3.metric(label="Google Rating", value="4.5 ★", delta="2,200+ Reviews", delta_color="off")

st.divider()

# --- 5. Partners Section ---
st.markdown("<h4 style='text-align: center; color: #169ba6;'>SPOTLIGHT</h4>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Our Partners</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555; padding-top: 20px;'>Amazon &nbsp; | &nbsp; Croma &nbsp; | &nbsp; Vijay Sales &nbsp; | &nbsp; ICICI Bank &nbsp; | &nbsp; Delta</h4>", unsafe_allow_html=True)
