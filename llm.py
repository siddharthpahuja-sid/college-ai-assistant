from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    google_api_key=api_key
)


def generate_answer(question, context):

    prompt = f"""
You are a college AI assistant.

Answer the user's question using only the provided context.

IMPORTANT:
- Give only the direct answer.
- Do not mention the PDF or context.
- Keep the answer clear and concise.
- If the answer is not available in the context, say:
"I could not find this information in the college document."

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = llm.invoke(prompt)

        # Extract only the actual text from Gemini response
        if isinstance(response.content, list):
            text_parts = []

            for item in response.content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            return "\n".join(text_parts)

        return response.content

    except Exception as e:

        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            return "⚠️ AI service is temporarily busy. Please try again in a few seconds."

        return "⚠️ Something went wrong while generating the answer."