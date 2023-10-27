import os
import fitz # PyMuPDF
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

def extract_text_from_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()

        # delete file
        os.remove(file_path)

        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
def ans_question_from_text(text, question):
    messages = [
        {"role": "system", "content": f"Use the following text to answer the question: {text}"},
        {"role": "user", "content": question}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message = response['choices'][0]['message']['content']
        return message
    except Exception as e:
        raise Exception(f"Error chatting with OpenAI: {str(e)}")