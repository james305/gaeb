from flask import Flask
app = Flask("gaeb")

@app.route('/')
def hello_world():
    return 'Hello Flask!'

if __name__ == '__main__':
    app.run()
