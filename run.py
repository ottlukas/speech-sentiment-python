import os
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage
import config

from speech_sentiment_python.recorder import Recorder

def transcribe_audio(path_to_audio_file):
    username = config.USERNAME
    password = config.PASSWORD
    speech_to_text = SpeechToText(username=username,
                                  password=password)

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,
            content_type='audio/wav')

def get_text_emotion(text):
    #return a dictionary containing emotions and values
    alchemy_api_key = config.API_KEY  
    alchemy_language = AlchemyLanguage(api_key=alchemy_api_key)
    result_emotion = alchemy_language.emotion(text=text)
    
    #Uncomment to see FULL json output
    #print str(result_emotion)
    print result_emotion['docEmotions']
    return result_emotion['docEmotions']


def get_text_sentiment(text):
    #return a dictionary containing text sentiment and values
    alchemy_api_key = config.API_KEY   
    alchemy_language = AlchemyLanguage(api_key=alchemy_api_key)
    result = alchemy_language.sentiment(text=text)

    #Uncomment to see FULL json output
    #print str(result)
    print result['docSentiment']
    return result['docSentiment']

def main():
    recorder = Recorder("speech.wav")

    print("Please say something nice into the microphone\n")
    recorder.record_to_file()

    print("Transcribing audio....\n")
    result = transcribe_audio('speech.wav')
    
    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")
    
    sentiment = get_text_sentiment(text)
    mood = get_text_emotion(text)
    #print(sentiment, score)  

if __name__ == '__main__':
    try:
        main()
    except:
        print("IOError detected, restarting...")
        main()


