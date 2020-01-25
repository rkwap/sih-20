from app import *
youtube = Blueprint('youtube', __name__,url_prefix='/scrape/youtube')
youtube_id=''

@youtube.route('/<string:yt_id>/', methods=["GET","POST"])
def yt_search_url(yt_id):
    youtube_id=yt_id
    limit=10
    count=0
    data=[]
    for comment in download_comments(youtube_id):
        c_id=str(comment['cid'])
        check_comment=query_db("SELECT id from youtube WHERE c_id=%s", (c_id,))
        if len(check_comment)==0:
            # calculating sentiment and storing
            text=str(comment['text'])
            sentiment=getMixedSentiment(str(comment['text']))
            polarity=str(sentiment.polarity)
            subjectivity=str(sentiment.subjectivity)
            execute_db("INSERT INTO youtube(id,c_id,text,polarity,subjectivity) VALUES (%s,%s,%s,%s,%s)",(
                        yt_id,
                        c_id,
                        text,
                        polarity,
                        subjectivity,
                    ))
                    
        # retrieving data from db
        data.append(query_db("SELECT * FROM youtube WHERE c_id=%s", (c_id,)))
        count+=1
        if limit and count>=limit:
            break
    count=query_db("SELECT count(c_id) FROM youtube")
    polarities=query_db("SELECT polarity FROM youtube")
    total_polarities=[p for p in polarities]
    total_polarity=0
    for x in total_polarities:
        total_polarity+=float(x[0])
    return render_template("index.html", **locals())


YOUTUBE_COMMENTS_URL = 'https://www.youtube.com/all_comments?v={youtube_id}'
YOUTUBE_COMMENTS_AJAX_URL = 'https://www.youtube.com/comment_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

def find_value(html, key, num_chars=2):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find('"', pos_begin)
    return html[pos_begin: pos_end]

def extract_comments(html):
    tree = lxml.html.fromstring(html)
    item_sel = CSSSelector('.comment-item')
    text_sel = CSSSelector('.comment-text-content')

    for item in item_sel(tree):
        yield {'cid': item.get('data-cid'),
               'text': text_sel(item)[0].text_content()}

def extract_reply_cids(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.comment-replies-header > .load-comments')
    return [i.get('data-cid') for i in sel(tree)]

def ajax_request(session, url, params, data, retries=500, sleep=0):
    for _ in range(retries):
        response = session.post(url, params=params, data=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict.get('page_token', None), response_dict['html_content']
        else:
            time.sleep(sleep)

def download_comments(youtube_id, sleep=0):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT

    # Get Youtube page with initial comments
    response = session.get(YOUTUBE_COMMENTS_URL.format(youtube_id=youtube_id))
    html = response.text
    reply_cids = extract_reply_cids(html)

    ret_cids = []
    for comment in extract_comments(html):
        ret_cids.append(comment['cid'])
        yield comment

    page_token = find_value(html, 'data-token')
    session_token = find_value(html, 'XSRF_TOKEN', 4)

    first_iteration = True

    # Get remaining comments (the same as pressing the 'Show more' button)
    while page_token:
        data = {'video_id': youtube_id,
                'session_token': session_token}

        params = {'action_load_comments': 1,
                  'order_by_time': True,
                  'filter': youtube_id}

        if first_iteration:
            params['order_menu'] = True
        else:
            data['page_token'] = page_token

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        page_token, html = response

        reply_cids += extract_reply_cids(html)
        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment

        first_iteration = False
        time.sleep(sleep)

    # Get replies (the same as pressing the 'View all X replies' link)
    for cid in reply_cids:
        data = {'comment_id': cid,
                'video_id': youtube_id,
                'can_reply': 1,
                'session_token': session_token}

        params = {'action_load_replies': 1,
                  'order_by_time': True,
                  'filter': youtube_id,
                  'tab': 'inbox'}

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
        if not response:
            break

        _, html = response

        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment
        time.sleep(sleep)