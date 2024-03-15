import speech_recognition as sr

def search():
    r = sr.Recognizer()  #record ko recognize
    with sr.Microphone() as source:  #built-in mic or external
        #read the audio data form the defualt microphone
        audio_data = r.record(source, duration=3)
        #convert speech to text
        content = r.recognize_google(audio_data)
        return content