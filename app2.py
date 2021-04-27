from flask import Flask
app = Flask(__name__)
@app.route('/test')
def goodbye_world():
    print('googbye, cruel world.')

