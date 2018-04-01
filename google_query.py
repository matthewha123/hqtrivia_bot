import requests
from PIL import Image
import pytesseract as pyt
import os
import nltk

pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

def send_request():
    raw_text = pyt.image_to_string(Image.open(os.path.join(os.getcwd(),'example_images','img2.png')))
    question = ''
    empty_question = True
    answers = []
    parts = raw_text.split('\n\n')
    for text in parts:
        if '?' in text and len(question) == 0:
            question = ' '.join(text.split('\n'))
        elif len(question) != 0:
            answers.append(text)

    print(question)
    print(answers)

    keywords = {words for words in question.split() if words not in nltk.corpus.stopwords.words('english')}
    print(keywords)


    #if noun, can search wikipedia
    #otherwise, can also d a google search of the question along with the answer
        #ping all the ones
send_request()
