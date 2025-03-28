import requests
import logging
from enum import Enum
import json

#API_KEY = "f4528e09-e26a-4f33-b388-20ee9b81bbb3"
logger = logging.getLogger("mcp-sarvam")

class Sarvam:
    class Task(Enum):
        TRANSLATE = "translate"
        LANGUAGE_IDENTIFICATION = "text-lid"
        TRANSLITERATE = "transliterate"
        TRANSLATE_DOC = "parse/translatepdf"
        
    class Languages(Enum):
        ENGLISH = "en-IN"
        HINDI = "hi-IN"
        BENGALI = "bn-IN"
        GUJARATI = "gu-IN"
        KANNADA = "kn-IN"
        MALAYALAM = "ml-IN"
        MARATHI = "mr-IN"
        ODIA = "od-IN"
        PUNJABI = "pa-IN"
        TAMIL = "ta-IN"
        TELUGU = "te-IN"
        
    class Scripts(Enum):
        LATIN = "Latn"        # Latin (Romanized script)
        DEVANAGARI = "Deva"   # Devanagari (Hindi, Marathi)
        BENGALI = "Beng"      # Bengali
        GUJARATI = "Gujr"     # Gujarati
        KANNADA = "Knda"      # Kannada
        MALAYALAM = "Mlym"    # Malayalam
        ODIA = "Orya"         # Odia
        GURMUKHI = "Guru"     # Gurmukhi
        TAMIL = "Taml"        # Tamil
        TELUGU = "Telu"       # Telugu
        
    class Gender(Enum):
        MALE = "Male"
        FEMALE = "Female"
        
    class TranslationMode(Enum):
        FORMAL = "formal"
        COLLOQUIAL_MODERN = "modern-colloquial"
        COLLOQUIAL_CLASSIC = "classic-colloquial"
        CODE_MIXED = "code_mixed"
        
    class TransliterationOptsForTranslation(Enum):
        NULL = "null"
        ROMAN = "roman"
        FULLY_NATIVE = "fully-native"
        SPOKEN_FORM_IN_NATIVE = "spoken-form-in-native"
        
    class NumeralsFormat(Enum):
        INTERNATIONAL = "international"
        NATIVE = "native"
        
    class SpokenFormNumeralsLanguage(Enum):
        ENGLISH = "english"
        NATIVE = "native"
        
    def __init__(self, api_key):
        self.task = Sarvam.Task.TRANSLATE.value
        self.base_url = "https://api.sarvam.ai/"
        self.api_key = api_key
        self.model_translate = "mayura:v1",
        
    def translate_text(self, text: str, 
                       target_language: Languages,
                       source_language: Languages = "auto", 
                       speaker_gender: Gender = Gender.FEMALE.value,
                       mode: TranslationMode = TranslationMode.FORMAL.value,
                       output_script: TransliterationOptsForTranslation = TransliterationOptsForTranslation.FULLY_NATIVE.value,
                       numerals_format: NumeralsFormat = NumeralsFormat.INTERNATIONAL.value,
                       enable_preprocessing: bool = False
                       ):
        logger.info("Function 'translate_text' trigerred.")

        endpoint = f"{self.base_url}{Sarvam.Task.TRANSLATE.value}"
        payload = {
            "input": text,
            "source_language_code": source_language,
            "target_language_code": target_language,
            "speaker_gender": speaker_gender,
            "mode": mode,
            "model": "mayura:v1",
            "enable_preprocessing": enable_preprocessing,
            "output_script": output_script,
            "numerals_format": numerals_format
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": self.api_key
            }
        
        response = requests.request("POST", endpoint, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info("API call successful!")
            logger.info(f"{response}")
            logger.info(f"{response.text}")
            
            logger.info("Function 'translate_text' completed.")
            return json.loads(response.text)['translated_text']
        else:
            logger.error("API call failed!")
            logger.error(f"{response}")
            logger.error(f"{response.text}")
            
            logger.info("Function 'translate_text' completed.")
            raise RuntimeError(f"API called failed. Error: {response.text}")
            
      
    def identify_language(self, text):
        logger.info("Function 'identify_language' trigerred.")
        
        result = {}
        endpoint = f"{self.base_url}{Sarvam.Task.LANGUAGE_IDENTIFICATION.value}"
        payload = {"input": text}
        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": self.api_key
            }
        response = requests.request("POST", endpoint, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info("API call successful!")
            logger.info(f"{response}")
            logger.info(f"{response.text}")
            
            result['Language'] = next((l.name for l in self.Languages if l.value ==  json.loads(response.text)['language_code']), "UNKNOWN")
            result['Script'] = next((s.name for s in self.Scripts if s.value == json.loads(response.text)['script_code']), "UNKNOWN")

            
            logger.info("Function 'identify_language' completed.")
            
            return result
        else:
            logger.error("API call failed!")
            logger.error(f"{response}")
            logger.error(f"{response.text}")
            
            logger.info("Function 'identify_language' completed.")
            raise RuntimeError(f"API called failed. Error: {response.text}")
        
        
        
    def transliterate_text(self, text: str,
                           target_language: Languages,
                           source_language: Languages, 
                           numerals_format: NumeralsFormat = NumeralsFormat.INTERNATIONAL.value,
                           spoken_form: bool = False,
                           spoken_form_numerals_language: SpokenFormNumeralsLanguage = SpokenFormNumeralsLanguage.NATIVE.value
                           ):
        logger.info("Function 'transliterate_text' trigerred.")
        
        endpoint = f"{self.base_url}{Sarvam.Task.TRANSLITERATE.value}"
        payload = {
            "spoken_form": spoken_form,
            "input": text,
            "source_language_code": source_language,
            "target_language_code": target_language,
            "numerals_format": numerals_format,
            "spoken_form_numerals_language": spoken_form_numerals_language
        }
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.request("POST", endpoint, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info("API call successful!")
            logger.info(f"{response}")
            logger.info(f"{response.text}")
            
            logger.info("Function 'transliterate_text' completed.")
            return json.loads(response.text)['transliterated_text']
        else:
            logger.error("API call failed!")
            logger.error(f"{response}")
            logger.error(f"{response.text}")
            
            logger.info("Function 'transliterate_text' completed.")
            raise RuntimeError(f"API called failed. Error: {response.text}")
  
        
    def translate_doc(self):
        from requests_toolbelt.multipart.encoder import MultipartEncoder
        import base64
        import xml.etree.ElementTree as ET
        import json
        endpoint = f"{self.base_url}{Sarvam.Task.TRANSLATE_DOC.value}"
        hard_translate_dict= {
            "Hello": "नमस्कार"
        }
        hard_translate_dict_json = json.dumps(hard_translate_dict, ensure_ascii=False)
        print(f"hard_translate_dict_json is: {hard_translate_dict_json}")
        path = r"C:\Users\shris\OneDrive\Documents\Shristi\Learning\Projects\mcp-server-sarvam\src\mcp_sarvam\selectable_text_essay.pdf"
        payload = MultipartEncoder(
            fields={
                "pdf": ('selectable_text_essay.pdf', open(path, 'rb'),  'application/pdf'),
                "page_number": "1",
                "hard_translate_dict": hard_translate_dict_json,
                "input_lang": Sarvam.Languages.ENGLISH.value,
                "output_lang": Sarvam.Languages.HINDI.value
            }
        )
        print(endpoint)
        print(payload)
        headers = {
            "api-subscription-key": self.api_key,
            "Content-Type": payload.content_type 
        }

 
        response = requests.request('POST', endpoint, data=payload, headers=headers)
        print(response.status_code)
        
        base64_encoded = (response.json())['translated_pdf']
        
        decoded_data = base64.b64decode(base64_encoded)
        
        print(decoded_data)
        
        # Save the decoded data to a PDF file
        with open('decoded_file.pdf', 'wb') as pdf_file:
            pdf_file.write(decoded_data)
            
        print("PDF file has been created successfully.")


if __name__ == "__main__":
    sarvam = Sarvam()
    # res = sarvam.identify_language("मी माझे नशीब स्वतः घडवत आहे.")
    # res = sarvam.translate_text("मी माझे नशीब स्वतः घडवत आहे.", sarvam.Languages.HINDI.value)
    # res = sarvam.transliterate_text("मी माझे नशीब स्वतः घडवत आहे.",sarvam.Languages.ENGLISH.value, sarvam.Languages.MARATHI.value)
    res = sarvam.translate_doc()
    #print(res)