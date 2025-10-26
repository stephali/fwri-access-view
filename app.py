from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Load employees JSON
    with open('data/employees.json') as f:
        employees = json.load(f)
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
