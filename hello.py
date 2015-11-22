from flask import Flask
from functools import wraps
from flask import request, Response

def check_auth(uname, passwd):
    return uname == 'admin' and passwd == 'admin'

def authenticate():
    return Response('not authorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hellow World, from Nick"

@app.route("/secure")
@requires_auth
def sec():
    return "I'm secure"

if __name__ == "__main__":
    app.run()
