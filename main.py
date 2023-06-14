from flask import Flask, request, jsonify
from chain import ask_llm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/question', methods=['POST'])
def process_question():
    # Retrieve the question from the request
    question = request.json.get('question')
    print(question)

    # Perform some processing or logic based on the question
    answer = ask_llm(question)
    print(type(answer))
    response = {'answer': answer}

    # Return the response as JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)