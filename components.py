import streamlit as st

def render_navbar():
    st.markdown("""
        <div class="navbar">
            <div class="nav-logo">Homigo<span>●</span></div>
            <div class="nav-right">
                <div class="nav-item-dropdown">
                    <a class="nav-link" style="color:white; cursor:pointer;">Device & Plans ▾</a>
                    <div class="mega-menu">
                        <div class="mega-col">
                            <span class="mega-title">Air Conditioner</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Refrigerator</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Television</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                        </div>
                        <div class="mega-col">
                            <span class="mega-title">Mobile Phone</span>
                            <a href="#" class="mega-link">Request Service</a>
                            <a href="#" class="mega-link">AMC Plans</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_action_blocks():
    st.markdown("""
        <div class="action-blocks-row">
            <div class="action-block">
                <div class="action-block-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
                </div>
                <div class="action-block-label">SERVICE REQUEST</div>
            </div>
            <div class="action-block">
                <div class="action-block-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4l3 3"></path></svg>
                </div>
                <div class="action-block-label">ACTIVATE PLAN</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
