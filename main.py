from app import *
from textblob import TextBlob
from googletrans import Translator

translator = Translator()
text='''
ఈ పాట విన్న తరువాత నాకు ఒకటి అనిపించింది
నాన్న కోసం మన ప్రాణం ఇచ్చిన కూడా తక్కువే అనిపిస్తుంది 😢😢
'''

text=deEmojify(text)
new_text=translator.translate(text).text
blob = TextBlob(new_text)
print(blob.sentiment)


# # for sentence in blob.sentences:
#     # print(sentence)
#     # print(sentence.sentiment)
