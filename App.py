from datetime import datetime

import streamlit as st
from Logic import check_med, view_stock, add_med, remove_med, update_stock, check_expiry, get_whatsapp_link

st.set_page_config(page_title = "Medicine Stock App", page_icon = "💊", layout = "wide")

st.markdown(
    """
    <style>
    /* 1. KEYFRAMES FOR COSMIC ANIMATIONS */
    @keyframes accretionSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes cosmicPulse {
        0% { box-shadow: 0 0 8px rgba(255, 153, 0, 0.3), 0 0 15px rgba(255, 85, 0, 0.2); }
        50% { box-shadow: 0 0 25px rgba(255, 153, 0, 0.8), 0 0 45px rgba(255, 85, 0, 0.5); }
        100% { box-shadow: 0 0 8px rgba(255, 153, 0, 0.3), 0 0 15px rgba(255, 85, 0, 0.2); }
    }

    /* 2. NEBULA BACKGROUND & GLOBAL FONTS */
    .stApp {
        background: 
            radial-gradient(circle at 15% 20%, rgba(147, 51, 234, 0.18) 0%, transparent 45%),
            radial-gradient(circle at 85% 75%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(14, 165, 233, 0.12) 0%, transparent 60%),
            #030712 !important;
        background-attachment: fixed !important;
    }

    html, body, [class*="st-"] {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #E2E8F0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Michroma', sans-serif !important;
        letter-spacing: -0.5px;
        color: #F8FAFC !important;
        text-shadow: 0 0 12px rgba(168, 85, 247, 0.4);
    }

    code, pre, [data-testid="stCodeBlock"] {
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* 3. TABS STYLING (GLASSMORPHISM NEBULA LOOK) */
    .stTabs [aria-selected="true"] {
        background: rgba(15, 23, 42, 0.75) !important;
        color: #FF9900 !important;
        border-bottom: 2px solid #FF9900 !important;
        font-family: 'Michroma', sans-serif !important;
        font-size: 0.85rem !important;
        backdrop-filter: blur(8px);
    }

    .stTabs button {
        color: #94A3B8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600;
    }

    /* 4. TEXT INPUTS & CARDS (GLASSMORPHISM CARDS) */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        background-color: rgba(11, 14, 20, 0.0) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 8px !important;
        backdrop-filter: blur(6px) !important;
    }

    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus {
        border-color: #00F0FF !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4) !important;
    }

    /* 5. PRIMARY BUTTON (ACCRETION DISK ROTATION HOVER) */
    div.stButton > button[kind="primary"] {
        position: relative !important;
        background: #0B0E14 !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255, 153, 0, 0.4) !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.6rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    div.stButton > button[kind="primary"]::before {
        content: "";
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(from 0deg, transparent 0%, #FF9900 25%, transparent 50%, #00F0FF 75%, transparent 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
        pointer-events: none;
        z-index: 0;
    }

    div.stButton > button[kind="primary"]::after {
        content: "";
        position: absolute;
        inset: 2px;
        background: #0B0E14;
        border-radius: 6px;
        z-index: 1;
        transition: background 0.3s ease;
    }

    div.stButton > button[kind="primary"] p {
        position: relative !important;
        z-index: 2 !important;
        color: #E2E8F0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    div.stButton > button[kind="primary"]:hover {
        border-color: #FF9900 !important;
        animation: cosmicPulse 1.5s infinite alternate ease-in-out !important;
        transform: translateY(-2px) scale(1.02) !important;
    }

    div.stButton > button[kind="primary"]:hover::before {
        opacity: 1;
        animation: accretionSpin 3s linear infinite;
    }

    div.stButton > button[kind="primary"]:hover::after {
        background: #05070A;
    }

    div.stButton > button[kind="primary"]:hover p {
        color: #FFFFFF !important;
        text-shadow: 0 0 10px #00F0FF, 0 0 20px #FF9900 !important;
    }

    /* 6. WHATSAPP LINK BUTTON */
    div.stLinkButton > a {
        background: linear-gradient(135deg, #FF9900 0%, #FF5500 100%) !important;
        color: #030712 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }

    div.stLinkButton > a:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(255, 153, 0, 0.6) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["View Stock", "Add Medicine", "Remove Medicine", "Update Stock", "Send Message"])

with tab1:
    st.header("View Stock")
    st.dataframe(view_stock(), width = "stretch", hide_index = True)
    st.subheader("📋 Medicines that are expired:")
    if check_expiry() is not None:
        expired_meds, expiring_in_10_days, expiring_in_30_days = check_expiry()
        if expired_meds is not None and len(expired_meds) > 0:
            st.write("Expired Medicines:")
            st.write(expired_meds)
        if expiring_in_10_days is not None and len(expiring_in_10_days) > 0:
            st.write("Expiring in 10 Days:")
            st.write(expiring_in_10_days)
        if expiring_in_30_days is not None and len(expiring_in_30_days) > 0:
            st.write("Expiring in 30 Days:")
            st.write(expiring_in_30_days)
    else:
        st.success("No medicines expired or expiring soon.")

with tab2:
    st.header("Add Medicine")

    if "add_med" not in st.session_state:
        st.session_state.add_med = False

    med_name = st.text_input("Enter the name of the medicine:")

    if st.button("Add New Medicine", type = "primary"):
        st.session_state.add_med = True

    if st.session_state.add_med and med_name:
        if not check_med(med_name): 
            col1, col2, col3 = st.columns(3)
            with col1:
                med_tablets = st.number_input("Number of Tablets:", min_value=0.0, step=0.5)
            with col2:
                med_dose = st.number_input("Dose of Medicine (minimum 0.001):", min_value=0.001, step=0.001)
            with col3:
                med_expiry = st.date_input("Expiry Date:", min_value = datetime.now().date())
            med_days = med_tablets / med_dose
            if st.button("Confirm Add", type = "primary"):
                if med_name and med_tablets and med_dose > 0 and med_expiry:
                    med_added = add_med(med_name, med_tablets, med_dose, med_days, med_expiry)
                    if med_added:
                        st.success(f"{med_name} added successfully!")
                        st.session_state.add_med = False
                    else:
                        st.error(f"Failed to add {med_name}.")
                else:
                    st.warning("Please fill in all the fields correctly.")
        else:
            st.warning(f"{med_name} already exists in stock. Please use the Update Stock tab to modify it.")

with tab3:
    st.header("Remove Medicine")
    med_name_remove = st.text_input("Enter the name of the medicine to remove:")
    if st.button("Remove Medicine", type = "primary"):
        if med_name_remove:
            if check_med(med_name_remove):
                med_removed = remove_med(med_name_remove)
                if med_removed == True:
                    st.success(f"{med_name_remove} removed successfully!")
                else:
                    st.error(med_removed)
            else:
                st.warning(f"{med_name_remove} not found in stock.")
        else:
            st.warning("Please enter the name of the medicine to remove.")

with tab4:
    st.header("Update Stock")

    if "update_med" not in st.session_state:
        st.session_state.update_med = False

    df = view_stock()
    med_name_update = st.text_input("Enter the name of the medicine to update:")

    if st.button("Search Medicine", type = "primary"):
        if med_name_update:
            st.session_state.update_med = True
        else:
            st.warning("Please enter the name of the medicine to search.")

    if st.session_state.update_med and med_name_update:
        if check_med(med_name_update):
            col1, col2, col3 = st.columns(3)
            with col1:
                new_tablets = st.number_input("Number of Tablets You Bought:", min_value=0.0, step=0.5)
            with col2:
                new_dose = st.number_input("New Dose of Medicine (minimum 0.001):", min_value=0.001, step=0.001)
            with col3:
                new_expiry = st.date_input("New Expiry Date:", min_value = datetime.now().date())

            new_tablets += df.loc[df["Name"] == med_name_update, "Tablets Left"].values[0]

            if st.button("Confirm Update", type = "primary"):
                if new_tablets > 0 and new_dose > 0 and new_expiry:
                    new_days = new_tablets / new_dose
                    update_successful = update_stock(med_name_update, new_tablets, new_days, new_dose, new_expiry)
                    if update_successful:
                        st.success(f"{med_name_update} updated successfully!")
                        st.session_state.update_med = False  # Reset state after update
                    else:
                        st.error(f"Failed to update {med_name_update}.")
                else:
                    st.warning("Please fill in all the fields correctly.")
        else:
            st.warning(f"'{med_name_update}' not found in stock.")

with tab5:
    st.header("📨 Send Refill Reminder to Mummy")
    st.markdown("Automated trigger to send low stock medicine list via WhatsApp.")
    
    phone_input = st.text_input("Enter Mummy's WhatsApp Number (with country code, e.g. +91XXXXXXXXXX):", value="+91")
    
    link, msg_summary = get_whatsapp_link(phone_input)
    
    if link:
        st.subheader("📋 Low Stock Summary:")
        st.code(msg_summary, language="markdown")
        
        # Link button to open WhatsApp directly with pre-filled text
        st.link_button("🟢 Open WhatsApp & Send Message", link, width = "stretch")
    else:
        st.success("🎉 All medicines have sufficient stock! No refill needed right now.")