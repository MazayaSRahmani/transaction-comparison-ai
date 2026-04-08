import google.generativeai as genai
import pandas as pd
from utils.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL = genai.GenerativeModel("gemini-1.5-flash")

def parse_with_gemini(file_text):
    prompt = f"""
    Extract structured transaction data from the following text.

    Return JSON array with fields:
    - date
    - description
    - amount
    - type (debit/credit)

    TEXT:
    {file_text}
    """

    response = MODEL.generate_content(prompt)

    try:
        data = eval(response.text)  # ⚠️ replace with safer JSON parsing later
        return pd.DataFrame(data)
    except Exception:
        return pd.DataFrame(columns=["date", "description", "amount", "type"])


def read_file(file):
    import PyPDF2

    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.to_string()

    else:
        raise ValueError("Unsupported file format")