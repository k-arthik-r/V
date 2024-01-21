from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
import requests
import random
from openai import OpenAI
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)
openai_client = OpenAI()

translate_api_url = ''
chatbot_api_url = ''



client = MongoClient(config['DATABASE']['STRING'])
db = client[config['DATABASE']['DATABASE_NAME']]
collection = db[config['DATABASE']['COLLECTION_LOGIN']]


@app.route('/')
def login():
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/aboutk')
def aboutk():
    return render_template('aboutk.html')

@app.route('/diseasePrediction')
def diseasePrediction():
    return render_template('2options.html')

@app.route('/prediction1')
def prediction1():
    return render_template('prediction.html')

@app.route('/mcq')
def mcq():
    return render_template('mcq.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/predic')
def predic():
    return render_template('predic.html')

@app.route('/ask', methods=['POST'])
def ask():
    questions = request.get_json().get('question')
    response = requests.post(f"{chatbot_api_url}/input_bot", json={'questions': questions})
    if response.status_code == 200:
        answers = response.json().get('answer')
        return jsonify({'answers': answers})
    else:
        return jsonify({'error': 'Failed to get answers'})

@app.route('/mcqfun1', methods=["GET", "POST"])
def mcqfun1():
    if request.method == "POST":
        list = ['Depression', 'Anxiety Disorders', 'Schizophrenia', 'Bipolar Disorder', 'Obsessive-Compulsive Disorder (OCD)', 'Post-Traumatic Stress Disorder(PTSD)']
        symp = random.choices(list)
    return render_template('predic.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    texts = data.get('texts', [])
    target_lang = data.get('target_lang', 'en')

    response = requests.post(f"{translate_api_url}/translate", json={'texts': texts, 'target_lang': target_lang})

    if response.status_code == 200:
        translated_texts = response.json().get('translated_texts', [])
        return jsonify({'translated_texts': translated_texts})
    else:
        return jsonify({'error': 'Failed to get translation'})


@app.route("/loginsuccessfull", methods=["GET", "POST"])
def validate_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        required_one = {
            "_id": username, "password": password
        }
        data = collection.find_one(required_one)
        print(data)
        if data:
            return render_template('dashboard.html')
        else:
            return render_template('index.html')
    return render_template('index.html')

@app.route("/userfeeling", methods=["GET", "POST"])
def userfeeling():
    if request.method == "POST":
        userfeeling = request.form["feeling"]


        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Consider the given feeling, analyze it and classify it into one of these categories: None, Depression, Anxiety Disorders, Schizophrenia, Bipolar Disorder, Obsessive-Compulsive Disorder (OCD), and Post-Traumatic Stress Disorder (PTSD). Give me only the name of the label, not the explanation."},
                {"role": "user", "content": userfeeling}
            ]
        )

        symptom = completion.choices[0].message.content
        print(symptom)


        existing_student = collection.find_one({'_id': 'karthik'})
        if existing_student:
            
            collection.update_one(
                
                {'_id': 'karthik'},
                {'$set': {'symptom': symptom}}
            )      

        return render_template('prediction.html', symptom = symptom)
    else:
        return render_template('prediction.html', symptom = None)

@app.route("/predict2")
def predict2():
    return render_template('prediction.html')
        
if __name__ == '__main__':
    app.run(debug = True)

