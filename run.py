import os
import json
from os.path import join, dirname
import config
import pyaudio
import wave
from watson_developer_cloud import TextToSpeechV1
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguage

from speech_sentiment_python.recorder import Recorder

def response_conversation(text):
    conversation = ConversationV1(
    username=config.CONVERSATION_USERNAME,
    password=config.CONVERSATION_PASSWORD,
    version='2016-09-20')

    # use your own workspace_id
    workspace_id = config.WORKSPACE_ID

    response = conversation.message(workspace_id=workspace_id, message_input={
        'text': text})
    #print(json.dumps(response, indent=2))
    answer = response['output']['text']
    #print(answer)
    return answer                

def transcribe_audio(path_to_audio_file):
    username = config.SPEECH_TO_TEXT_USERNAME
    password = config.SPEECH_TO_TEXT_PASSWORD
    speech_to_text = SpeechToText(username=username,
                                  password=password)

    with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
        return speech_to_text.recognize(audio_file,
            content_type='audio/wav')
    
def synthesize_audio(text,tvoice):

    text_to_speech = TextToSpeechV1(
    username= config.TEXT_TO_SPEECH_USERNAME,
    password= config.TEXT_TO_SPEECH_PASSWORD,
    x_watson_learning_opt_out=True)  # Optional flag

    with open(join(dirname(__file__), 'output.wav'),
          'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, accept='audio/wav',
                                      voice=tvoice))

    #define stream chunk   
    chunk = 1024  

    #open a wav format music  
    f = wave.open(r"output.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()  

def get_text_sentiment(text):
    #return a dictionary containing text sentiment and values
    alchemy_api_key = config.ALCHEMY_API_KEY   
    alchemy_language = AlchemyLanguage(api_key=alchemy_api_key)
    result = alchemy_language.sentiment(text=text)

    #Uncomment to see FULL json output
    #print str(result)
    #print (result['docSentiment'])
    return result['docSentiment']

def main():
    
    recorder = Recorder("speech.wav")

    print("Please say something nice into the microphone\n")
    recorder.record_to_file()

    print("Transcribing audio....\n")
    result = transcribe_audio('speech.wav')
    
    text = result['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")
    response=response_conversation(text)
    print('Answer: '+ str(response))
    sentiment = get_text_sentiment(text)['type']
    score = get_text_sentiment(text)['score']
    print(text,'is',score,sentiment)
    output = str(text+' '+ 'is'+' '+ sentiment)
    synthesize_audio(output,'en-US_MichaelVoice')
    output = str(response[0])
    synthesize_audio(output,'en-US_AllisonVoice')


if __name__ == '__main__':
    try:
        main()
    except:
        print("IOError detected,restarting...")
        main()



