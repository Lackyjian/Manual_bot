
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from voice_bot import aud_bot
tk = Tk()
option = IntVar()
def start():
    new_window = Toplevel(tk)
    option_ = int(option.get())
    if(option_ == 1):
        print(option)
    if(option_ == 2):
        print(option)
        start_button = Button(new_window, text="Start", command=aud)
        start_button.pack()

def aud():
    aud_bot(knowledge_base)

choose_label = Label(tk, text="Choose your choice:")
choose_label.pack()


option1 = Radiobutton(tk, text="Text Based Chatbot", value=1, var = option)
option1.pack()

option2 = Radiobutton(tk, text="Voice Based Chatbot", value=2, var = option)
option2.pack()

start_button = Button(tk, text="Start", command=start)
start_button.pack()

knowledge_base = {
    "What courses do you offer or are available?": "AI, ML, Web & Mobile App Development, Cybersecurity, Digital Marketing, and Training.",
    "What are the timings?": "10am to 1 pm",
    "What is the fees structure": "10000/- for 6 month course.",
    "how to contact you": "you can contact us at contact@anshinfotech.org",
    "How to enroll for course": "you can enroll by fillinf the form by clicking here https://anshinfotech.org/registerform.php"
    }

tk.mainloop()

# while(True):
#     print("1. Text Based Chatbot")
#     print("2. Voice Based Chatbot")
#     print("3. Exit")
#     choice = int(input("Enter your choice: "))
#     if choice == 1:
#        text_bot(knowledge_base)
#     elif choice == 2:
#        aud_bot(knowledge_base)
#     elif choice == 3:
#        break
#     else:
#        print("Invalid choice. Please try again.")