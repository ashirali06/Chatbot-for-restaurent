import streamlit as st
from data import DataManager

def render_admin_panel():
    st.header("Admin Panel")
    
    data_manager = DataManager()
    config = data_manager.get_config()

    # Password Protection
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == config.get("admin_password"):
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return

    # Admin Tabs
    tab1, tab2, tab3 = st.tabs(["Menu Management", "FAQ Management", "Settings"])

    # --- MENU MANAGEMENT ---
    with tab1:
        st.subheader("Edit Menu")
        menu = data_manager.get_menu()
        
        # Add New Category
        with st.expander("Add New Category"):
            new_cat = st.text_input("Category Name")
            if st.button("Add Category"):
                if new_cat and new_cat not in menu:
                    menu[new_cat] = []
                    data_manager.save_menu(menu)
                    st.success(f"Category '{new_cat}' added.")
                    st.rerun()
        
        # Edit Items per Category
        for category, items in menu.items():
            st.write(f"### {category}")
            
            # Delete Category Button
            if st.button(f"Delete Category: {category}", key=f"del_cat_{category}"):
                del menu[category]
                data_manager.save_menu(menu)
                st.rerun()

            # Add Item to Category
            with st.expander(f"Add Item to {category}"):
                with st.form(f"add_item_{category}"):
                    name = st.text_input("Item Name")
                    price = st.number_input("Price", min_value=0.0)
                    desc = st.text_input("Description")
                    submitted = st.form_submit_button("Add Item")
                    if submitted:
                        items.append({
                            "name": name, 
                            "price": price, 
                            "description": desc,
                            "available": True
                        })
                        data_manager.save_menu(menu)
                        st.success("Item added!")
                        st.rerun()

            # List Items (Simple Delete for MVP)
            for i, item in enumerate(items):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                col1.text(f"{item['name']} - ${item['price']}")
                if col4.button("Delete", key=f"del_{category}_{i}"):
                    items.pop(i)
                    data_manager.save_menu(menu)
                    st.rerun()

    # --- FAQ MANAGEMENT ---
    with tab2:
        st.subheader("Edit FAQs")
        faq = data_manager.get_faq()

        # Add New FAQ
        with st.expander("Add New FAQ"):
            with st.form("new_faq"):
                key = st.text_input("Keyword/Topic (e.g. 'hours')")
                answer = st.text_area("Answer")
                submitted = st.form_submit_button("Save FAQ")
                if submitted:
                    if key:
                        faq[key.lower()] = answer
                        data_manager.save_faq(faq)
                        st.success("FAQ saved!")
                        st.rerun()

        # List/Edit FAQs
        for key, answer in faq.items():
            st.write("---")
            st.write(f"**Topic**: {key}")
            new_ans = st.text_area("Answer", value=answer, key=f"faq_{key}")
            if st.button("Update", key=f"upd_{key}"):
                faq[key] = new_ans
                data_manager.save_faq(faq)
                st.success("Updated!")
            
            if st.button("Delete", key=f"del_faq_{key}"):
                del faq[key]
                data_manager.save_faq(faq)
                st.rerun()

    # --- SETTINGS ---
    with tab3:
        st.subheader("Operational Settings")
        
        with st.form("settings_form"):
            r_name = st.text_input("Restaurant Name", value=config.get("restaurant_name", ""))
            admin_pass = st.text_input("Change Admin Password", value=config.get("admin_password", ""))
            
            submitted = st.form_submit_button("Save Settings")
            if submitted:
                config["restaurant_name"] = r_name
                config["admin_password"] = admin_pass
                data_manager.save_config(config)
                st.success("Settings saved!")

    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.rerun()
