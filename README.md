# Nihongo — Japanese Learning Assistant

A full-stack Japanese vocabulary learning app I built to review kanji using spaced repetition, while improving my Python and backend development skills.

## Why I Built This

I wanted a tool tailored to how I actually study Japanese — combining a proper spaced repetition algorithm with a furigana generator for reading real sentences — while also using the project to get hands-on practice with FastAPI, SQLAlchemy, and building a small full-stack application from scratch.

## Features

- **Spaced repetition (SM-2 algorithm)** — words are scheduled for review based on how well you remember them, following the same algorithm used by tools like SuperMemo and (in modified form) Anki.
- **Furigana generator** — paste any Japanese text and get automatic readings for every kanji, powered by morphological analysis (`fugashi` + `unidic-lite`). Readings are editable before saving.
- **Word management** — add, edit, and delete vocabulary entries, each with kanji, reading, and meaning.
- **Review queue** — a shuffled, session-stable queue of due words, with four recall grades (Again / Hard / Good / Easy) mapped to the SM-2 quality scale.
- **Progress stats** — total words, total reviews, accuracy, and a daily streak counter.
- **Word list view** — a sortable table of all saved vocabulary with current review status.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** Streamlit
- **NLP:** fugashi (MeCab-based tokenizer), unidic-lite
- **Testing:** pytest
- **Other:** pandas (word list display)

## Project Structure

```
nihongo/
├── app/
│   ├── models/         # SQLAlchemy models (Word, ReviewLog, database setup)
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/         # Core logic (SM-2 algorithm, furigana analysis, streak calculation)
│   ├── routes/            # API endpoints
│   └── main.py
├── frontend/
│   └── streamlit_app.py   # Streamlit UI
├── tests/
│   └── test_srs.py         # Unit tests for the SM-2 algorithm
└── data/
    └── app.db                # SQLite database (gitignored)
```

## How It Works

1. Add a word (manually or via the furigana generator).
2. Each day, review the words that are due — the app shows the kanji and reading, you grade how well you remembered it.
3. Based on your answer, the SM-2 algorithm recalculates when you'll see that word next — well-known words are shown less often, difficult ones come back sooner.
4. Progress (accuracy, streak, total words) is tracked automatically.

## Setup

```bash
git clone https://github.com/efe-erel/nihongo.git
cd nihongo
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

Two processes need to run in parallel, in separate terminals:

**Terminal 1 — Backend:**
```bash
uvicorn app.main:app --reload --port 8001
```
API docs available at `http://127.0.0.1:8001/docs`

**Terminal 2 — Frontend:**
```bash
streamlit run frontend/streamlit_app.py --server.port 8502
```
App available at `http://localhost:8502`

## Running Tests

```bash
pytest tests/ -v
```

## Roadmap

- [x] Core backend + SM-2 algorithm
- [x] Streamlit interface (review, add word, stats)
- [x] Furigana generator
- [x] Word list, delete, streak tracking
- [ ] Edit word functionality
- [ ] OCR integration (extract text from manga/screenshot images)
- [ ] Deployment

## Notes

This project is under active development — I add new kanji and use it daily as part of my own Japanese studies, so the roadmap will keep evolving based on real usage.