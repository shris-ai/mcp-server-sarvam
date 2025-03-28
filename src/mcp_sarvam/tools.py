import os
from enum import Enum
import logging
from dotenv import load_dotenv
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from . import sarvam
from typing import List, Optional
import json

load_dotenv()
logger = logging.getLogger("mcp-sarvam")

logger.info("Fetching api key for running tools...")
api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    logger.error("Environment variable SARVAM_API_KEY not found in the environment.")
    raise ValueError("SARVAM_API_KEY environment variable is required.")
else:
    logger.info("Environment variable SARVAM_API_KEY is present in the environment.")

class SarvamTools(str, Enum):
    TRANSLATION = "translate_text"
    LANGUAGE_IDENTIFICATION = "identify_language"
    TRANSLITERATION = "transliterate_text"
    
class ToolHandler():
    def __init__(self, tool_name: str):
        self.name = tool_name
        
    def get_tool_description(self) -> Tool:
        raise NotImplementedError()
    
    def run_tool(self, args: dict) -> list[TextContent]:
        raise NotImplementedError
    
class CreateToolHandler_Translation(ToolHandler):
    def __init__(self):
        super().__init__(SarvamTools.TRANSLATION.value)
        
    class TranslationRequest(BaseModel):
        text: str = Field(..., description="Text to translate")
        target_language: sarvam.Sarvam.Languages = Field(..., description="""Must be one of the supported languages: ENGLISH, HINDI 
                                                         BENGALI, GUJARATI, KANNADA, MALAYALAM, MARATHI, ODIA, PUNJABI, TAMIL, TELUGU 
                                                         """)
        source_language: Optional[sarvam.Sarvam.Languages] = Field("auto", description="""[OPTIONAL] Must be one of the supported languages: ENGLISH, HINDI 
                                                         BENGALI, GUJARATI, KANNADA, MALAYALAM, MARATHI, ODIA, PUNJABI, TAMIL, TELUGU 
                                                         """)
        #is_speaker_gender_male: bool = Field(..., description="Check for Male (leave unchecked for Female)")
        speaker_gender: Optional[sarvam.Sarvam.Gender] = Field(None, description="""[OPTIONAL] Must be one of the two: MALE, FEMALE
                                                         """)
        mode: Optional[sarvam.Sarvam.TranslationMode] = Field(None, description="""[OPTIONAL] Must be one of the supported modes: FORMAL, COLLOQUIAL_MODERN, COLLOQUIAL_CLASSIC, CODE_MIXED
                                                         """)
        output_script: Optional[List[sarvam.Sarvam.TransliterationOptsForTranslation]] = Field(None, description="""[OPTIONAL] Must be one of the supported scripts: FORMAL, COLLOQUIAL_MODERN, COLLOQUIAL_CLASSIC, CODE_MIXED
                                                         """)
        numerals_format: Optional[List[sarvam.Sarvam.NumeralsFormat]] = Field(None, description="""[OPTIONAL] Must be one of the supported formats: NULL, ROMAN, FULLY_NATIVE, SPOKEN_FORM_IN_NATIVE""")

        
    def get_tool_description(self):
        logger.info(f"Getting tool description for tool: {self.name}")
        return Tool(
            name = self.name,
            description = "Translates the given text from English or any Indic language to any Indic language or English.",
            inputSchema=self.TranslationRequest.model_json_schema()
        )
        
    def run_tool(self, args: dict):
        logger.info(f"Translating text for the given args: {args}")
        
        if "text" not in args or "target_language" not in args:
            logger.error("Required arguments are missing!")
            raise RuntimeError("Required: 'text' and 'target language'")
        
        api_args = {
            'text': args['text']
        }
        
        if args["target_language"] in sarvam.Sarvam.Languages.__members__:
            api_args['target_language'] = sarvam.Sarvam.Languages[args['target_language']].value
        else:
            logger.error(f"Invalid argument: target_language='{args['target_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
            raise RuntimeError(f"Invalid argument: target_language='{args['target_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")

        if args.get('source_language') is not None:
            if args['source_language'] in sarvam.Sarvam.Languages.__members__:
                api_args['source_language'] = sarvam.Sarvam.Languages[args['source_language']].value
            else:
                logger.error(f"Invalid argument: source_language='{args['source_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: source_language='{args['source_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
   
        if args.get('speaker_gender') is not None:
            if args['speaker_gender'] in sarvam.Sarvam.Gender.__members__:
                    api_args['speaker_gender'] = sarvam.Sarvam.Gender[args['speaker_gender']].value
            else:
                logger.error(f"Invalid argument: speaker_gender='{args['speaker_gender']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Gender.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: speaker_gender='{args['speaker_gender']}'. Allowedd any one of these: {', '.join(sarvam.Sarvam.Gender.__members__.keys())}")
 
        if args.get('mode') is not None:
            if args['mode'] in sarvam.Sarvam.TranslationMode.__members__:
                api_args['mode'] = sarvam.Sarvam.TranslationMode[args['mode']].value
            else:
                logger.error(f"Invalid argument: mode='{args['mode']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.TranslationMode.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: mode='{args['mode']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.TranslationMode.__members__.keys())}")
 
        if args.get('output_script') is not None:
            if args['output_script'] in sarvam.Sarvam.TransliterationOptsForTranslation.__members__:
                    api_args['output_script'] = sarvam.Sarvam.TransliterationOptsForTranslation[args['output_script']].value
            else:
                logger.error(f"Invalid argument: output_script='{args['output_script']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.TransliterationOptsForTranslation.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: output_script='{args['output_script']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.TransliterationOptsForTranslation.__members__.keys())}")

        if args.get('numerals_format') is not None:
            if args['numerals_format'] in sarvam.Sarvam.NumeralsFormat.__members__:
                api_args['numerals_format'] = sarvam.Sarvam.NumeralsFormat[args['numerals_format']].value
            else:
                logger.error(f"Invalid argument: numerals_format='{args['numerals_format']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.NumeralsFormat.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: numerals_format='{args['numerals_format']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.NumeralsFormat.__members__.keys())}")

        
        try:
            api = sarvam.Sarvam(api_key)
            result = api.translate_text(
                **api_args
            )
            
            logger.info("Successfully fetched results")
            logger.debug(f"API response: {result}")

            return result
        except Exception as e:
            logger.error(f"Failed to translate text. Error: {str(e)}")
            raise
        
    
class CreateToolHandler_LanguageIdentification(ToolHandler):
    def __init__(self):
        super().__init__(SarvamTools.LANGUAGE_IDENTIFICATION.value)
        
    class LanguageIdentificationRequest(BaseModel):
        text: str = Field(..., description="Text for which the language should be identified")
        
    def get_tool_description(self):
        logger.info(f"Getting tool description for tool: {self.name}")
        return Tool(
            name = self.name,
            description = "Text for which the language should be identified. The detected language will be either English or one of the supported Indic languages.",
            inputSchema=self.LanguageIdentificationRequest.model_json_schema()
        )
        
    def run_tool(self, args: dict):
        logger.info(f"Identifying language for the given args: {args}")
        
        if "text" not in args:
            logger.error("Required arguments are missing!")
            raise RuntimeError("Required: 'text'.")
        
        api_args = {
            'text': args['text']
        }
        
        try:
            api = sarvam.Sarvam(api_key)
            result = api.identify_language(
                **api_args
            )
            
            logger.info("Successfully fetched results")
            logger.debug(f"API response: {result}")

            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Failed to translate text. Error: {str(e)}")
            raise
        
        
class CreateToolHandler_Transliteration(ToolHandler):
    def __init__(self):
        super().__init__(SarvamTools.TRANSLITERATION.value)
        
    class TransliterationRequest(BaseModel):
        text: str = Field(..., description="Text to transliterate")
        target_language: sarvam.Sarvam.Languages = Field(..., description="""Must be one of the supported languages: ENGLISH, HINDI 
                                                         BENGALI, GUJARATI, KANNADA, MALAYALAM, MARATHI, ODIA, PUNJABI, TAMIL, TELUGU 
                                                         """)
        source_language: Optional[sarvam.Sarvam.Languages] = Field(..., description="""Must be one of the supported languages: ENGLISH, HINDI 
                                                         BENGALI, GUJARATI, KANNADA, MALAYALAM, MARATHI, ODIA, PUNJABI, TAMIL, TELUGU 
                                                         """)
        numerals_format: Optional[List[sarvam.Sarvam.NumeralsFormat]] = Field(None, description="""[OPTIONAL] Must be one of the supported formats: NULL, ROMAN, FULLY_NATIVE, SPOKEN_FORM_IN_NATIVE""")
        spoken_form: Optional[bool] = Field(None, description="Must be either of the two: TRUE, FALSE")
        spoken_form_numerals_language: Optional[List[sarvam.Sarvam.SpokenFormNumeralsLanguage]] = Field(None, description="Must be one of the supported formats: ENGLISH, NATIVE")

        
    def get_tool_description(self):
        logger.info(f"Getting tool description for tool: {self.name}")
        return Tool(
            name = self.name,
            description =  "Transliterates the given text from English or any Indic language to any Indic language or English while preserving its pronunciation.",
            inputSchema=self.TransliterationRequest.model_json_schema()
        )
        
    def run_tool(self, args: dict):
        logger.info(f"Transliterating text for the given args: {args}")
        
        if "text" not in args or "target_language" not in args or "source_language" not in args:
            logger.error("Required arguments are missing!")
            raise RuntimeError("Required: 'text' and 'target language' and 'source_language'")
        
        api_args = {
            'text': args['text']
        }
        
        if args["target_language"] in sarvam.Sarvam.Languages.__members__:
            api_args['target_language'] = sarvam.Sarvam.Languages[args['target_language']].value
        else:
            logger.error(f"Invalid argument: target_language='{args['target_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
            raise RuntimeError(f"Invalid argument: target_language='{args['target_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")

        if args['source_language'] in sarvam.Sarvam.Languages.__members__:
            api_args['source_language'] = sarvam.Sarvam.Languages[args['source_language']].value
        else:
            logger.error(f"Invalid argument: source_language='{args['source_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
            raise RuntimeError(f"Invalid argument: source_language='{args['source_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.Languages.__members__.keys())}")
   
        if args.get('numerals_format') is not None:
            if args['numerals_format'] in sarvam.Sarvam.NumeralsFormat.__members__:
                api_args['numerals_format'] = sarvam.Sarvam.NumeralsFormat[args['numerals_format']].value
            else:
                logger.error(f"Invalid argument: numerals_format='{args['numerals_format']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.NumeralsFormat.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: numerals_format='{args['numerals_format']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.NumeralsFormat.__members__.keys())}")
            
        if args.get('spoken_form') is not None:
            if args['spoken_form'] is True or args['spoken_form'] is False:
                api_args['spoken_form'] = args['spoken_form']
            else:
                logger.error(f"Invalid argument: spoken_form='{args['spoken_form']}'. Allowed any one of these: TRUE, FALSE")
                raise RuntimeError(f"Invalid argument: spoken_form='{args['spoken_form']}'. Allowed any one of these: TRUE, FALSE")
        
        if args.get('spoken_form_numerals_language') is not None:
            if args['spoken_form_numerals_language'] in sarvam.Sarvam.SpokenFormNumeralsLanguage.__members__:
                api_args['spoken_form_numerals_language'] = sarvam.Sarvam.SpokenFormNumeralsLanguage[args['spoken_form_numerals_language']].value
            else:
                logger.error(f"Invalid argument: spoken_form_numerals_language='{args['spoken_form_numerals_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.SpokenFormNumeralsLanguage.__members__.keys())}")
                raise RuntimeError(f"Invalid argument: spoken_form_numerals_language='{args['spoken_form_numerals_language']}'. Allowed any one of these: {', '.join(sarvam.Sarvam.SpokenFormNumeralsLanguage.__members__.keys())}")
       
        try:
            api = sarvam.Sarvam(api_key)
            result = api.translate_text(
                **api_args
            )
            
            logger.info("Successfully fetched results")
            logger.debug(f"API response: {result}")

            return result
        except Exception as e:
            logger.error(f"Failed to transliterate text. Error: {str(e)}")
            raise
 