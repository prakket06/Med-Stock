from datetime import datetime

import streamlit as st
from Logic import check_med, view_stock, add_med, remove_med, update_stock, check_expiry, get_whatsapp_link, reduce_stock

st.set_page_config(page_title = "Medicine Stock App", page_icon = "💊", layout = "wide", initial_sidebar_state = "expanded")

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

    html, body {
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

    /* 3. TABS STYLING */
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #FF9900 !important;
        border-bottom: 2px solid #FF9900 !important;
        font-family: 'Michroma', sans-serif !important;
        font-size: 0.85rem !important;
    }

    .stTabs button {
        color: #94A3B8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600;
    }

    /* 4. TEXT INPUTS & NUMBER INPUTS (CLEAN NEBULA BORDER) */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input {
        background-color: #0B0E14 !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus {
        border-color: #00F0FF !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4) !important;
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

    /* ---------------- ALERT BOXES (NEBULA SHADES & GLOW) ---------------- */

    /* Base Alert Box Styling */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        padding: 12px 18px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    /* 1. SUCCESS (Green Box & Bright Green Text) */
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentSuccess"]),
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconSuccess"]) {
        background-color: rgba(6, 78, 59, 0.45) !important;
        border: 1px solid #059669 !important;
        box-shadow: 0 4px 20px rgba(5, 150, 105, 0.25) !important;
    }
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentSuccess"]) p,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconSuccess"]) p,
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentSuccess"]) svg,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconSuccess"]) svg {
        color: #34D399 !important;
        fill: #34D399 !important;
    }

    /* 2. WARNING (Amber/Gold Box & Gold Text) */
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentWarning"]),
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconWarning"]) {
        background-color: rgba(120, 53, 15, 0.45) !important;
        border: 1px solid #D97706 !important;
        box-shadow: 0 4px 20px rgba(217, 119, 6, 0.25) !important;
    }
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentWarning"]) p,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconWarning"]) p,
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentWarning"]) svg,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconWarning"]) svg {
        color: #FBBF24 !important;
        fill: #FBBF24 !important;
    }

    /* 3. ERROR (Crimson Box & Soft Red Text) */
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentError"]),
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconError"]) {
        background-color: rgba(127, 29, 29, 0.45) !important;
        border: 1px solid #DC2626 !important;
        box-shadow: 0 4px 20px rgba(220, 38, 38, 0.25) !important;
    }
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentError"]) p,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconError"]) p,
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentError"]) svg,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconError"]) svg {
        color: #FCA5A5 !important;
        fill: #FCA5A5 !important;
    }

    /* 4. INFO (Deep Cyan Box & Bright Cyan Text) */
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentInfo"]),
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconInfo"]) {
        background-color: rgba(22, 78, 99, 0.45) !important;
        border: 1px solid #0891B2 !important;
        box-shadow: 0 4px 20px rgba(8, 145, 178, 0.25) !important;
    }
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentInfo"]) p,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconInfo"]) p,
    div[data-testid="stAlert"]:has(div[data-testid="stAlertContentInfo"]) svg,
    div[data-testid="stAlert"]:has(svg[data-testid="stNotificationIconInfo"]) svg {
        color: #22D3EE !important;
        fill: #22D3EE !important;
    }

    /* Code block inside Alert styling */
    div[data-testid="stAlert"] code {
        background-color: rgba(3, 7, 18, 0.7) !important;
        border-radius: 4px;
        padding: 0.15rem 0.4rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("💊 Medicine Stock App")
st.sidebar.markdown("Should the daily stock be reduced right now?")
if st.sidebar.button("Yes, Reduce Stock", type = "primary"):
    st.sidebar.success("Stock reduced successfully!")
    # Call the reduce_stock function from Logic.py
    reduce_stock()
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["View Stock", "Add Medicine", "Remove Medicine", "Update Stock", "Skipped Medicines","Send Message"])

with tab1:
    st.header("View Stock")
    st.dataframe(view_stock(), width = "stretch", hide_index = True)
    st.subheader("📋 Medicines that are expired or expiring soon:")
    if check_expiry() is not None:
        expired_meds, expiring_in_10_days, expiring_in_30_days = check_expiry()
        if expired_meds is not None and len(expired_meds) > 0:
            st.error("Expired Medicines:")
            st.write(expired_meds)
        if expiring_in_10_days is not None and len(expiring_in_10_days) > 0:
            st.warning("Expiring in 10 Days:")
            st.write(expiring_in_10_days)
        if expiring_in_30_days is not None and len(expiring_in_30_days) > 0:
            st.info("Expiring in 30 Days:")
            st.write(expiring_in_30_days)
    else:
        st.success("No medicines expired or expiring soon.", icon = "🟢")

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
                        st.success(f"{med_name} added successfully!", icon = "🟢")
                        st.session_state.add_med = False
                    else:
                        st.error(f"Failed to add {med_name}.", icon = "🔴")
                else:
                    st.warning("Please fill in all the fields correctly.", icon = "🟡")
        else:
            st.info(f"{med_name} already exists in stock. Please use the Update Stock tab to modify it.", icon = "ℹ️")

