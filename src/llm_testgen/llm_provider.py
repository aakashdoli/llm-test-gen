from __future__ import annotations
import os
from typing import Optional

class LLMProvider:
    """Pluggable LLM provider. Supports OpenAI and Google Gemini (New SDK)."""

    def __init__(self):
        # Normalize provider name
        raw_provider = os.getenv("LLM_PROVIDER", "").lower().strip()
        if raw_provider in ["google", "gemini"]:
            self.provider = "google"
        else:
            self.provider = raw_provider
            
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        # Default model to try first
        self.model = os.getenv("LLM_MODEL", "gemini-1.5-flash") 

    def generate(self, prompt: str) -> Optional[str]:
        if not self.provider:
            return None

        if self.provider == "google":
            return self._generate_google(prompt)
        
        if self.provider == "openai":
            return self._generate_openai(prompt)
        
        print(f"Warning: Unknown provider '{self.provider}'. Using fallback.")
        return None

    def _generate_google(self, prompt: str) -> Optional[str]:
        if not self.api_key:
            print("Error: GEMINI_API_KEY not set.")
            return None
            
        try:
            from google import genai
            # Initialize client (letting SDK choose best default version)
            client = genai.Client(api_key=self.api_key)
            
            # 1. Try the configured model first
            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                if response.text:
                    return response.text
            except Exception as e:
                # Only warn if it's a 404 (Not Found), otherwise it might be a real error
                if "404" in str(e) or "not found" in str(e).lower():
                    print(f"Model '{self.model}' not found. Attempting auto-discovery...")
                else:
                    print(f"Google Gemini Error: {e}")
                    return None

            # 2. Auto-Discovery (If first attempt failed)
            try:
                print("Scanning for available models...")
                # List all models available to your API key
                all_models = list(client.models.list())
                
                valid_models = []
                for m in all_models:
                    # Safely get the name, handling both object and dict styles
                    name = getattr(m, 'name', None) or m.get('name')
                    if not name: continue
                    
                    # Clean name (remove 'models/' prefix)
                    clean_name = name.split("/")[-1]
                    
                    # We only want 'gemini' models, ignore 'embedding' or 'aqa' models
                    if "gemini" in clean_name.lower() and "vision" not in clean_name.lower():
                        valid_models.append(clean_name)

                if not valid_models:
                    print("Error: No valid Gemini models found for this API key.")
                    return None
                
                print(f"Found available models: {valid_models}")

                # 3. Smart Selection: Prefer Flash -> Pro -> 1.0
                best_model = valid_models[0] # Default to first found
                
                # Priority logic
                for m in valid_models:
                    if "1.5-flash" in m: 
                        best_model = m
                        break
                else:
                    for m in valid_models:
                        if "1.5-pro" in m:
                            best_model = m
                            break

                print(f"-> Retrying with active model: {best_model}")
                self.model = best_model # Update for future calls

                # 4. Retry with the discovered model
                response = client.models.generate_content(
                    model=best_model,
                    contents=prompt
                )
                if response.text:
                    return response.text

            except Exception as discovery_error:
                print(f"Auto-discovery failed: {discovery_error}")
            
            return None
            
        except ImportError:
            print("CRITICAL ERROR: 'google-genai' library missing. Run: pip install google-genai")
            return None
        except Exception as e:
            print(f"Google SDK Error: {e}")
            return None

    def _generate_openai(self, prompt: str) -> Optional[str]:
        if not self.api_key:
            print("Error: OPENAI_API_KEY not set.")
            return None
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return None
