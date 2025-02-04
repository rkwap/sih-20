from app import *
# from .main import saveReviews
flipkart = Blueprint('flipkart',__name__,url_prefix='/scrap/flipkart')


@flipkart.route("/hello/", methods=['POST', 'GET'])
def hello():
    print("#########")
    return 0


@flipkart.route("/reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    data = []
    
    products = query_db("SELECT * from products WHERE pid=%s", (pid,))
    reviews = query_db("SELECT pid from reviews WHERE pid=%s", (pid,))

    if not products or not reviews:
        for _ in range(1):
            page = requests.get('https://www.flipkart.com/q/product-reviews/q?pid='+pid)
            soup = BeautifulSoup(page.text, 'html.parser')
            pos1 = int(str(soup).find('\"readReviewsPage\":'))
            pos2 = int(str(soup).find('\"recentlyViewed\"'))
            string = '{'+str(soup)[pos1:pos2]+'}rk'
            string = string.replace("}}},}rk","}}}}")
            string = json.loads(string)
            string = string['readReviewsPage']['reviewsData']['product_review_page_default_1']['data']
            for s in string:
                blob = TextBlob(s['value']['text'])
                execute_db("INSERT INTO reviews(pid,text,title,polarity,date) VALUES (%s,%s,%s,%s,%s)",(
                    pid,
                    s['value']['text'],
                    s['value']['title'],
                    blob.sentiment.polarity,
                    s['value']['created'],
                ))
    data =[]

    reviews = query_db("SELECT * from reviews WHERE pid=%s", (pid,))
    positive = 0
    negative = 0
    slightly_negative = 0
    slightly_positive = 0
    neutral = 0
    # print(reviews)
    for r in reviews:
        keys=['pid','title','text','created','polarity']
        values = [r[1],r[2],r[3],r[5],r[4]]
        if r[4]>0.5:
            positive+=1
        elif r[4]<0.5 and r[4]>0:
            slightly_positive+=1
        elif r[4]==0:
            neutral+=1
        elif r[4]>-0.5 and r[4]<0:
            slightly_negative+=1
        else:
            negative+=1
        data.append([dict(zip(keys,values))])

    reviews = {"results": data, "positive": positive, "negative": negative, "neutral": neutral, "slightly_positive":slightly_positive, "slightly_negative":slightly_negative}
    return jsonify(reviews)


# @flipkart.route("results/<string:q>", methods=['POST', 'GET'])
# def getResults(q):
#     results = True
#     p_name=[]
#     p_url=[]
#     p_id=[]
#     trust_value=[]
#     page = requests.get('https://www.flipkart.com/search?q='+q)
#     soup = BeautifulSoup(page.text, 'html.parser')
#     string = soup.find('script', {'id':'jsonLD'}).text
#     string = json.loads(string)
#     string = string['itemListElement']
#     query = ' '.join(q.split('+'))
#     polarities = []
#     for s in string:
#         p_name.append(s['name'])
#         p_url.append(s['url'])
#         pos1 = str(s['url']).find('?pid=')
#         pos2 = str(s['url']).find('&lid=')
#         id = str(s['url'])[pos1:pos2]
#         id = id.replace('?pid=','').replace('&lid=','')
#         p_id.append(id)
#         products_chk = query_db("SELECT pid from products WHERE pid=%s", (id,))
#         if not products_chk:
#             execute_db("INSERT INTO products(pid,name,url) VALUES (%s,%s,%s)",(id,s['name'],s['url'],))
#             saveReviews(id)

#         polarity=query_db("SELECT polarity from reviews WHERE pid=%s", (id,))
#         polarity_ = []
#         for review in polarity:
#              for poles in review:
#                 polarity_.append(round(poles, 4))
#         tv = query_db("SELECT AVG(polarity) FROM reviews WHERE pid=%s",(id,))
#         if tv[0][0] is not None:
#             trust_value.append(round(tv[0][0],2))
#         polarities.append(polarity_)
#     data = zip(p_name,p_id,p_url,trust_value)
#     return render_template('results.html',**locals())
