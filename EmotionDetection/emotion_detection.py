"""Emotion detection using the Watson NLP library."""
import requests

URL = ('https://sn-watson-emotion.labs.skills.network/v1/'
       'watson.runtime.nlp.v1/NlpService/EmotionPredict')
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ['anger', 'disgust', 'fear', 'joy', 'sadness']


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion for the text.

    If the service answers with status code 400 (e.g. blank input), every
    value in the returned dictionary is None.
    """
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=payload, headers=HEADERS, timeout=10)

    if response.status_code == 400:
        return {**{emotion: None for emotion in EMOTIONS}, 'dominant_emotion': None}

    scores = response.json()['emotionPredictions'][0]['emotion']
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result['dominant_emotion'] = max(result, key=result.get)
    return result
