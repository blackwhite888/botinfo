import speech_recognition as sr
from pydub import AudioSegment

def recognize_speech_from_voice(audio_path):
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path.replace(".ogg", ".wav")
    audio.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать голос"
    except sr.RequestError as e:
        return f"Ошибка распознавания: {e}"
