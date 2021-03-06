import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder
from nltk.collocations import TrigramAssocMeasures
from nltk import pos_tag
import random
import re
import json
import sys
import pickle
 
def word_feats(words):
    features = dict([(word, True) for word in words])

    finder = BigramCollocationFinder.from_words(words)
    finder.apply_word_filter(lambda x: False if re.match('\w', x) else True)
    bigrams = finder.nbest(BigramAssocMeasures.chi_sq, 20000)
    features.update(dict([(bigram, True) for bigram in bigrams]))

    #finder = TrigramCollocationFinder.from_words(words)
    #finder.apply_word_filter(lambda x: False if re.match('\w', x) else True)
    #trigrams = finder.nbest(TrigramAssocMeasures.chi_sq, 20000)
    #features.update(dict([(trigram, True) for trigram in trigrams]))

    return features
 
#f = open('review_small.json', 'r')
f = open('review_50000.json', 'r')

pos_data = []
neg_data = []

def get_adjectives(words):
    pos_words = pos_tag(words)
    adjs = [w for w in pos_words if w[1] == 'JJ']
    return adjs

def tokenize(sentence):
    tokens = word_tokenize(sentence.lower())
    return [w for w in tokens if not w in stopwords.words('english')]# and re.match('\w', w)]

read = 0
for line in f:
    read+=1
    if read%1000 == 0:
        print read
    line = eval(line)
    #print line['text']
    tokens = tokenize(line['text'])
    features = word_feats(tokens)


    if line['stars'] >= 3.5:
        pos_data.append((features, 'pos'))
    else:
        neg_data.append((features, 'neg'))

    #tokens = nltk.word_tokenize(line['text'])
    #tagged = nltk.pos_tag(tokens)
    #entities = nltk.chunk.ne_chunk(tagged)

    #leaves = entities.leaves()
    #print leaves

    #nouns = [t[0] for t in leaves if t[1][:2] == "NN"]

    #print nouns

f.close()

pos_size = len(pos_data)
neg_size = len(neg_data)
min_size = min(pos_size, neg_size)

if pos_size > min_size:
    pos_data = random.sample(pos_data, min_size)
elif neg_size > min_size:
    neg_data = random.sample(neg_data, min_size)

pos_limit = len(pos_data)*3/4
neg_limit = len(neg_data)*3/4

train_data = neg_data[:] + pos_data[:]
 
classifier = NaiveBayesClassifier.train(train_data)

f = open('my_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

f_out = open('review_sentiment_50000.json', 'w')
f = open('review_50000.json', 'r')
read = 0
for line in f:
    line = eval(line)
    read+=1
    output_class = classifier.classify(word_feats(tokenize(line['text'])))
    line['predicted_sentiment'] = output_class
    f_out.write(json.dumps(line)+"\n")

classifier.show_most_informative_features()
