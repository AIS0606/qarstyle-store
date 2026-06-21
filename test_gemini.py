import google.generativeai as genai
import sys

api_key = 'AIzaSyAkwYBLX9VSD5jkIA4Lo7LT3_YBMg1UsAQ'
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Привет, это тест!")
    print("SUCCESS")
    print(response.text)
except Exception as e:
    print(f"ERROR: {e}")
