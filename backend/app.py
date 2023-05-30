import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv('.env')

app = Flask(__name__)
CORS(app)

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("GPTKEY")


'''messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]'''

def promptGPT(data):
    messages = data['messages']
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, max_tokens=1000)
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']


@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    print(data)
    # result = []
    # for key in data:
    #     result.append([key, data[key]])
    return jsonify(promptGPT(data))


@app.route('/')
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)



