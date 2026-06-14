import time

import streamlit as st
import requests as rq
from pygments.lexer import default

if "authentifikatsiya" not in st.session_state:
    st.session_state.authentifikatsiya = False

if not st.session_state.authentifikatsiya:
    kirish, royhatdan_otish = st.tabs(["Kirish", "Royhatdan Otish"])
    with kirish:
        st.title("Kirish")
        with st.form("Kirish form"):
            email = st.text_input("Kirish email")
            password = st.text_input("Parol")
            submit_btn = st.form_submit_button("Syatga kirish")
            if submit_btn:
                response = rq.post("http://127.0.0.1:8000/login", json={"email": email, "password": password})
                if response.json()["message"] == "Successfully logged in":
                    st.session_state.authentifikatsiya = True
                    st.rerun()
                else:

                    st.info("Foydalanuvchi topilmadi !\n Ro'yhatdan o'tishigizni so'raymiz 🤷‍♂️")
                    time.sleep(7)
                    st.rerun()

    with royhatdan_otish:
        st.title("Royhatdan Otish")
        with st.form("Royhatdan form"):
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            phone_number = st.text_input("Phone number", value="+998")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submit_btn_register = st.form_submit_button("Ro'yhatdan o'tish", key="royhatdan_otish")
            if submit_btn_register:
                response = rq.post(
                    "http://127.0.0.1:8000/register",
                    json=({
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone_number": phone_number,
                        "password": password,
                        "confirm_password": confirm_password
                    })
                )

                if response.json()['message'] == "User created":
                    st.session_state.authentifikatsiya = True
                    # st.rerun()
                elif response.json()["message"] == "User already exists":
                    st.info("User allaqachon royhatdan otgan !")
                    # st.rerun()
                else:
                    st.info("Muvaffaqiyatli royhatdan otgan !")
                    time.sleep(3)
                    st.rerun()

else:
    # st.snow()
    st.title("SXD RESTARANIGA XUSH KELIBSIZ !")
    # with st.sidebar:
    #
    #     st.title("🛒 Savat")
    #
    #     cart = [
    #         {"name": "Osh", "price": 30000, "qty": 1},
    #         {"name": "Manti", "price": 25000, "qty": 2},
    #     ]
    #
    #     total = 0
    #
    #     for item in cart:
    #         subtotal = item["price"] * item["qty"]
    #         total += subtotal
    #
    #         with st.container(border=True):
    #             col1, col2 = st.columns([3, 1])
    #
    #             with col1:
    #                 st.write(f"**{item['name']}**")
    #                 st.caption(
    #                     f"{item['qty']} x {item['price']:,} so'm"
    #                 )
    #
    #             with col2:
    #                 st.write(f"{subtotal:,}")
    #
    #     st.divider()
    #
    #     st.metric(
    #         "Jami summa",
    #         f"{total:,} so'm"
    #     )
    #
    #     st.button(
    #         "🚀 Buyurtma berish",
    #         use_container_width=True,
    #         type="primary"
    #     )

    products = rq.get(
        "http://127.0.0.1:8000/categories"
    ).json()["categories"]
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                product = products[i + j]
                with cols[j]:
                    # st.image(product["image_url"])
                    # st.info(product["name"])
                    # st.write(f"{product['price']} so'm")
                    st.button(
                        f"{product["name"]}",
                        key=product["name"]

                    )
