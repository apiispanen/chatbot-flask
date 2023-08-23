# TEACHSERV QUIZBOT
# Author: Drew Piispanen
# Date: 2023-08-01
# Description: This is the main file for the TeachServ QuizBot. It is a Flask app that uses the OpenAI API to generate responses to user input.
# **** For use with TeachServ only ****
# **** All rights reserved ****

from gevent import monkey
monkey.patch_all()


from flask import Flask, jsonify, render_template, request, session
from flask_session import Session
from datetime import datetime
import config
import openai
import json
from dotenv import load_dotenv
from embedder import get_vector_results
import base64
import os
# import transcriber
from flask_cors import CORS
from typing import List, Dict
from schemas import QuizLayout

os.environ['GEVENT_SUPPORT'] = 'True'

# Define a local file path to save the PDF
pdf_path = "temp_pdf_file.pdf"

# Delete the existing file if it exists
if os.path.exists(pdf_path):
    os.remove(pdf_path)


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'some_secret_string'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
pdf_path = None
messages = []
conversation_log = []
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

@app.route('/')
# @app.route('/home')
# def home():
#     # set secret key
#     # session['conversation'] = None
#     # session['chat_history'] = None

#     """Renders the home page."""
#     return render_template(
#         'index.html',
#         title='Home Page',
#         year=datetime.now().year,
#     )



@app.route('/api/vectorize', methods=['POST'])
def vectorize():
    try:
        # Define a local file path to save the PDF
        pdf_path = "temp_pdf_file.pdf"
        
        # Delete the existing file if it exists
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        base64_pdf = request.json['data']
        pdf_data = base64.b64decode(base64_pdf)
        
        with open(pdf_path, 'wb') as f:
            f.write(pdf_data)

        # Now, you can reference the PDF path in your get_vector_results function
        vector_results = get_vector_results('', pdf_path)  # Modify the function accordingly
        print("*******************************vector_results", vector_results)
        return jsonify({"status": "success", "files": vector_results})
    except Exception as e:
        print("*!*!*!*!*!*!*!*!*!*!*!*ERROR:", e)  # Print or log the error for debugging
        return jsonify({"status": "error", "message": str(e)})

# @app.route('/transcribe', methods=['POST'])
# def transcribe():
#     # RETURNS THE TRANSCRIPT OF A VIDEO OR AUDIO FILE
#     url = json.loads(request.data)['url']
#     transcript = transcriber.get_transcription(url)
#     return jsonify({"transcript": transcript})

# ENDPOINT FOR CHATGPT API
@app.route('/MakeQuiz', methods=['POST'])
def MakeQuiz():
    transcript = json.loads(request.data)['transcript']
    print(f"*************TRANSCRIPT RECEIVED **********\n{transcript}")
    message ={"role": "user", "content": f"Make a quiz about the following text:\n{transcript}"}
    conversation_log.append(message)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            message
    ],
    functions=[
        {
          "name": "generate_quiz_questions",
          "description": "Get Quiz Qustions from Text",
          "parameters": QuizLayout.schema()
        }
    ],
    function_call={"name": "generate_quiz_questions"}
    )

    output = json.loads(response.choices[0]["message"]["function_call"]["arguments"])
    print(response)
    conversation_log.append({"role": "bot", "content": output})
    session['conversation_log'] = conversation_log
    return jsonify({'message':output})


# ENDPOINT FOR CHATGPT API
@app.route('/GPTResponse', methods=['POST'])
def ChatGPTWebAPI():
    try:
        print("ChatGPTWebAPI request.data: ", request.json)
        prompt = json.loads(request.data)['prompt']
        print("prompt: ", prompt)
        conversation_log.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=conversation_log,
            temperature=config.temperature,
            stream=False,  # set stream=True
            max_tokens=250
        )
        print("response: ", response)
        session['conversation_log'] = conversation_log

        # query = classification.query_intent(prompt)
        query = "SELECT * FROM table WHERE entities = 'entities'"
        # if entities == ""
        return jsonify({"message": response, "query":query})

    except openai.OpenAIError as e:
        print(e)
        # Check if the exception was due to a timeout
        if "timeout" in str(e).lower():
            return jsonify({"message": config.timeOutErrorMessage})
        # For any other OpenAIError
        return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})
    except Exception as e:
        print(e)
        # For any other exception
        return jsonify({"message": config.anyOtherExceptionErrorMessage, "query":"Error, see logs for details."})



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5555, debug=False, ssl_context=('/etc/letsencrypt/live/aptiversity.com/fullchain.pem', '/etc/letsencrypt/live/aptiversity.com/privkey.pem'))
    except Exception as e:
        print(e)
        app.run(host='0.0.0.0', port=5555, debug=False, ssl_context=('cert.pem', 'key.pem'))

# if __name__ == '__main__':
#     app.run(debug=True, port=os.getenv("PORT", default=5000))

# defaults http://127.0.0.1:5000/api/ChatGPTWebAPITester

# A few functions:
#  1. make multiple choice quiz questions
#  2. make true/false quiz questions
#  3. make fill in the blank quiz questions
#  4. make short answer quiz questions