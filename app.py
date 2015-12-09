from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def user_details(username):
    return "Your username is " + username

if __name__ == '__main__':
    app.run(host='0.0.0.0')
