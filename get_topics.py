import json
from urllib.request import urlopen, Request
import traceback
import sys
import requests


from nltk.corpus import stopwords
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
import re, string

stop = stopwords.words('english') + list(string.punctuation)
stop.extend(['from', 'subject', 're', 'edu', 'use'])

def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop] for doc in texts]

def make_bigrams(unseen_bigram_mod, texts):
    return [unseen_bigram_mod[doc] for doc in texts]

def get_topics(userid):
    # Get submission by userid made after Jan 1, 2018
    URL = 'http://hn.algolia.com/api/v1/search?tags=story,author_' + userid
    URL = URL + '&numericFilters=created_at_i>1516006858&hitsPerPage=100'
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    data_dict = json.loads(urlopen(req).read().decode('utf8'))
    unseen_docs = []

    for i in range(0, len(data_dict['hits'])):
        unseen_docs.append(data_dict['hits'][i]['title'])
    
    # Remove newline characters
    unseen_docs = [re.sub('\s+', ' ', sent) for sent in unseen_docs]
    # Remove single quotes
    unseen_docs = [re.sub("\'", "", sent) for sent in unseen_docs]

    unseen_data_words = list(sent_to_words(unseen_docs))

    # Build the bigram model
    # higher threshold fewer phrases. 
    unseen_words_bigram = gensim.models.Phrases(unseen_data_words, min_count=5, threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    unseen_words_bigram_mod = gensim.models.phrases.Phraser(unseen_words_bigram)

    # Remove Stop Words
    unseen_data_words_nostops = remove_stopwords(unseen_data_words)

    # Form Bigrams
    unseen_data_words_bigrams = make_bigrams(unseen_words_bigram_mod, unseen_data_words_nostops)

    # Create Dictionary
    id2word = corpora.Dictionary(unseen_data_words_bigrams)

    # Create Corpus
    texts = unseen_data_words_bigrams

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # mallet_path = '/home/vivek/Documents/HN_For_You/mallet-2.0.8/bin/mallet'
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus,
          num_topics=10, id2word=id2word, iterations=1000)

    topics = lda.show_topics(num_topics=10, num_words=10, formatted=False)
    return topics