from flask import Flask, request, render_template
import re
import math

app = Flask("__name__")

q = ""

@app.route("/")
def loadPage():
	return render_template('home.html', query="")

def main_form():
	return '<form action="submit" id="textform" method="post"><textarea name="text"></textarea><input type="submit" value="Submit"></form>'

@app.route('/submit', methods=['POST'])
def submit_textarea():

    #List of unique words
	uniqueWords = []

	# store the given text in a variable
	text = request.form.get("text")
	text2 = text.lower()
	text3 = re.sub("[^\w]", " ",text2).split()

	filehandler = open("existingQuery.txt", 'wt')
	filehandler.write(str(text3))
	filehandler.close()

    #Creating a list of uniqueWords from the input query
	for word in text3:
		if word not in uniqueWords:
			uniqueWords.append(word)

	#return render_template('home.html')
	return render_template('home.html', text=text)

@app.route("/", methods=['POST'])
def cosineSim():

    #List of unique words
	uniqueWords = []
    #m implies Percentage of matching between Input text & Database text
	m = 0

	####################################################################################################
	#inputQuery: It is the input query which is entered in the frontend.
	inputQuery = request.form['query']
    #Converting the input query to lower case
	lowercaseQuery = inputQuery.lower()
    #Replace punctuation by space and split
	queryWordList = re.sub("[^\w]", " ",lowercaseQuery).split()

    #Creating a list of uniqueWords from the input query
	for word in queryWordList:
		if word not in uniqueWords:
			uniqueWords.append(word)

	####################################################################################################
    #Reading the existing text present in existingQuery.txt
	fd = open("existingQuery.txt", "r")
    #Converting the text to lower case
	existingQuery = fd.read().lower()
    #Replace punctuation by space and split
	existingQueryList = re.sub("[^\w]", " ",existingQuery).split()

    #Appending more words to the uniqueWords list to create an universal list
	for word in existingQueryList:
		if word not in uniqueWords:
			uniqueWords.append(word)

	####################################################################################################

	queryTF = []
	existingQueryTF = []

	for word in uniqueWords:
		queryTfCounter = 0
		existingQueryTFCounter = 0

		for word2 in queryWordList:
			if word == word2:
				queryTfCounter += 1
		queryTF.append(queryTfCounter)

		for word2 in existingQueryList:
			if word == word2:
				existingQueryTFCounter += 1
		existingQueryTF.append(existingQueryTFCounter)

	dotProduct = 0
	for i in range (len(queryTF)):
		dotProduct += queryTF[i]*existingQueryTF[i]

	queryVectorMagnitude = 0
	for i in range (len(queryTF)):
		queryVectorMagnitude += queryTF[i]**2
	queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

	existingQueryMagnitude = 0
	for i in range (len(existingQueryTF)):
		existingQueryMagnitude += existingQueryTF[i]**2
	existingQueryMagnitude = math.sqrt(existingQueryMagnitude)

	m = (float)(dotProduct / (queryVectorMagnitude * existingQueryMagnitude))*100

	output = "Text of document 2 matches %0.02f%% with the text of document 1."%m

	return render_template('home.html', query=inputQuery, output=output)

app.run()
