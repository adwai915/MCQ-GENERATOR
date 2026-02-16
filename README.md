# Automated MCQ Generator Using LangChain + Gemini API

This project generates multiple-choice questions (MCQs) from uploaded PDF or TXT content using a Streamlit web app and Google Gemini via LangChain.

## Features

- Upload `.pdf` or `.txt` files
- Generate MCQs in simple English
- Select subject, tone, and number of questions
- View questions in human-readable format
- View structured table output and raw JSON output
- Get a short review of quiz quality

## Project Structure

```text
.
|- StreamlitAPP.py
|- requirements.txt
|- .env
|- src/
|  |- mcqgenerator/
|     |- MCQGenerator.py
|     |- utils.py
|     |- logger.py
|- logs/
```

## Prerequisites

- Python 3.10 or 3.11 recommended
- Gemini API key from Google AI Studio

## Installation

```powershell
cd "D:\All Python\Automated-MCQ-Generator-Using-Langchain-OpenAI-API"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Environment Variables

Create or update `.env` in project root:

```env
GEMINI_API_KEY=your_api_key_here
```

You can also use:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Run the App

```powershell
streamlit run .\StreamlitAPP.py
```

Open browser at:

- `http://localhost:8501`

## How to Use

1. Upload a PDF or TXT file.
2. Set subject, tone, and number of MCQs from the sidebar.
3. Click `Generate MCQs`.
4. Read MCQs in simple format (`Q`, options, answer).
5. Optionally inspect table and raw JSON output.

## Tech Stack

- Streamlit
- LangChain
- langchain-google-genai
- PyPDF2
- python-dotenv

## Notes

- Current model used: `gemini-2.5-flash`
- If you see blank page, ensure `StreamlitAPP.py` is not empty and restart Streamlit.
- If PDF text extraction is weak for scanned PDFs, OCR may be required.

## Troubleshooting

- `API key required`:
  - Check `.env` format (one key per line, no extra text).
  - Restart Streamlit after changing `.env`.
- `model not found`:
  - Use a model available for your Gemini key.
- PyPDF2 deprecation errors:
  - This project already uses `PdfReader` (PyPDF2 v3 compatible).
- Python 3.14 warning from LangChain:
  - Prefer Python 3.10/3.11 for best compatibility.

## Security

- Do not commit `.env` or API keys.
- If a key is exposed, rotate it immediately in Google AI Studio.
