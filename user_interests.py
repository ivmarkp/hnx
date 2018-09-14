import _pickle as cPickle
import requests, ast
from collections import OrderedDict

import properties
import get_topics
import utils

class UserInterests:
    # Stores a list of ref topics
    ref_topics = ''

    # Stores an array of user interests tuples
    interests = []

    """
    Get reference topics from gist and store into a list of
    OrderedDict.
    """
    def get_ref_topics(self):
        response = requests.get(properties.REF_TOPICS_URL)
        data = response.content
        data = eval(data)
        
        data_tuples = []
        
        for t in range(0, len(data)):
            item_dict = {}
            annotations = data[t][0]
            for k in range(0, len(data[t][1])):
                key = data[t][1][k][0]
                score = data[t][1][k][1]
                item_dict[key] = score
            data_tuples.append((annotations, item_dict))

        self.ref_topics = data_tuples[1:]
    
    """
    Infers interests through simple keyword matching
    """
    def generate_interests_keywords(self, userid):
        # Initialise ref_topics
        self.get_ref_topics()
        
        # Get top-10 user topics
        user_topics = get_topics.get_topics(userid)

        # Get top-20 keywords
        top20_keywords = []
        for i in range(len(user_topics)):
            for j in range(0, 2):
                top20_keywords.append(utils.stem(user_topics[i][1][j][0]))

        # Fit top-20 keywords in ref_topics to get interests keywords
        for i in range(0, len(top20_keywords)):
            keyword = top20_keywords[i]
            for j in range(0, len(self.ref_topics)):
                if keyword in self.ref_topics[j][1]:
                    self.interests.append(self.ref_topics[j])
        
        return self.interests
