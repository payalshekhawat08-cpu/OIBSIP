import datetime
import re
import webbrowser
from urllib.parse import quote_plus

import pyttsx3
import speech_recognition as sr


class MicrophoneUnavailableError(Exception):
    """Report that speech input cannot be used."""


# This function prints each reply and reads it aloud.
def speak(text):
    print(text)
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as error:
        print(f"Text-to-speech is unavailable: {error}")


# This function listens for speech and returns recognized words in lowercase.
def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1.0
    try:
        with sr.Microphone() as microphone:
            recognizer.adjust_for_ambient_noise(microphone, duration=1)
            print("Listening...")
            audio = recognizer.listen(
                microphone,
                timeout=8,
                phrase_time_limit=6,
            )
        text = recognizer.recognize_google(audio, language="en-IN").lower().strip()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError as error:
        print(f"Speech was not understood: {error}")
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
    except sr.WaitTimeoutError as error:
        print(f"Listening timed out: {error}")
    except (OSError, AttributeError) as error:
        print(f"Microphone error: {error}")
        speak("The microphone is unavailable. Please check your microphone.")
        raise MicrophoneUnavailableError from error
    return ""


# This function repeats the prompt until it receives understood speech.
def listen_again():
    while True:
        answer = listen()
        if answer:
            return answer
        speak("Sorry, I didn't catch that. Please repeat.")


# This function handles commands until the user asks the assistant to stop.
def main():
    speak(
        "Hello! I can help with hello, time, date and web search. "
        "Say hello, time, date, search, or exit."
    )

    try:
        while True:
            command = listen()
            if not command:
                speak("Sorry, I didn't catch that. Please repeat.")
                continue

            command_words = set(command.split())

            # Respond to a greeting.
            if command_words.intersection({"hello", "hi", "hey"}):
                speak("Hello! It's nice to talk with you.")

            # Tell the user the current time.
            elif "time" in command_words:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {current_time}.")

            # Tell the user today's date.
            elif command_words.intersection({"date", "day"}):
                today = datetime.datetime.now()
                current_date = f"{today:%A}, {today.day} {today:%B %Y}"
                speak(f"Today is {current_date}.")

            # Search Google using a topic from this sentence or a follow-up.
            elif command_words.intersection({"search", "google"}):
                search_match = re.search(r"\b(?:search|google)\b", command)
                topic = command[search_match.end():].strip(" \t.,!?;:-")
                if topic.startswith("for "):
                    topic = topic[4:].strip()
                if not topic:
                    speak("What should I search for?")
                    topic = listen_again()
                search_url = "https://www.google.com/search?q=" + quote_plus(topic)
                webbrowser.open(search_url)
                speak(f"Here are the search results for {topic}.")

            # Say goodbye and end the assistant.
            elif command_words.intersection({"exit", "stop", "bye", "quit"}):
                speak("Goodbye!")
                break

            # Explain which commands are available.
            else:
                speak("I can help with hello, time, date and web search.")
    except MicrophoneUnavailableError:
        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Goodbye!")