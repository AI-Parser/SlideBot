import pyttsx3

def narrate_slide(title, content):
    engine = pyttsx3.init()
    narration = f"Slide Title: {title}. Content: {content}"
    engine.say(narration)
    engine.runAndWait()
