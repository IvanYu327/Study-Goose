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
#clean up the intents phrases, tokenizing them into individual words and stemming them to get root words with nltk
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
    patternWords = doc[0]
    patternWords = [stemmer.stem(word.lower()) for word in patternWords]
    for w in words:
        bag.append(1) if w in patternWords else bag.append(0)
    output_row = list(output_empty)
    output_row[classifyingTags.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)


trainX = list(training[:,0])
trainY = list(training[:,1])

#Build neural network, 2 layers 8 nodes
tf.compat.v1.reset_default_graph()


net = tflearn.input_data(shape=[None, len(trainX[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(trainY[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

model.fit(trainX, trainY, n_epoch=1000, batch_size=8, show_metric=True)

#save the model
model.save('model.tflearn')



pickle.dump( {'words':words, 'classifyingTags':classifyingTags, 'trainX':trainX, 'trainY':trainY}, open( "training_data", "wb" ) )
data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classifyingTags = data['classifyingTags']
trainX = data['trainX']
trainY = data['trainY']


with open('intents.json') as json_data:
    intents = json.load(json_data)
    

# load our saved model
model.load('./model.tflearn')

#tokenzie and stem the words in the sentence from the use
def clean_up_sentence(sentence):
    sentenceWords = nltk.word_tokenize(sentence)
    sentenceWords = [stemmer.stem(word.lower()) for word in sentenceWords]
    return sentenceWords

#check for matching words
def loopThroughBag(sentence, words):
    sentenceWords = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentenceWords:
        for i,word in enumerate(words):
            if word == s:
                bag[i] = 1
    return(np.array(bag))

#run the model on the processed input, exclude low probability tags and return a random output from the tag with the highest probability
def classify(sentence):
    results = model.predict([loopThroughBag(sentence, words)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>0.25]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classifyingTags[r[0]], r[1]))
    return return_list

#reponse method
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
