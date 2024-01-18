import pyttsx3
engine = pyttsx3.init()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import speech_recognition as sr
from knowledge_base import knowledge_base_aud
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
        if flag == True:
            speak('Welcom!\n How can I help you?')
        flag = False
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
            speak(ans)
            break
            
        except sr.UnknownValueError:
            speak('Speech Recognition could not understand the audio. Please try again.')
            break
        except sr.WaitTimeoutError:
            print('No speech detected within the timeout. Please try again.')
            break
if __name__ == '__main__':
    example_qa_pairs = knowledge_base_aud
    aud_bot(example_qa_pairs)