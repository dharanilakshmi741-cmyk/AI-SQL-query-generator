import os
import json

from groq import Groq
from dotenv import load_dotenv

from .sql_instructions import SQL_PROMPT

# Load .env file
load_dotenv()

# Read API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Check your .env file."
    )

# Create Groq Client
client = Groq(
    api_key=GROQ_API_KEY
)


def generate_sql(question, dialect, model_name):

    prompt = f"""
{SQL_PROMPT}

SQL Dialect:
{dialect}

User Question:
{question}

Return ONLY valid JSON.
"""

    try:

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        raw_response = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        print("\n===== GROQ RESPONSE =====")
        print(raw_response)
        print("=========================\n")

        raw_response = raw_response.replace(
            "```json",
            ""
        )

        raw_response = raw_response.replace(
            "```",
            ""
        )

        raw_response = raw_response.strip()

        try:

            parsed = json.loads(
                raw_response
            )

            return {
                "query": parsed.get(
                    "query",
                    ""
                ),
                "explanation": parsed.get(
                    "explanation",
                    ""
                )
            }

        except Exception:

            return {
                "query": raw_response,
                "explanation":
                "JSON parsing failed. Showing raw response."
            }

    except Exception as e:

        print(
            "ERROR:",
            str(e)
        )

        return {
            "query": "",
            "explanation":
            f"Error: {str(e)}"
        }