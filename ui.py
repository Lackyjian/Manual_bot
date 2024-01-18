from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_bot import get_answer
#from voice_bot import aud_bot
from knowledge_base import knowledge_base_aud, knowledge_base_text
import speech_recognition as sr
import pyttsx3
import time
import keyboard
engine = pyttsx3.init()

tk = Tk()
def mic():
    aud_bot(knowledge_base_aud) 

base_label = Label(tk, text="How can I help you?")
base_label.pack()

ask_label = Label(tk, text="Ask a question by voice input")
ask_label.pack()

def text():
    new_question = question.get()
    new_question = new_question.lower()
    if 'exit' in new_question:
        ans = 'Bot: Bye!'
        answer_text.config(text=ans)
    else:
        ans = get_answer(new_question, vectorizer, tfidf_matrix, knowledge_base_text)
        answer_text.config(text=ans)
        #tk.after(1000, text) 
example_qa_pairs = knowledge_base_text
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())

start_button = Button(tk, text="Ask a question", command=mic)
start_button.pack()

type_label = Label(tk, text="or\nType a question:")
type_label.pack()

question = Entry(tk)
question.pack()

ask_button = Button(tk, text="Get Answer", command=text)
ask_button.pack()

answer_text = Label(tk)
answer_text.pack()


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 185)
    engine.say(text)
    engine.runAndWait()

def get_answer(question, vectorizer, tfidf_matrix,example_qa_pairs):
    similarity_scores = cosine_similarity(vectorizer.transform([question]), tfidf_matrix)
    most_similar_index = similarity_scores.argmax()
    if similarity_scores[0, most_similar_index]>0.2:
        most_similar_question = list(example_qa_pairs.keys())[most_similar_index]
        most_similar_answer = example_qa_pairs[most_similar_question]
        return most_similar_answer
    else:
        return 'Sorry, I don\'t have an answer for that question. Try rephrasing it.'

def aud_bot(example_qa_pairs):
    recognizer = sr.Recognizer()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())
    flag = True
    while True:
        try:
            with sr.Microphone() as source:
                print('Listening:')
                answer_text.config(text='Listening...')
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=3)
                new_question = recognizer.recognize_google(audio)
            # new_question = input('User: ')
            print('User:', new_question)
            new_question = new_question.lower()
            if 'exit' in new_question:
                speak('Bye!')
                break
            ans = get_answer(new_question, vectorizer, tfidf_matrix, example_qa_pairs)
            answer_text.config(text=ans)
            words = ans.split()
            for i in range(0, len(words), 5):
                chunk = " ".join(words[i:i+5])
                if keyboard.is_pressed("q"):
                    break
                speak(chunk)
            break
            
        except sr.UnknownValueError:
            speak('Speech Recognition could not understand the audio. Please try again.')
            break
        except sr.WaitTimeoutError:
            speak('No speech detected within the timeout. Please try again.')
            break

tk.mainloop()