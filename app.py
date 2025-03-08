""""application"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/model-report')
def modelReport():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)