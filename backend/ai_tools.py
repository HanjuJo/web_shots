import os
import requests
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

class AIToolkit:
    def __init__(self):
        pass
    
    def translate_text(self, text, target_lang='en'):
        """텍스트 번역 (DeepL API 사용)"""
        try:
            url = "https://api-free.deepl.com/v2/translate"
            headers = {
                "Authorization": f"DeepL-Auth-Key {os.getenv('DEEPL_API_KEY')}"
            }
            data = {
                "text": [text],
                "target_lang": target_lang.upper()
            }
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            return {'success': True, 'translated_text': result['translations'][0]['text']}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def text_to_speech(self, text, lang='ko'):
        """텍스트를 음성으로 변환"""
        try:
            tts = gTTS(text=text, lang=lang)
            audio_path = "temp_audio.mp3"
            tts.save(audio_path)
            return {'success': True, 'audio_path': audio_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
