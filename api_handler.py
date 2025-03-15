import requests

class APIHandler:
    def __init__(self):
        self.api_url = "https://api.gemini.ai/v1/translate"
        self.api_key = "AIzaSyAdBZQ55OeV1pGWnWiI2QVsWCO97wUvY2I"

    def translate_text(self, text, target_language="en"):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "target_language": target_language
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("translated_text", "")
            else:
                return f"Error: {response.json().get('message', 'Translation failed.')}"
        except requests.RequestException as e:
            return f"Error: {str(e)}"