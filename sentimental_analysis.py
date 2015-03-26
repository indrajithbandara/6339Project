import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import random
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
f = open('review_small.json', 'r')
pos_data = []
neg_data = []

def tokenize(sentence):
    tokens = word_tokenize(sentence.lower())
    return [w for w in tokens if not w in stopwords.words('english')]

for line in f:
    line = eval(line)
    tokens = tokenize(line['text'])
    features = word_feats(tokens)
    if line['stars'] >= 3.5:
        pos_data.append((features, 'pos'))
    else:
        neg_data.append((features, 'neg'))

pos_size = len(pos_data)
neg_size = len(neg_data)
min_size = min(pos_size, neg_size)

pos_data = random.sample(pos_data, min_size)
neg_data = random.sample(neg_data, min_size)

pos_limit = len(pos_data)*3/4
neg_limit = len(neg_data)*3/4

train_data = neg_data[:neg_limit] + pos_data[:pos_limit]
test_data = neg_data[neg_limit:] + pos_data[pos_limit:]
print 'train on %d instances, test on %d instances' % (len(train_data), len(test_data))
 
classifier = NaiveBayesClassifier.train(train_data)
print 'accuracy:', nltk.classify.util.accuracy(classifier, test_data)
classifier.show_most_informative_features()
