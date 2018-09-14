import nltk

snow = nltk.stem.SnowballStemmer('english')

def stem(word):
    return snow.stem(word)
