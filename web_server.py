from flask import Flask, request
from resources import EntryManager
from resources import Entry
import os
#FOLDER = '/tmp/'
FOLDER = r'C:\Users\Alena\Desktop\spain'
#https://voitixler.com/course/coding/todo-frontend/

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/entries/")
def get_entries():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entry_list = []
    for i in entry_manager.entries:
        entry = Entry(i)
        entry_list.append(entry.json())
    return entry_list

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    json_data = request.get_json()
    for i in json_data:
        ex = Entry.from_json(i)
        entry_manager.entries.append(ex)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)