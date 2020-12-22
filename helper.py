import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
words = stopwords.words("english")
def pre_process(corpus):
    corpus = corpus.lower()
    stopset = stopwords.words('english') + list(string.punctuation)
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    corpus = unidecode(corpus)
    return corpus
def lemmatize(corpus):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(corpus)
    new_word_list = []
    for w in words:
        new_word_list.append(lemmatizer.lemmatize(w))
    return new_word_list
