import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the secret API key from your .env file
load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

# 2. Configure the library
genai.configure(api_key=api_key)

def get_ai_review(code_content):
    """
    Sends the code to Gemini 2.5 Flash and returns a structured review.
    """
    try:
        # Initialize the specific model
        
        model = genai.GenerativeModel("gemini-2.0-flash-latest",
            # Inside get_ai_review function
           # Inside get_ai_review function in src/ai_engine.py
system_instruction=(
    "You are a Senior Software Engineer. Analyze the code and provide feedback in 4 distinct sections.\n"
    "Use these exact tags to separate sections:\n"
    "[ERRORS]: List all logical or syntax bugs here.\n"
    "[SUGGESTIONS]: List style, security, and readability improvements if really necessary for the code also suggesr to remove if any unused variables,imports are there.\n"
    "[COMPLEXITY]: Provide Big-O time and space complexity analysis.\n"
    "[FIXED_CODE]: Provide the full corrected code block here only if it has errors and need optimization."
    "Keep it shorter."
)
)
        
        
        # Generate the response
        response = model.generate_content(f"Please review this code:\n\n{code_content}",stream=True)
        
        return response.text
        
    except Exception as e:
        return f"❌ Error connecting to Gemini: {str(e)}"
