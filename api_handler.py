import requests

def translate_text(self, text, target_language="en"):
    # Define supported languages
    supported_languages = {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "zh": "Chinese",
        "ja": "Japanese",
        "ru": "Russian",
        "it": "Italian",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    
    if target_language not in supported_languages:
        return f"Error: Language '{target_language}' is not supported. Supported languages: {', '.join(supported_languages.keys())}"

    # Set up request headers and payload
    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_language": target_language
    }
    
    try:
        # Send request to translation API
        response = requests.post(self.api_url, json=payload, headers=headers)
        if response.status_code == 200:
            # Return the translated text
            return response.json().get("translated_text", "")
        else:
            # Handle API error response
            return f"Error: {response.json().get('message', 'Translation failed.')}"
    except requests.RequestException as e:
        # Handle network or request exceptions
        return f"Error: {str(e)}"