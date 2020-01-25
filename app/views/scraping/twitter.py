from app import *
twitter = Blueprint('twitter', __name__,url_prefix='/scrape/twitter')

@twitter.route('/<string:q>/', methods=["GET","POST"])
def twitter_search_url(q):
    data=[]
    tweets = scrape(q)
    for tweet in tweets:
        t_id=tweet.id
        check_comment=query_db("SELECT t_id from twitter WHERE t_id=%s", (t_id,))
        if len(check_comment)==0:
            text = str(tweet.tweet)
            sentiment=getMixedSentiment(text)
            polarity=str(sentiment.polarity)
            subjectivity=str(sentiment.subjectivity)
            execute_db("INSERT INTO twitter(t_id,tweet,polarity,subjectivity) VALUES (%s,%s,%s,%s)",(
                        t_id,
                        text,
                        polarity,
                        subjectivity,
                    ))
        data.append(query_db("SELECT * FROM twitter WHERE t_id=%s", (t_id,)))

    print(data)
    return render_template("index.html", **locals())


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
