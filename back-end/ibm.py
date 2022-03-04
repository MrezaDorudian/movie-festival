import credetials
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1, NaturalLanguageUnderstandingV1, LanguageTranslatorV3
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions


def speech_to_text_request(path_to_audio_file):
    authenticator = IAMAuthenticator(credetials.IBM_SPEECH_TO_TEXT_APIKEY)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(credetials.IBM_SPEECH_TO_TEXT_URL)

    with open(path_to_audio_file, 'rb') as audio_file:
        try:
            response = speech_to_text.recognize(audio=audio_file, content_type='audio/mp3')
            return response.result['results'][0]['alternatives'][0]['transcript']
        except Exception as e:
            return f'Error: {e}'


def natural_language_understanding_request(text):
    authenticator = IAMAuthenticator(credetials.IBM_NATURAL_LANGUAGE_UNDERSTANDING_APIKEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(credetials.IBM_NATURAL_LANGUAGE_UNDERSTANDING_URL)

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(emotion=EmotionOptions())
    )
    emotions = response.result['emotion']['document']['emotion']
    print(emotions)
    if emotions['anger'] > 0.50:
        return False
    return True


def language_translator_request(text, target_language):
    authenticator = IAMAuthenticator(credetials.IBM_LANGUAGE_TRANSLATOR_APIKEY)
    language_translator = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
    language_translator.set_service_url(credetials.IBM_LANGUAGE_TRANSLATOR_URL)

    response = language_translator.translate(text=text, model_id=f'en-{target_language}')
    return response.result['translations'][0]['translation']