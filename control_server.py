from flask import Flask
from control import *

app = Flask(__name__)

@app.route('/run/<string:command>')
def run_command(command):
    print("Running", command)
    commandMap[command]()
    return 'done'
    


