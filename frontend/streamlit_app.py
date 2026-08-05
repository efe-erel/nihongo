
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Nihongo - Japanese Learning Assistant")


tab_review, tab_add = st.tabs(["Review", "Add Word"])

with tab_review:
    response = requests.get(f"{API_URL}/review/today")
    words = response.json()

    if not words:
        st.write("No reviews for today! 🎉")
    else:
        st.write(f"Words to review today: {len(words)}")

        current_word = words[0]
        st.header(current_word["kanji"])
        st.subheader(current_word["reading"])

        if st.button("Show Meaning"):
            st.write(current_word["meaning"])

        st.write("Rate your recall quality (0-5):")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("hard (quality = 2)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 2})
                st.rerun()

        with col2:
            if st.button("medium (quality = 3)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 3})
                st.rerun()

        with col3:
            if st.button("easy (quality = 5)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 5})
                st.rerun()

with tab_add:
    st.subheader("Add a new word")

    with st.form("add_word_form", clear_on_submit=True):
        kanji = st.text_input("Kanji")
        reading = st.text_input("Reading (hiragana/katakana)")
        meaning = st.text_area("Meaning")

        submitted = st.form_submit_button("Add Word")

        if submitted:
            if not kanji or not reading or not meaning:
                st.error("Please fill in all fields before submitting.")
            else:
                response = requests.post(f"{API_URL}/words", json={
                    "kanji": kanji,
                    "reading": reading,
                    "meaning": meaning
                })

                if response.status_code == 200:
                    st.success(f"Word '{kanji}' added successfully!")
                else:
                    st.error("Something went wrong while adding the word. Please try again.")