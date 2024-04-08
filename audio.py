import speech_recognition as sr

def voice(lang):
    r = sr.Recognizer()  #record ko recognize
    with sr.Microphone() as source:  #built-in mic or external

        audio_data = r.record(source, duration=5)

        if(lang=='1'):
            content = r.recognize_google(audio_data,language='en-US')
        else:
            content = r.recognize_google(audio_data,language='hi-IN')

        audiolist = [content,audio_data]
        return audiolist


