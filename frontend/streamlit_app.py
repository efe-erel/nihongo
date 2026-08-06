
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Nihongo - Japanese Learning Assistant")


tab_review, tab_add, tab_stats, tab_furigana = st.tabs(["Review", "Add Word", "Stats", "Furigana"])

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

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("Again (quality=0)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 0})
                st.rerun()

        with col2:
            if st.button("Hard (quality=2)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 2})
                st.rerun()

        with col3:
            if st.button("Good (quality=3)"):
                requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": 3})
                st.rerun()

        with col4:
            if st.button("Easy (quality=5)"):
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

with tab_stats:
    st.subheader("Your Learning Stats")
    response = requests.get(f"{API_URL}/stats")
    stats = response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Words", stats["total_words"])
    col2.metric("Total Reviews", stats["total_reviews"])
    col3.metric("Accuracy (%)", stats["accuracy"])


with tab_furigana:
    st.subheader("Furigana generator")

    text_input = st.text_area("Enter Japanese text")

    if st.button("Analyze"):
        response = requests.post(f"{API_URL}/furigana", json={"text": text_input})
        st.session_state["furigana_tokens"] = response.json()["tokens"]

    if "furigana_tokens" in st.session_state:
        st.write("---")
        for index, token in enumerate(st.session_state["furigana_tokens"]):
            if token["has_kanji"]:
                st.write(f"**{token['surface']}**")
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    reading = st.text_input(
                        "Reading",
                        value=token["reading"],
                        key=f"reading_{index}",
                        label_visibility="collapsed"
                    )
                with col2:
                    meaning = st.text_input(
                        "Meaning",
                        key=f"meaning_{index}",
                        placeholder="Meaning",
                        label_visibility="collapsed"
                    )
                with col3:
                    if st.button("Save", key=f"save_{index}"):
                        if meaning:
                            requests.post(
                                f"{API_URL}/words",
                                json={
                                    "kanji": token["surface"],
                                    "reading": reading,
                                    "meaning": meaning
                                }
                            )
                            st.success(f"Saved: {token['surface']}")
                        else:
                            st.warning("Enter a meaning first.")
            else:
                st.write(token["surface"])