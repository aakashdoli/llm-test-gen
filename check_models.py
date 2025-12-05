import os

# Set your key here if it's not already in your environment
# os.environ["GEMINI_API_KEY"] = "AIzaSy..." 

print("--- Checking Old SDK (google-generativeai) ---")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    
    print("Success! Listing available models (v1beta):")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f" - {m.name}")
except ImportError:
    print("Old SDK not installed.")
except Exception as e:
    print(f"Old SDK Error: {e}")

print("\n--- Checking New SDK (google-genai) ---")
try:
    from google import genai
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    print("Success! Listing available models (v1 Stable):")
    # This might fail if you haven't installed the new library yet
    for m in client.models.list():
        print(f" - {m.name}")
except ImportError:
    print("New SDK not installed (Run: pip install google-genai)")
except Exception as e:
    print(f"New SDK Error: {e}")