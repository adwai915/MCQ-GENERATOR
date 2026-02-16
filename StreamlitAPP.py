import json
import traceback

import pandas as pd
import streamlit as st

from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.utils import get_table_data, parse_quiz_json, read_file


st.set_page_config(page_title="Automated MCQ Generator", layout="wide")
st.title("Automated MCQ Generator")
st.write("Upload a PDF or TXT file, then generate MCQs.")

RESPONSE_JSON = {
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}

with st.sidebar:
    st.header("Settings")
    subject = st.text_input("Subject", value="General Knowledge")
    tone = st.selectbox("Tone", ["Simple", "Intermediate", "Advanced"])
    number = st.number_input("Number of MCQs", min_value=1, max_value=20, value=5, step=1)

uploaded_file = st.file_uploader("Upload input file", type=["pdf", "txt"])
generate_clicked = st.button("Generate MCQs", type="primary")

if generate_clicked:
    if uploaded_file is None:
        st.warning("Please upload a PDF or TXT file first.")
    else:
        try:
            with st.spinner("Generating MCQs..."):
                text = read_file(uploaded_file)
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": int(number),
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )

            parsed_quiz = parse_quiz_json(response["quiz"])
            if parsed_quiz:
                st.subheader("Generated MCQs")
                for q_no, q_data in parsed_quiz.items():
                    st.markdown(f"**Q{q_no}. {q_data.get('mcq', '')}**")
                    options = q_data.get("options", {})
                    for opt_key in ["a", "b", "c", "d"]:
                        if opt_key in options:
                            st.write(f"{opt_key.upper()}. {options[opt_key]}")
                    st.write(f"Answer: {q_data.get('correct', '')}")
                    st.write("")
            else:
                st.warning("Could not parse formatted quiz output. Showing raw response.")

            table_data = get_table_data(response["quiz"])
            if table_data:
                st.subheader("MCQ Table")
                st.dataframe(pd.DataFrame(table_data), use_container_width=True)
            else:
                st.warning("Could not parse quiz JSON into table format.")

            with st.expander("Raw JSON Output"):
                st.code(response["quiz"], language="json")

            st.subheader("Review")
            st.write(response["review"])
        except Exception as e:
            st.error("An error occurred while generating MCQs.")
            st.code(str(e))
            st.code(traceback.format_exc())
