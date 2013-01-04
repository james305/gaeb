from flask import Flask, request, jsonify, Response, url_for, render_template
app = Flask("gaeb")

articles = []

from functools import wraps

def check_auth(username, password):
    return username == 'admin' and password == 'secret' # TODO: move to config file

def authenticate(message=''):
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate("Authentication Failed.")
        return f(*args, **kwargs)

    return decorated

@app.route('/')
def list_articles():
    return render_template('blog_list.html', articles=articles)

@app.route('/articles', methods = ['GET'])
@requires_auth
def api_articles():
    return str(articles)

@app.route('/articles', methods = ['POST'])
@requires_auth
def api_post_article():
    articles.append(request.data)
    return 'article ' + str(len(articles)) + ' posted!' + str(request.data)

@app.route('/articles/<int:articleid>', methods = ['GET'])
@requires_auth
def api_article(articleid):
    return 'You are reading ' + articles[articleid]

@app.route('/articles/<int:articleid>', methods = ['DELETE'])
@requires_auth
def api_delete_article(articleid):
    del articles[articleid]
    return 'You have deleted ' + str(articleid)

if __name__ == '__main__':
    app.run()
