# ChatBot

Chat AI GUI using PySimpleGUI.Using the tensorflow-tflearn model, this is a chatbot framework that takes in a user input and processes a response accordingly and accurately, with the ability to handle contexual responses. 

<center>
  <h3>Example Image</h3>
  <img src="https://user-images.githubusercontent.com/62800170/154606145-51be647d-3546-424e-8a16-3b202d0eab9c.png" alt="Sample Image" width="40%"/>
</center>

## How the AI Framework works

In ```setup.py```, it will break up the json file into tags, unique keywords, and sentences with the tags. It will then stem each keyword to take away the unnecessary letters to provide a more accurate answer, and covert each pattern for each tag into a bag-of-words model allowing the AI to each word into a numbers to describe the occurence of words for a specific tag. 

Lastly, it performs its "training" by processing all the information extracted into Neural Networks using tflearn to determine predictions and probability which aims for the best possible output. It does so by taking in an input data (in this case, bag of words for each keywords per tag), makes a prediction and compares the prediction to the desired output (the output being the respective tag).

## How the AI processes user input

Given the user input, it will put the imput into a bag-of-words and create an array of probabilities (with respect to the tags) given the bag-of-words. Get the tag in respect to the index of the highest probability, and go through all the intents until the respective tag is found. If found provide a response, otherwise a default response is sent. 

## How to add more to the bot

Inside the json file, when creating a new intent, the mandatory tags are ```tag, keywords, responses```. Follow the same format to what is already there. 

For contextual, add the tag ```context_set``` with ```context_response``` in respect to the name of ```context_set```. Follow the knock knock joke tag for an example.

## Required Modules
```
pip install tensorflow
pip install tflearn
pip install PySimpleGUI
pip install numpy
pip install pickle
pip install nltk
```

## Documents used as reference to help implement the AI
<a href="https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077" targer="_blank">Contextual Chatbots with Tensorflow</a>

<a href="https://chatbotslife.com/deep-learning-in-7-lines-of-code-7879a8ef8cfb" targer="_blank">Learn more about deep learning</a>

## Credits
Author: Anthony Massaad

Copyright © 2022. All rights reserved
