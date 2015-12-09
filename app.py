from flask import Flask, send_from_directory, render_template
app = Flask(__name__, static_url_path='/static/')
app.debug = True

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/user/<username>')
def user_details(username):
    return "Your username is " + username

if __name__ == '__main__':
    app.run(host='0.0.0.0')
