import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=key,
    temperature=0.7,
)

template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all questions conform to the text.
Use clear, simple English that is easy for school students to understand.
Keep each question and option short. Avoid technical jargon unless required by the source text.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure you make exactly {number} MCQs.
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template,
)

template2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students,\
you need to evaluate question complexity and give a complete analysis in at most 50 words.
If the quiz is not aligned with students' cognitive and analytical abilities,\
update the quiz questions that need changes and adjust tone accordingly.
Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=template2,
)


def _message_to_text(message):
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            part.get("text", str(part)) if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)


def generate_evaluate_chain(inputs):
    quiz_prompt = quiz_generation_prompt.format(**inputs)
    quiz_response = llm.invoke(quiz_prompt)
    quiz_text = _message_to_text(quiz_response)

    review_prompt = quiz_evaluation_prompt.format(
        subject=inputs["subject"],
        quiz=quiz_text,
    )
    review_response = llm.invoke(review_prompt)
    review_text = _message_to_text(review_response)

    return {"quiz": quiz_text, "review": review_text}

