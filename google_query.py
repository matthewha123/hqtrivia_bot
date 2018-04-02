import requests
from PIL import Image
import pytesseract as pyt
import os
import nltk
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession


pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"


def analyze_text(sess, resp, answer):
    extract = ''
    def extractor(resp_dict):
        nonlocal extract
        if('extract' in resp_dict.keys()):
            #print('hi')
            extract = resp_dict['extract']
            #print(return_dict)
            return
        else:
            #print("Dictionary:", get_dict, "\n")
            for k in resp_dict.keys():
                if(type(resp_dict[k]) == dict):
                    extractor(resp_dict[k])
    extractor(resp.json())
    text = BeautifulSoup(extract, 'html.parser').get_text()

    kw_dict = {kw:0 for kw in keywords}
    count_dict[answer] = kw_dict
    for w in text.split():
        if w in keywords:
            kw_dict[w] += 1
    print(count_dict)

def get_title(sess, resp, answer):
    page = (resp.json()['query']['search'][0]['title'])
    session = FuturesSession()
    session.get('https://en.wikipedia.org/w/api.php?titles='+page+'&action=query&prop=extracts&redirects=1&format=json', 
        background_callback = lambda sess, resp: analyze_text(sess,resp, answer))




raw_text = pyt.image_to_string(Image.open(os.path.join(os.getcwd(),'example_images','img2.png')))
question = ''
empty_question = True
answers = []
count_dict = {}

parts = raw_text.split('\n\n')
for text in parts:
    if '?' in text and len(question) == 0:
        question = ' '.join(text.split('\n'))[:-1]
    elif len(question) != 0:
        answers.append(text)

print('QUESTION: ', question)
print('ANSWERS: ', answers)

keywords = {words for words in question.split() if words not in nltk.corpus.stopwords.words('english')}
print('KEYWORDS: ', keywords)

#TODO don't use wikipedia and do asynchronous requests
# print(wiki.page(wiki.search(answers[0])[0]).content)
session = FuturesSession()

for ans in answers:
    session.get('https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch='+ans+'&utf8&format=json', 
        background_callback = lambda sess,resp: get_title(sess, resp, ans)).result()
# response_one = future_one.result()



#if noun, can search wikipedia
#otherwise, can also d a google search of the question along with the answer
    #ping all the ones
