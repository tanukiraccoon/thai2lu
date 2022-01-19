from flask import Flask, render_template, request, jsonify
# from loo import use_loo
from tltk.nlp import th2ipa

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    if name:
        words = name
        # words = th2ipa(words)  # แปลงภาษาไทยเป็น ipa
        result = use_loo(words)
        if result == "error error ":
            return jsonify({'error': 'Missing data!'})
        else:
            return jsonify({'result': result})
    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
