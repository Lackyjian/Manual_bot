from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Dictionary of example questions and answers


def get_answer(question, vectorizer, tfidf_matrix,example_qa_pairs):
    similarity_scores = cosine_similarity(vectorizer.transform([question]), tfidf_matrix)
    most_similar_index = similarity_scores.argmax()
    if similarity_scores[0, most_similar_index]>0.2:
        most_similar_question = list(example_qa_pairs.keys())[most_similar_index]
        most_similar_answer = example_qa_pairs[most_similar_question]
        return most_similar_answer
    else:
        return 'Sorry, I don\'t have an answer for that question. Try rephrasing it.'

def text_bot(example_qa_pairs):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())
    flag = True
    while True:
        if flag == True:
            print('Bot:Welcom!\n How can I help you?')
        flag = False
        new_question = input('User: ')
        new_question = new_question.lower()
        if('exit' in new_question):
            print('Bot: Bye!')
            break
        print('Bot:',get_answer(new_question, vectorizer, tfidf_matrix, example_qa_pairs))

if __name__ == '__main__':
    example_qa_pairs = {
    "What courses do you offer or are available?": "AI, ML, Web & Mobile App Development, Cybersecurity, Digital Marketing, and Training.",
    "What are the timings?": "10am to 1 pm",
    "What is the fees structure": "10000/- for 6 month course.",
    "how to contact you": "you can contact us at contact@anshinfotech.org",
    "How to enroll for course": "you can enroll by fillinf the form by clicking here https://anshinfotech.org/registerform.php"
    }
    #vectorizer = TfidfVectorizer()
    #tfidf_matrix = vectorizer.fit_transform(example_qa_pairs.keys())
    text_bot(example_qa_pairs)