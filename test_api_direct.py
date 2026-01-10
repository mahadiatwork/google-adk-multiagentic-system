
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ No API key found")
    exit(1)

import sys

# Force UTF-8 for output
sys.stdout.reconfigure(encoding='utf-8')

genai.configure(api_key=api_key)

print("Listing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")

model_name = "gemini-1.5-flash"
print(f"\nTesting model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Hello, world!")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error with {model_name}: {e}")
    
    # Try backup
    backup_model = "gemini-2.5-flash"
    print(f"\nTrying backup model: {backup_model}")
    try:
        model = genai.GenerativeModel(backup_model)
        response = model.generate_content("Hello, world!")
        print(f"Success with backup! Response: {response.text}")
    except Exception as e:
        print(f"Error with backup: {e}")
