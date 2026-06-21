import google.generativeai as genai

api_key = 'AIzaSyAkwYBLX9VSD5jkIA4Lo7LT3_YBMg1UsAQ'
genai.configure(api_key=api_key)

try:
    print("Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"ERROR: {e}")
