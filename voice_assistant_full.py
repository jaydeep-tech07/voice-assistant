# Voice Assistant - Full Version (~85 lines)
# Install: pip install SpeechRecognition pyttsx3 wikipedia pyaudio
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import random
import os
import urllib.parse
import pywhatkit

try:
    import pygetwindow as gw
    HAS_GW = True
except ImportError:
    HAS_GW = False

# ---------- Setup ----------
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # bolne ki speed

MUSIC_DIR = os.path.expanduser("~/Music")  # apna music folder yahan set karo

JOKES = [
    "Programmer ko chai kyun pasand hai? Kyunki usme Java hota hai.",
    "Computer ko thand kyun lagi? Kyunki uski Windows khuli thi.",
    "Bug fix kiya to teen naye bug mil gaye. Yehi to zindagi hai.",
]


# ---------- Output: Text-to-Speech ----------
def speak(text):
    print(">>> SPEAK FUNCTION CALLED <<<")
    print("Assistant:", text)

    try:
        voice_engine = pyttsx3.init("sapi5")
        voices = voice_engine.getProperty("voices")

        if voices:
            voice_engine.setProperty("voice", voices[0].id)

        voice_engine.setProperty("rate", 170)
        voice_engine.setProperty("volume", 1.0)

        voice_engine.say(text)
        voice_engine.runAndWait()
        voice_engine.stop()

    except Exception as e:
        print("Voice Error:", e)


# ---------- Input: Speech-to-Text ----------
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Sun raha hoon...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
        return r.recognize_google(audio, language="en-IN").lower()
    except (sr.WaitTimeoutError, sr.UnknownValueError):
        return ""  # kuch samajh nahi aaya, dobara suno
    except (sr.RequestError, OSError):
        # internet ya mic ki dikkat ho to keyboard se command do
        return input("Type karo: ").lower()

def close_window(keyword):
    """Jis window ke title mein keyword mile, usse band kar deta hai."""
    if not HAS_GW:
        return False
    try:
        matches = [w for w in gw.getAllWindows() if keyword.lower() in w.title.lower() and w.title.strip()]
        if matches:
            matches[0].close()
            return True
    except Exception:
        pass
    return False
# ---------- Greeting ----------
def wish():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 17:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Main aapka voice assistant hoon. Bataiye kya karna hai?")


# ---------- Commands ----------
def handle(cmd):
    """Command ko match karke kaam karta hai. False return kare to program band."""
    if "close" in cmd:
        if "youtube" in cmd:
            ok = close_window("youtube")
        elif "google" in cmd or "chrome" in cmd or "browser" in cmd or "edge" in cmd:
            ok = close_window("google") or close_window("chrome") or close_window("edge")
        elif "wikipedia" in cmd:
            ok = close_window("wikipedia")
        elif "notepad" in cmd:
            ok = close_window("notepad")
        elif "calculator" in cmd:
            ok = close_window("calculator")
        else:
            ok = False

        if ok:
            speak("Band kar diya")
        elif not HAS_GW:
            speak("Close karne ke liye pygetwindow library chahiye, pehle use install karo")
        else:
            speak("Wo window mujhe nahi mili, shayad pehle se band hai")

    elif "time" in cmd:
        speak("Abhi time hai " + datetime.datetime.now().strftime("%I:%M %p"))

    elif "date" in cmd or "today" in cmd:
        speak("Aaj ki date hai " + datetime.datetime.now().strftime("%d %B %Y"))

    elif "wikipedia" in cmd:
        topic = cmd.replace("wikipedia", "").replace("search", "").strip()
        try:
            speak(wikipedia.summary(topic, sentences=2))
            page_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(topic.replace(" ", "_"))
            webbrowser.open(page_url)
        except Exception:
            speak("Is topic par jaankari nahi mili")

    elif "open youtube" in cmd:
        speak("YouTube khol raha hoon")
        webbrowser.open("https://youtube.com")

    elif "open google" in cmd:
        speak("Google khol raha hoon")
        webbrowser.open("https://google.com")

    elif "search" in cmd:
        query = cmd.replace("search", "").strip()
        if "youtube" in query:
            query = query.replace("on youtube", "").replace("youtube", "").strip()
            speak("YouTube par pehla video chala raha hoon: " + query)
            try:
                pywhatkit.playonyt(query)
            except Exception:
                speak("Video chalane mein dikkat aayi, search results khol raha hoon")
                webbrowser.open("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query))
        else:
            speak("Google par search kar raha hoon: " + query)
            webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(query))

    elif "joke" in cmd:
        speak(random.choice(JOKES))

    elif "music" in cmd or "song" in cmd:
        try:
            songs = os.listdir(MUSIC_DIR)
            os.startfile(os.path.join(MUSIC_DIR, random.choice(songs)))  # Windows
            speak("Gaana chala raha hoon")
        except Exception:
            speak("Music folder nahi mila")

    elif "notepad" in cmd:
        os.system("start notepad")

    elif "calculator" in cmd:
        os.system("start calc")

    elif "your name" in cmd:
        speak("Mera naam Jarvis hai")

    elif "how are you" in cmd:
        speak("Main bilkul theek hoon, shukriya")

    elif "stop" in cmd or "exit" in cmd or "bye" in cmd:
        speak("Goodbye, phir milte hain")
        return False

    elif cmd:
        speak("Maaf kijiye, ye command mujhe samajh nahi aaya")

    return True

# ---------- Main loop ----------
if __name__ == "__main__":
    wish()
    running = True
    while running:
        command = listen()
        if command:
            print("You:", command)
        running = handle(command)