with tab3:
    st.header("Remove Medicine")
    df = view_stock()
    med_list = df["Name"].tolist()
    med_name_remove = st.multiselect("Select the medicine(s) to remove:", options=med_list, placeholder="Select medicine(s)...")

    if med_name_remove:
        if st.button("Confirm Remove", type = "primary"):
            for med_name in med_name_remove:
                remove_successful = remove_med(med_name)
                if remove_successful:
                    st.success(f"{med_name} removed successfully!", icon = "🟢")
                else:
                    st.error(f"Failed to remove {med_name}.", icon = "🔴")

with tab4:
    st.header("Update Stock")
    df = view_stock()
    med_list = df["Name"].tolist()
    update_data = {}
    # 1. Select kon-kon si medicines miss hui
    med_name_update = st.multiselect(
        "Select medicines to update:",
        options=med_list,
        placeholder="Select medicines..."
    )

    if med_name_update:
        st.subheader("📋 Update Stock")
        update_data = {}

        # 2. Selected medicines ke liye dynamic input fields
        cols = st.columns(len(med_name_update)) if len(med_name_update) <= 3 else [st.container()]
        
        # Grid layout for inputs
        for idx, med_name in enumerate(med_name_update):
            # Fetch default dose for this med
            tablets_left = float(df.loc[df["Name"] == med_name, "Tablets Left"].values[0])
            dose = float(df.loc[df["Name"] == med_name, "Dose"].values[0])

            with st.container(border=True):
                st.write(f"**{med_name}**")
                tablets_bought = st.number_input(f"No. of tablets bought: ({med_name})", min_value=0.001, value = tablets_left, step=0.5, key=f"buy_{med_name}")
                new_dose = st.number_input(f"New Dose of Medicine (minimum 0.001): ({med_name})", min_value=0.001, value=dose, step=0.001, key=f"dose_{med_name}")
                new_expiry = st.date_input(f"New Expiry Date: ({med_name})", min_value = datetime.now().date(), key=f"expiry_{med_name}")
                update_data[med_name] = [tablets_bought, new_dose, new_expiry]

        # 3. Confirm Button
        if st.button("Update Stock", type="primary"):
            for med_name, qty in update_data.items():
                # Stock me quantity add back karne ka logic
                current_tablets = df.loc[df["Name"] == med_name, "Tablets Left"].values[0]
                current_dose = df.loc[df["Name"] == med_name, "Dose"].values[0]
                current_expiry = datetime.strptime(df.loc[df["Name"] == med_name, "Expiry Date"].values[0], "%d-%m-%y")
                
                new_tablets = current_tablets + qty[0]
                new_days = new_tablets / qty[1]
                
                update_stock(med_name, new_tablets, new_days, qty[1], qty[2])
                
            st.success("Stock updated successfully! 🎉", icon = "🟢")
    else:
        st.info("No medicines selected for update.", icon = "ℹ️")

with tab5:
    st.header("Skipped Medicines")

    df = view_stock()
    med_list = df["Name"].tolist()

    # 1. Select kon-kon si medicines miss hui
    selected_skipped_meds = st.multiselect(
        "Skipped medicines?",
        options=med_list,
        placeholder="Select skipped medicines..."
    )

    if selected_skipped_meds:
        st.subheader("📋 Missed Doses Adjustment")
        skipped_data = {}

        # 2. Selected medicines ke liye dynamic input fields
        cols = st.columns(len(selected_skipped_meds)) if len(selected_skipped_meds) <= 3 else [st.container()]
        
        # Grid layout for inputs
        for idx, med_name in enumerate(selected_skipped_meds):
            # Fetch default dose for this med
            default_dose = float(df.loc[df["Name"] == med_name, "Dose"].values[0])
            
            with st.container(border=True):
                st.write(f"**{med_name}**")
                tablets_skipped = st.number_input(f"No. of tablets skipped: ({med_name})", min_value=0.001, value=default_dose, step=0.5, key=f"skip_{med_name}")
                skipped_data[med_name] = tablets_skipped

        # 3. Confirm Button
        if st.button("Log Skipped Doses (Add Back to Stock)", type="primary"):
            for med_name, qty in skipped_data.items():
                # Stock me quantity add back karne ka logic
                current_tablets = df.loc[df["Name"] == med_name, "Tablets Left"].values[0]
                current_dose = df.loc[df["Name"] == med_name, "Dose"].values[0]
                current_expiry = datetime.strptime(df.loc[df["Name"] == med_name, "Expiry Date"].values[0], "%d-%m-%y")
                
                new_tablets = current_tablets + qty
                new_days = new_tablets / current_dose
                
                update_stock(med_name, new_tablets, new_days, current_dose, current_expiry)
                
            st.success("Skipped doses added back to stock! 🎉", icon = "🟢")
    else:
        st.info("No skipped medicines selected.", icon = "ℹ️")

with tab6:
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
        st.success("🎉 All medicines have sufficient stock! No refill needed right now.", icon = "🟢")