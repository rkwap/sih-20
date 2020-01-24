import twint
from textblob import TextBlob
from googletrans import Translator
import psycopg2
import json
import emoji

def scrape(search_string):
    tweets = []
    c = twint.Config()
    c.Search = search_string
    c.Limit = 100
    #c.Filter_retweets = True
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    c.Format = "id: {id}"
    twint.run.Search(c)
    return tweets

def Translate(text):
    translator = Translator()
    new_text=translator.translate(text).text
    blob = TextBlob(new_text)
    val = []
    val.append(blob)
    val.append(float(blob.sentiment[0]))
    val.append(float(blob.sentiment[1]))
    return val #returns polarity and subjectivity

def write(search):
    try:
        connect_str = "dbname='sih' user='badboy' host='localhost' password='1234'"
        conn = psycopg2.connect(connect_str)
        cursor = conn.cursor()
        tweets = scrape(search)
        for tweet in tweets:
            string = tweet.tweet
            string = emoji.get_emoji_regexp().sub(u'',string)
            val = Translate(string)
            #query = "insert into twitter values('"+str(tweet.id)+"','"+str(val[0])+"','"+str(val[1])+"','"+str(val[2])+"');"
            query = "INSERT INTO twitter(t_id,tweet,polarity,subjectivity) VALUES (%s,%s,%s,%s)"
            cursor.execute(query,(str(tweet.id),str(val[0]),str(val[1]),str(val[2])))
            conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error Connecting to Database")
        print(e)

if __name__=="__main__":
    search = "CAA"
    write(search)