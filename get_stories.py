import json
from urllib.request import urlopen, Request
import traceback
import sys
import requests
import gensim
import random

import utils
import get_topics
import user_interests

def get_stories(id, type):
    ui = user_interests.UserInterests()
    ui.interests = []
    interests = ui.generate_interests_keywords(id)
    interests = ui.generate_interests_keywords(id)

    ALGOLIA_URL = 'https://hn.algolia.com/api/v1/';
    if type == 'top':
        ALGOLIA_URL += 'search?tags=front_page&hitsPerPage=50';
    elif type == 'new':
        ALGOLIA_URL += 'search_by_date?tags=story&hitsPerPage=50';
    elif type == 'show':
        ALGOLIA_URL += 'search_by_date?tags=show_hn&hitsPerPage=50';
    elif type == 'ask':
        ALGOLIA_URL += 'search_by_date?tags=ask_hn&hitsPerPage=50';

    req = Request(ALGOLIA_URL, headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(urlopen(req).read().decode('utf8'))
    
    stories = []
    
    # Shuffle interests
    random.shuffle(interests)

    for i in range(0, len(data['hits'])):
        title = data['hits'][i]['title']
        url = data['hits'][i]['url']
        time = data['hits'][i]['created_at']
        author = data['hits'][i]['author']
        points = data['hits'][i]['points']
        comments_count = data['hits'][i]['num_comments']

        if url == '':
            continue

        if type == 'ask':
            title = title.replace('Ask HN:', '')
        if type == 'show':
            title = title.replace('Show HN:', '')

        words = gensim.utils.simple_preprocess(str(title), deacc=True)

        story = {}
        flag = False
        for word in words:
            word = word.lower()
            for interest in interests:
                if word in interest[1] or utils.stem(word) in interest[1]:
                    story['title'] = title
                    story['url'] = url
                    story['time'] = time
                    story['author'] = author
                    story['points'] = points
                    story['comments'] = comments_count
                    story['topics'] = interest[0]
                    stories.append(story)
                    flag = True
                    break
            if flag:
                break

    return stories[1:]



