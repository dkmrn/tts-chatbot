import os
from openai import OpenAI
from os import system
import speech_recognition as sr

client = OpenAI(api_key=os.getenv("OPENAI_AI_KEY"))
r = sr.Recognizer()

def getSpeech():
    while True:

        try:

            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input 
                print("Listening...")
                audio2 = r.listen(source2)
                print("Processing...")
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                
                #Print text to screen and speak text
                print("User: ", MyText)
                return MyText
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

def speak(text):
    
    #output text as sound "spoken" by computer
    system("say {}".format(text))

def chatbot():
    messages = [{"role": "system", "content": "You are a helpful assistant."},]
    
    while True:
        
        message = getSpeech()
        if message.lower() == "quit":
            break
        message = message + ". Please respond in less than one paragraph."
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(model = "gpt-3.5-turbo", messages=messages)
        
        chat_message = response.choices[0].message.content
        delimited_message = chat_message
        delimited_message = delimited_message.replace("'","\\'")
        delimited_message = delimited_message.replace("\n"," ")

        print(f"Bot: {delimited_message}")
        speak(delimited_message)

        messages.append({"role": "assistant", "content": chat_message})

if __name__ == "__main__":
    print("Start chatting with the bot (say 'quit' to stop)! ")
    chatbot()