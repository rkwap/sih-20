from app import *
from textblob import TextBlob
from googletrans import Translator

translator = Translator()
text='''
Maaf Karo yar , aaj subah tak patanhi tha that I wudnt be able to come today :( 
'''
new_text=translator.translate(text).text
print(new_text)
blob = TextBlob(new_text)
print(blob.sentiment)

# # for sentence in blob.sentences:
#     # print(sentence)
#     # print(sentence.sentiment)
