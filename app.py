import streamlit as st
import requests as rq

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
    with royhatdan_otish:
        st.title("Royhatdan Otish")


else:
    # st.snow()
    st.title("SXD RESTARANIGA XUSH KELIBSIZ !")
    st.image(image="./Images/img.png")
    st.image(image="./Images/img.png")
    st.image(image="./Images/img.png")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Mavjud ovqat turlari", value="25")
    with col2:
        st.metric(label="Mavjud ichimlik turlari", value="25")
    with col3:
        st.metric(label="Mavjud salat turlari", value="25")
    with st.sidebar:
        st.header("Kategoriyalar ✔")
