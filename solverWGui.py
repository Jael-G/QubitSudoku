from flask import Flask, render_template, request
from flaskwebgui import FlaskUI
import sudokuWFCSolver
import json

BROWSER_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" #Default chrome path, comment out if using another browser
sudokuWFCSolver.MAX_ATTEMPTS = 10000

app = Flask(__name__)

@app.route('/',  methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/solve_sudoku', methods=['POST'])
def solve_sudoku():
    array = request.json['sudokuArray']
    converted_data = [[int(val) for val in sublist] for sublist in array]
    
    #Set solved to False. Otherwise it will remain True and the solver will work once
    sudokuWFCSolver.SOLVED = False
    temp_array = sudokuWFCSolver.copy_array(converted_data)
    solved_array = sudokuWFCSolver.solver_thread(temp_array)

    response = json.dumps({"solvedArray":solved_array})
    
    return response

if __name__ == '__main__':
    # app.run(debug=True)

    #Run in UI app instead of local server
    FlaskUI(app=app, server="flask", width=550, height=750, browser_path=BROWSER_PATH).run() 

