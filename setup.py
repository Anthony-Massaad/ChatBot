import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
from tensorflow.python.framework import ops
import random
import json
import pickle
# needed to break down each word in the patterns
# to the root of the word (i.e 'there?' -> 'ther')
stemmer = LancasterStemmer()
nltk.download('punkt')

## CONSTANTS ##
INTENT = "intents"
PATTERN = "patterns"
RESPONSE = "responses"
TAG = "tag"
CONTEXT_SET = "context_set"
CONTEXT_RESPONSE = "context_response"


class Chatty:

    def __init__(self):
        self.keywords = []
        self.tags = []
        self.sentences_by_tag = []
        self.training = []
        self.output = []
        self.model = None
        self.context = {}
        with open("Bot_Data.json") as file:
            self.data = json.load(file)
        try:
            with open("Bot_Data.pickle", "rb") as f:
                self.keywords, self.tags, self.training, self.output = pickle.load(f)
        except:
            self.setup()
        print(self.training, self.output, self.keywords, self.tags)
        self.create_model()

    def setup(self) -> None:
        # Loop to collect all patterns and tags accordingly
        for intent in self.data[INTENT]:
            for pattern in intent[PATTERN]:
                # tokenize to split all the sentences into separate words
                unique_words = nltk.word_tokenize(pattern)
                # appends the unique words into the list of key words
                self.keywords.extend(unique_words)
                # Adds a touble populated by (tag, unique key words) into the list of sentences by tag
                self.sentences_by_tag.append((intent[TAG], unique_words))

            if intent[TAG] not in self.tags:
                self.tags.append(intent[TAG])
        # Stem the words for all unique words to take out the unnessary letters
        # and match words with similar meaning (i.e., 'tak' will match with taking, take, takers..etc)
        self.keywords = [stemmer.stem(w.lower()) for w in self.keywords if w != '?']
        self.keywords = sorted(list(set(self.keywords)))
        self.tags = sorted(self.tags)
        # loop to bag each unique word into bag of numbers to work with tensorflow
        # It is to simplify the natural modern language into data numbers that can be 
        # retrieved by the AI later
        for i, sentence_by_tag in enumerate(self.sentences_by_tag):
            bag = []
            # for each word in the pattern, stem it
            wrds = [stemmer.stem(w) for w in sentence_by_tag[1]]
            # create the bag of words. 1 if the keyword exist in the word list for a tag 
            # 0 otherwise
            for w in self.keywords:
                if w in wrds:
                    bag.append(1)
                    continue
                bag.append(0)
            # output is a 0 for each tag and 1 for each current tag
            output_row = [0 for x in range(len(self.tags))]
            output_row[self.tags.index(sentence_by_tag[0])] = 1

            # add the bag to the training and output_row to the ouput
            self.training.append(bag)
            self.output.append(output_row)

        self.training = np.array(self.training)
        self.output = np.array(self.output)

        with open("Bot_Data.pickle", "wb") as f:
            pickle.dump((self.keywords, self.tags, self.training, self.output), f)

    def create_model(self) -> None:
        """
        Using tflearn, we create a neuron network 

        """
        # set up the tensorflow model
        # reset the graph data
        ops.reset_default_graph()
        # Build neural network
        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        # Define model and setup tensor board using tflearn
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)
        self.model = tflearn.DNN(net)
        # how many times the AI will look at the data and train itself for more accuracy
        self.model.fit(self.training, self.output, n_epoch=1000, batch_size=8, show_metric=False)
        self.model.save("chatBotModel.tflearn")

    def get_response(self, sentence: str) -> str:
        """
        Generate a response given the user input 
        :param sentence: String, the setence
        :return: response as a string
        """
        CONTEXT_ID = "123456789"
        context_set_changed = False
        # bag the user input to get the most probable tag
        bag = [0]*len(self.keywords)
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]

        for sentence in sentence_words:
            for i, word in enumerate(self.keywords):
                if word == sentence:
                    bag[i] = 1

        # Generate probabilities
        prob_result = self.model.predict([np.array(bag)])[0]
        # Get the appropriate tag based on highest probability and generate response accordingly
        highest_prob_result = np.argmax(prob_result)
        tag = self.tags[highest_prob_result]
        responses = []
        for i, tg in enumerate(self.data[INTENT]):
            if tg[TAG] == tag:
                if CONTEXT_RESPONSE not in tg or (CONTEXT_ID in self.context and CONTEXT_RESPONSE in tg and tg[CONTEXT_RESPONSE] == self.context[CONTEXT_ID]):
                    responses = tg[RESPONSE]
                
                if CONTEXT_SET in tg:
                    self.context[CONTEXT_ID] = tg[CONTEXT_SET]
                    context_set_changed = True

            if i+1 == len(self.data[INTENT]) and context_set_changed is False:
                self.context = {}

        if responses:
            return random.choice(responses)

        return "Sorry, I don't have a response just yet"

