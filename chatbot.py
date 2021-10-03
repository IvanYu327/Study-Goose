import numpy as np
import tensorflow as tf
import tflearn
import random

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import json
import pickle
import warnings
warnings.filterwarnings("ignore")


#read intents
with open('intents.json') as json_data:
    intents = json.load(json_data)


with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)
words = []
classifyingTags = []
documents = []
stringsToIgnore = ['?,!']
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classifyingTags:
            classifyingTags.append(intent['tag'])


words = [stemmer.stem(w.lower()) for w in words if w not in stringsToIgnore]
words = sorted(list(set(words)))

classifyingTags = sorted(list(set(classifyingTags)))



training = []
output = []

output_empty = [0] * len(classifyingTags)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classifyingTags.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)


train_x = list(training[:,0])
train_y = list(training[:,1])

tf.compat.v1.reset_default_graph()


net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)



model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)

model.save('model.tflearn')



pickle.dump( {'words':words, 'classifyingTags':classifyingTags, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )



data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classifyingTags = data['classifyingTags']
train_x = data['train_x']
train_y = data['train_y']


with open('intents.json') as json_data:
    intents = json.load(json_data)
    

model.load('./model.tflearn')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))

def classify(sentence):
    results = model.predict([bow(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>0.25]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classifyingTags[r[0]], r[1])
    return return_list

def response(sentence, userID='123'):
    results = classify(sentence)
    if results:
        while results:
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    
                    temp = random.choice(i['responses'])
                    print("RETURNING "+temp)
                    return temp

            results.pop(0)
