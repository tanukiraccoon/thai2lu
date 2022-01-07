from flask import Flask, render_template, request, jsonify
from loo import use_loo

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    if name:
        words = name
        result = use_loo(words)
        newName = result
        return jsonify({'name': newName})
    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
