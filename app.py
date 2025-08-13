from flask import Flask, request

app = Flask(__name__)

@app.route('/')
async def index():
    return 'Hello'


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, True)
