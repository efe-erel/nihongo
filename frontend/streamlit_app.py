
import streamlit as st
import requests
import random
import pandas as pd

HIRAGANA = [
    [("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o")],
    [("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko")],
    [("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so")],
    [("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to")],
    [("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no")],
    [("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho")],
    [("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo")],
    [("や", "ya"), None, ("ゆ", "yu"), None, ("よ", "yo")],
    [("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro")],
    [("わ", "wa"), None, None, None, ("を", "wo")],
    [("ん", "n"), None, None, None, None],
]

KATAKANA = [
    [("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")],
    [("カ", "ka"), ("キ", "ki"), ("ク", "ku"), ("ケ", "ke"), ("コ", "ko")],
    [("サ", "sa"), ("シ", "shi"), ("ス", "su"), ("セ", "se"), ("ソ", "so")],
    [("タ", "ta"), ("チ", "chi"), ("ツ", "tsu"), ("テ", "te"), ("ト", "to")],
    [("ナ", "na"), ("ニ", "ni"), ("ヌ", "nu"), ("ネ", "ne"), ("ノ", "no")],
    [("ハ", "ha"), ("ヒ", "hi"), ("フ", "fu"), ("ヘ", "he"), ("ホ", "ho")],
    [("マ", "ma"), ("ミ", "mi"), ("ム", "mu"), ("メ", "me"), ("モ", "mo")],
    [("ヤ", "ya"), None, ("ユ", "yu"), None, ("ヨ", "yo")],
    [("ラ", "ra"), ("リ", "ri"), ("ル", "ru"), ("レ", "re"), ("ロ", "ro")],
    [("ワ", "wa"), None, None, None, ("ヲ", "wo")],
    [("ン", "n"), None, None, None, None],
]


def render_kana_table(table):
    for row in table:
        cols = st.columns(5)
        for col, cell in zip(cols, row):
            if cell:
                kana, romaji = cell
                col.markdown(
                    f"<div style='text-align:center; font-size:28px'>{kana}</div>"
                    f"<div style='text-align:center; color:gray'>{romaji}</div>",
                    unsafe_allow_html=True
                )
            else:
                col.write("")

API_URL = "http://127.0.0.1:8001"

st.title("Nihongo - Japanese Learning Assistant")


tab_review, tab_add, tab_stats, tab_furigana, tab_words, tab_kana = st.tabs(["Review", "Add Word", "Stats", "Furigana", "Words", "Kana"])

with tab_review:
    if "review_queue" not in st.session_state:
        response = requests.get(f"{API_URL}/review/today")
        words = response.json()
        random.shuffle(words)
        st.session_state["review_queue"] = words

    queue = st.session_state["review_queue"]

    if not queue:
        st.write("No words to review today! 🎉")
        if st.button("Refresh"):
            del st.session_state["review_queue"]
            st.rerun()
    else:
        st.write(f"{len(queue)} words left to review.")

        current_word = queue[0]

        st.header(current_word["kanji"])
        st.subheader(current_word["reading"])

        if st.button("Show meaning"):
            st.write(current_word["meaning"])

        st.write("---")
        st.write("How well did you remember it?")

        col1, col2, col3, col4 = st.columns(4)

        def submit_review(quality):
            requests.post(f"{API_URL}/review/{current_word['id']}/answer", json={"quality": quality})
            st.session_state["review_queue"].pop(0)
            st.rerun()

        with col1:
            if st.button("Again (quality=0)"):
                submit_review(0)
        with col2:
            if st.button("Hard (quality=2)"):
                submit_review(2)
        with col3:
            if st.button("Good (quality=3)"):
                submit_review(3)
        with col4:
            if st.button("Easy (quality=5)"):
                submit_review(5)

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
    st.subheader("Your progress")

    response = requests.get(f"{API_URL}/stats")
    stats = response.json()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total words", stats["total_words"])
    col2.metric("Total reviews", stats["total_reviews"])
    col3.metric("Accuracy", f"{stats['accuracy']}%")
    col4.metric("Streak", f"{stats['current_streak']} 🔥")

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


with tab_words:
    st.subheader("Your words")

    response = requests.get(f"{API_URL}/words")
    all_words = response.json()

    if not all_words:
        st.write("No words added yet.")
    else:
        df = pd.DataFrame(all_words)
        st.dataframe(df[["kanji", "reading", "meaning", "repetitions", "next_review_date"]])

        st.write("---")
        st.write("Delete a word")

        word_options = {f"{w['kanji']} ({w['meaning']})": w["id"] for w in all_words}
        selected_label = st.selectbox("Select a word to delete", list(word_options.keys()))

        if st.button("Delete"):
            word_id = word_options[selected_label]
            requests.delete(f"{API_URL}/words/{word_id}")
            st.success(f"Deleted: {selected_label}")
            st.rerun()


with tab_kana:
    st.subheader("Kana chart")

    kana_type = st.radio("Choose", ["Hiragana", "Katakana"], horizontal=True)

    if kana_type == "Hiragana":
        render_kana_table(HIRAGANA)
    else:
        render_kana_table(KATAKANA)