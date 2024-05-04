![Banner Image](/media/qubit_sudoku_banner.png)

# Qubit Sudoku

A Python Sudoku solver using the wave function collapse algorithm. Whenever the algorithm runs into a contradiction (unsolvable state), it retries from the beginning, persistently iterating until the Sudoku is solved.


## Table of Contents
- [How it Works](#how-it-works)
- [Usage](#usage)
- [Installation](#installation)
- [Performance, Optimization, & Threading](#performance-optimization--threading)
- [License](#license)

# How It Works

In simple terms, the wave function collapse algorithm iterates the 9x9 Sudoku array. For each zero/empty cell, it identifies all the potential numbers that can occupy it. This set of possibilities is quantified as the "Shannon entropy" of the cell, and its elements are referred to as "coefficients". The algorithm keeps track of the cell with the least Shannon entropy (updating if another cell with fewer possibilities is found).

After each iteration, the algorithm identifies the cell with the lowest Shannon entropy and randomly selects one of its coefficients—we'll call this a 'defining moment.' When a cell is defined, it "collapses" into a defined state. This process repeats until there is one out of two possible outcomes.

The preferable outcome of the algorithm is to achieve a fully solved Sudoku array, where collapsing a cell does not interfere with previously collapsed cells, continuing this behavior until all cells are defined and therefore solving the Sudoku. 

However, the other possible outcome is finding a cell with a Shannon entropy of zero. This indicates that no value can define said cell, entering a state of contradiction and being impossible to continue (think Solitaire, when previously formed card "piles" can lead to an unwinnable state). When this occurs, the algorithm simply starts again until the Sudoku is solved or a predetermined number of attempts is reached.

You can read more about the wave function collapse algorithm [here](https://github.com/mxgmn/WaveFunctionCollapse).

# Usage

The project comes with two python scripts.

First, `sudokuWFCSolver.py` is the source code for the algorithm. It includes all the functions used for solving the array as well as a simple terminal output to see it in action (solving the array defined in `main()`).

Output in terminal:
```
Initial Sudoku Array:
[0, 0, 0, 2, 0, 1, 0, 0, 0]
[0, 0, 2, 0, 0, 5, 0, 0, 9]
[0, 5, 0, 0, 8, 0, 0, 0, 6]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[3, 0, 0, 0, 5, 0, 0, 9, 0]
[0, 8, 0, 0, 7, 0, 0, 0, 4]
[0, 4, 0, 0, 9, 0, 0, 7, 0]
[0, 2, 0, 0, 0, 0, 0, 1, 0]
[0, 0, 8, 0, 1, 0, 0, 3, 0]
----------------------------------
Solving...
Total Attempts: 134
Total Iterations: 7329
----------------------------------
Solved Sudoku Array:
[8, 9, 7, 2, 6, 1, 5, 4, 3]
[6, 3, 2, 7, 4, 5, 1, 8, 9]
[4, 5, 1, 3, 8, 9, 7, 2, 6]
[5, 1, 4, 9, 2, 3, 8, 6, 7]
[3, 7, 6, 4, 5, 8, 2, 9, 1]
[2, 8, 9, 1, 7, 6, 3, 5, 4]
[1, 4, 3, 8, 9, 2, 6, 7, 5]
[9, 2, 5, 6, 3, 7, 4, 1, 8]
[7, 6, 8, 5, 1, 4, 9, 3, 2]
```

Second, `solverWGUI.py` is a GUI made using the [Flask](https://github.com/pallets/flask) framework, paired with the [Flaskwebgui](https://github.com/ClimenteA/flaskwebgui) library to create a desktop app.

It should be noted that the Flaskwebgui library works best with Chrome or Chromium-based browsers. It also works with Microsoft's Edge. The default Chrome executable Window's path is set as `BROWSER_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"`. You can change the path or simply comment out the line and delete the `browser_path=BROWSER_PATH` argument from the FlaskUI object and the library will try to find it automatically. 

If you simply want to run it as a Flask local server and not a desktop app, comment out `FlaskUI(app=app, server="flask", width=550, height=750, browser_path=browser_path).run() ` and uncomment `app.run()`. 

Flask GUI:

![Flask GUI](/media/flask_gui.gif)

# Installation
To install simply download the repo and install `requirements.txt`.
```
git clone https://github.com/Jael-G/QubitSudoku
python3 -m pip install -r .\requirements.txt
```
Now you can run whichever script you prefer, Flask GUI or terminal based. 

# Performance, Optimization, & Threading
Notes for extra reading and understanding, as well as future optimization and changes.
### Performance
The algorithm was tested using various websites. Since most of the results were similar, for simplicity's sake I'll mention the two most of note.

First, [sudoku.com](https://sudoku.com/), a website that provides Sudokus with various difficulties to attempt solving. In easy and medium difficulty, the algorithm solves the Sudoku almost instantly (normally less than 0.01s) and there is a very specific reason why this occurs. Given that the algorithm is based on Shannon Entropy, in these difficulties there are always cells present with only one coefficient, meaning the algorithm can only make one choice (the correct choice) to define the cell.

In the extreme difficulty, things are more interesting. The algorithm takes an approximate average of 6 seconds to solve the Sudoku, however, it sometimes does it almost instantly or takes a little longer, this is explained more below in [Optimization](#optimization).

Second, [extremesudoku.info](https://www.extremesudoku.info/), a website that creates Sudokus with the sole intention of being extremely hard to solve. In this website, the failure of optimization is noticeable. Even when using multiple threads (more in-depth explanation in [threading](#threading)), sometimes the solver seems to keep making attempts for a very long time. I can only _guess_ that implementing the correct optimization code would fix this.

### Optimization
A comment about how the algorithm can be further optimized in the future, which is in my TO-DO list. 

As explained in the [How it Works](#how-it-works) section, whenever a contradiction is reached the program starts again because the cell with the contradiction is impossible to define. This can lead to cases where the sudoku is solved almost instantly or where the sudoku takes more than usual attempts to be solved. This is due to the nature of the implementation.

The most optimal way to mitigate this is to have the algorithm keep track of the defining moments where the Shannon Entropy is larger than one (multiple coefficients). If a contradiction is reached, then the algorithm should go to the latest defining moment and attempt a different coefficient. If all choices of coefficients in the defining moment also lead to a contradiction, then the "mistake" was made on a previous defining moment and the algorithm would travel even further back.

This would optimize the implementation because it would signify the algorithm's "correction"  of its previous choices and eliminates the possibility of making the same mistakes over and over again in one solution. 


### Threading
The implementation of the algorithm was done partly for threads. For example, the repeating attempts (if the algorithm finds a contradiction and the Sudoku is not solved) rely on a `SOLVED` global variable. Due to the nature of threads, they can only "communicate" via global variables. Once one thread solves the Sudoku, it sets the flag to `True` and prevents other threads from starting another attempt. 

This implementation option was done partly to make up for the lack of optimization previously discussed. However, the implementation was not completed.

In a fully thread-friendly implementation, the result cannot be "returned" as it currently does. Instead, it must be stored as a global variable safeguarded by a mutex lock. 

The implementation of a fully thread-friendly code is on my TO-DO list. 

# License

Copyright (c) 2024 Jael Gonzalez

The content of this repository is bound by the MIT licenses:
```
MIT License

Copyright (c) 2024 Jael Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```