import os
import google.generativeai as genai
from pathlib import Path

# Setup API Key
genai.configure(api_key='AIzaSyAkwYBLX9VSD5jkIA4Lo7LT3_YBMg1UsAQ')
model = genai.GenerativeModel('gemini-1.5-pro-latest')

screenshots_dir = Path('/Users/ais/Desktop/Новая папка/Дизайн админ панели')
images = list(screenshots_dir.glob('*.png'))[:3] # Analyze first 3 to avoid payload limits

print(f"Found {len(images)} images to analyze.")

for img_path in images:
    print(f"Analyzing {img_path.name}...")
    try:
        sample_file = genai.upload_file(path=str(img_path))
        response = model.generate_content([
            "Ты frontend-разработчик. Детально опиши этот дизайн интерфейса для верстки. "
            "1. Основная цветовая палитра (фоны, акценты, текст) с примерными HEX. "
            "2. Структура (сайдбар, хедер, карточки). "
            "3. Уникальные элементы, которые отличаются от стандартного Django Admin. "
            "Выдай короткую выжимку.",
            sample_file
        ])
        print(f"\n--- Analysis for {img_path.name} ---")
        print(response.text)
        sample_file.delete()
    except Exception as e:
        print(f"Error analyzing {img_path.name}: {e}")
