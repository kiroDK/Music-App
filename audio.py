import speech_recognition as sr

def voice():
    r = sr.Recognizer()  #record ko recognize
    with sr.Microphone() as source:  #built-in mic or external
        #read the audio data form the defualt microphone
        audio_data = r.record(source, duration=5)
        #convert speech to text

        # with open('static/audioblog/audioblog.wav','wb') as f:
        #     f.write(audio_data.get_wav_data())

        content = r.recognize_google(audio_data)
        audiolist = [content,audio_data]
        return audiolist


