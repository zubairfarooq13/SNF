import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
def cleaning(data):
        for k in data.split("\n"):
            clean_data = (''.join(re.sub(r"[^a-zA-Z0-9]+", ' ', k)))
            return clean_data
            
def get_token(data):
        tokens=nltk.word_tokenize(data)
        return tokens
        
def get_stopWords(data):
        en_stops = set(stopwords.words('english'))
        list_stopwords = []
        for stopword in data:
            if stopword not in en_stops:
#               print(stopword)
               list_stopwords.append(stopword)
        return list_stopwords
        
def get_stemming(data):
        porter_stemmer = PorterStemmer()
        list_stemming_words = []
        for w_port in data:
           stemming_words=porter_stemmer.stem(w_port)
           list_stemming_words.append(stemming_words)
           #print(self.stemming_words)
           
        return ' '.join(list_stemming_words)
