from flask import Flask, render_template, request, jsonify
from lu import th2lu
import os
import psutil

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if text := str(request.form['text']):
        result = th2lu(text)
        print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        return jsonify({'result': result})
    return jsonify({'error': 'Missing data!'})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
