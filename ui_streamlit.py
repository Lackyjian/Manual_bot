import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_bot import get_answer
#from voice_bot import aud_bot
from knowledge_base import knowledge_base_aud, knowledge_base_text
import speech_recognition as sr
import pyttsx3
import time
import keyboard

example_qa_pairs = knowledge_base_text
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())

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
    
def text():
    new_question = question
    new_question = new_question.lower()
    if 'exit' in new_question:
        ans = 'Bot: Bye!'
    else:
        ans = get_answer(new_question, vectorizer, tfidf_matrix, knowledge_base_text)
    return ans

def aud_bot(example_qa_pairs):
    recognizer = sr.Recognizer()
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())
    flag = True
    while True:
        try:
            with sr.Microphone() as source:
                print('Listening:')
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
            words = ans.split()
            for i in range(0, len(words), 5):
                chunk = " ".join(words[i:i+5])
                if keyboard.is_pressed("q"):
                    return
                speak(chunk)
            return ans
            
        except sr.UnknownValueError:
            speak('Speech Recognition could not understand the audio. Please try again.')
            return 'Speech Recognition could not understand the audio. Please try again.'
        except sr.WaitTimeoutError:
            speak('No speech detected within the timeout. Please try again.')
            return 'No speech detected within the timeout. Please try again.'

center_class = "<style>.center { text-align: center; }</style>"

# Create centered header and title with separate divs
header = f"<div class='center'><h1>WELCOME TO ANSH INFOTECH BOT</h1></div>"
title = f"<div class='center'><h3>How can I help you?</h3></div>"

# Use unsafe_allow_html to render the HTML and CSS
st.markdown(f"{center_class}{header}{title}", unsafe_allow_html=True)

st.text('Ask a question by voice input:')
ask_button = st.button('Ask a question')
st.text('or')
question = st.text_input('Type a question:')
text_ans_button = st.button('Get Answer') 
placeholder = st.empty()
if ask_button:
    placeholder.text('Listening...')
    placeholder.text(aud_bot(knowledge_base_aud))
    #placeholder.text('Bye!')

if text_ans_button:
    placeholder.text(text())



