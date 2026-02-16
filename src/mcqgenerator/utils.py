import os
import PyPDF2
import json
import traceback
import re


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text += page_text
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        if not isinstance(quiz_str, str):
            raise ValueError("quiz_str must be a string")

        # Gemini/LLM output can be wrapped in markdown code fences.
        cleaned_quiz_str = quiz_str.strip()
        fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned_quiz_str, re.DOTALL | re.IGNORECASE)
        if fence_match:
            cleaned_quiz_str = fence_match.group(1).strip()

        # convert the quiz from a str to dict
        quiz_dict=json.loads(cleaned_quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


def parse_quiz_json(quiz_str):
    try:
        if not isinstance(quiz_str, str):
            return None

        cleaned_quiz_str = quiz_str.strip()
        fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned_quiz_str, re.DOTALL | re.IGNORECASE)
        if fence_match:
            cleaned_quiz_str = fence_match.group(1).strip()

        parsed = json.loads(cleaned_quiz_str)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


