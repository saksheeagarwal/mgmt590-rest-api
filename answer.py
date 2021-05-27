from transformers.pipelines import pipeline
from flask import Flask
from flask import request
from flask import jsonify
import sqlite3
import json
import time
import os

#Connecting to the database
conn = sqlite3.connect('database.db')
#Creating tables
conn.execute('CREATE TABLE IF NOT EXISTS answered (timestamp DATETIME, model TEXT, answer TEXT, question TEXT, context TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS models (name TEXT, tokenizer TEXT, model TEXT)')

# Create my flask app
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

# Define handler for /models path

@app.route("/models", methods=['DELETE', 'GET', 'PUT'])
def models():
    if request.method == 'GET':
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM models")
            rows = cur.fetchall()
            result = []
            for row in rows:
                out = {
                    "name": row[0],
                    "tokenizer": row[1],
                    "model": row[2]
                }
                result.append(out)
        return (jsonify(result))

    if request.method == 'PUT':
        datar = request.json
        name = datar['name']
        tokenizer = datar['tokenizer']
        model = datar['model']
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO models (name,tokenizer,model) VALUES(?, ?, ?)", (name, tokenizer, model))
            con.commit()
            cur.execute("SELECT * FROM models")
            rows = cur.fetchall()
            result = []
            for row in rows:
                out = {
                    "name": row[0],
                    "tokenizer": row[1],
                    "model": row[2]
                }
                result.append(out)
        return (jsonify(result))

    if request.method == 'DELETE':
        model = request.args.get('model')
        print(model)
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM models WHERE name=?", (model,))
            con.commit()

            #To display output
            cur.execute("SELECT * FROM models")
            rows = cur.fetchall()
            result = []
            for row in rows:
                out = {
                    "name": row[0],
                    "tokenizer": row[1],
                    "model": row[2]
                }
                result.append(out)
        return (jsonify(result))

# Define a handler for the /answer path

@app.route("/answer", methods=['POST', 'GET'])
def answer():
    if request.method == 'POST':
        model_name = request.args.get('model')
        # Get the request body data
        data = request.json
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM models WHERE name=?", (model_name,))
            row = cur.fetchone()
            if row == None:
                return("Model doesn't exist. Please insert the model first.")
            # Import model
            hg_comp = pipeline('question-answering', model=row[2], tokenizer=row[1])

            # Answer the question
            answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']
            timestamp = int(time.time())
            cur.execute("INSERT INTO answered (timestamp, model, answer, question, context ) VALUES(?, ?, ?, ?, ?)",
                        (timestamp, model_name, answer, data['question'], data['context'] ))
            con.commit()
        # Create the response body.
        out = {
            "timestamp": timestamp,
            "model": model_name,
            "answer": answer,
            "question": data['question'],
            "context": data['context']
        }

        return jsonify(out)

    if request.method == 'GET':
        start = request.args.get('start')
        end = request.args.get('end')
        if start==None or end == None:
            return ("Please input start and end time")
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            query = "SELECT * FROM answered where timestamp > ? and timestamp < ?"
            params = [start,end]
            if 'model' in request.args:
                model_name = request.args.get('model')
                query += "and model = ?"
                params += model_name,
            cur.execute(query,params)
            rows = cur.fetchall()
            result = []
            for row in rows:
                out = {
                    "timestamp": row[0],
                    "answer": row[1],
                    "model": row[2],
                    "question":row[3],
                    "context": row[4]
                }
                result.append(out)
        return (jsonify(result))

# Run if running "python answer.py"
if __name__ == '__main__':
    # Run our Flask app and start listening for requests!
    app.run(host='0.0.0.0',port=int(os.environ.get("PORT",8080)), threaded=True)
