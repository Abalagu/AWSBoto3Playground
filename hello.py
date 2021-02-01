# Created by Luming on 1/31/2021 9:46 AM
import boto3
from flask import Flask, render_template, request
from werkzeug.serving import run_simple
import json

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        lambda_client = boto3.client('lambda')
        context = {'email': email}
        payload = json.dumps(context)
        response = lambda_client.invoke(
            FunctionName='ReceiveEmailSubscriptionFlask', InvocationType='Event', Payload=payload)
        print(response)
        return render_template('after_registration.html', context=context)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    run_simple('0.0.0.0', 5001, app, use_reloader=True, use_debugger=True)
