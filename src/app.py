from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from copy import deepcopy
import sudoku_board as sudoku_board
from src.solutions import technique_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

has_started = False
help_step = 0
technique_result = None
sudoku = sudoku_board.SudokuBoard()


# HIDDEN TRIPLE: [[0, 0, 0, 7, 4, 0, 0, 0, 8], [4, 9, 6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 4, 0], [0, 0, 0, 0, 5, 7, 6, 0, 0], [8, 0, 0, 0, 0, 0, 0, 2, 1], [0, 0, 3, 4, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0], [1, 2, 4, 0, 7, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0]]
# NAKED TRIPLE: [[0, 7, 0, 0, 0, 0, 8, 0, 0], [0, 2, 0, 8, 0, 0, 9, 5, 0], [0, 0, 0, 0, 0, 9, 6, 0, 2], [0, 0, 0, 3, 0, 4, 2, 8, 9], [0, 0, 3, 9, 0, 0, 1, 6, 4], [4, 0, 0, 6, 1, 0, 5, 0, 0], [0, 4, 0, 2, 9, 6, 0, 1, 5], [0, 0, 0, 0, 0, 0, 0, 9, 6], [0, 0, 0, 5, 3, 0, 4, 2, 8]]
# FOURSOME: [[0, 0, 0, 7, 1, 0, 2, 5, 0], [0, 3, 1, 6, 0, 0, 0, 0, 8], [0, 5, 7, 9, 0, 0, 0, 1, 0], [0, 0, 0, 0, 4, 0, 0, 0, 0], [0, 7, 0, 0, 6, 2, 1, 0, 5], [0, 0, 6, 0, 9, 7, 8, 0, 2], [0, 0, 9, 2, 0, 1, 0, 6, 0], [0, 0, 0, 0, 7, 9, 3, 2, 1], [0, 0, 0, 0, 0, 6, 0, 8, 9]]
# EXAMPLE: [[0, 0, 0, 9, 8, 0, 6, 0, 0], [4, 6, 0, 0, 2, 0, 1, 8, 9], [0, 9, 0, 0, 1, 6, 0, 0, 2], [0, 0, 3, 7, 5, 9, 0, 0, 0], [0, 5, 0, 2, 4, 1, 9, 0, 3], [0, 0, 0, 6, 3, 8, 0, 1, 0], [7, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 7, 5, 0, 2, 4]]
# THIRD EYE: [[0, 0, 8, 6, 0, 0, 2, 1, 9], [2, 0, 6, 9, 0, 0, 5, 3, 8], [9, 5, 1, 2, 3, 8, 4, 6, 7], [4, 8, 2, 0, 9, 0, 3, 7, 6], [0, 9, 0, 4, 6, 2, 1, 8, 5], [1, 6, 5, 3, 8, 7, 9, 2, 4], [8, 0, 0, 0, 2, 9, 6, 0, 3], [5, 0, 0, 8, 0, 6, 7, 9, 2], [6, 2, 9, 7, 0, 3, 8, 0, 1]]
# THIRD EYE 2:[[2, 0, 0, 7, 4, 3, 1, 6, 5], [3, 4, 6, 1, 8, 5, 9, 2, 7], [5, 7, 1, 6, 2, 9, 8, 3, 4], [6, 3, 0, 0, 1, 0, 0, 4, 9], [7, 0, 0, 4, 3, 6, 0, 1, 8], [1, 0, 4, 0, 9, 0, 3, 0, 6], [8, 6, 7, 3, 5, 1, 4, 9, 2], [9, 1, 2, 8, 6, 4, 0, 0, 3], [4, 5, 3, 9, 7, 2, 6, 8, 1]]
# HARD EXAMPLE: [[0, 2, 3, 0, 6, 5, 0, 8, 9], [9, 0, 0, 0, 0, 4, 0, 0, 5], [5, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 3, 0, 0, 0, 1, 8], [3, 8, 0, 5, 9, 0, 0, 0, 2], [0, 0, 0, 0, 8, 6, 3, 0, 0], [2, 3, 0, 0, 0, 0, 0, 0, 6], [8, 0, 7, 0, 2, 0, 0, 0, 3], [0, 9, 6, 0, 5, 3, 8, 2, 0]]
# LBI : [[1, 2, 0, 0, 5, 6, 0, 8, 0], [0, 0, 5, 9, 0, 1, 0, 0, 6], [0, 0, 6, 0, 0, 2, 1, 0, 5], [0, 1, 2, 0, 0, 0, 4, 0, 7], [0, 3, 0, 1, 0, 0, 0, 0, 0], [7, 6, 9, 0, 2, 0, 0, 1, 3], [0, 0, 7, 0, 1, 8, 0, 9, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 3, 0, 7, 0]]
# XWING: [[1, 0, 0, 0, 0, 0, 0, 8, 0], [8, 0, 0, 1, 0, 0, 0, 2, 4], [7, 0, 0, 0, 0, 3, 1, 5, 0], [0, 0, 0, 0, 4, 1, 6, 9, 2], [0, 9, 0, 6, 7, 0, 4, 1, 3], [4, 1, 6, 2, 3, 9, 8, 7, 5], [9, 0, 1, 0, 6, 2, 5, 0, 8], [0, 0, 0, 3, 0, 0, 9, 0, 1], [0, 5, 0, 9, 1, 0, 2, 0, 7]]
# SKYSCRAPER: [[0, 0, 0, 0, 2, 0, 0, 0, 0], [3, 8, 6, 0, 0, 0, 0, 5, 2], [5, 0, 0, 0, 0, 3, 0, 0, 0], [0, 1, 0, 0, 0, 8, 0, 9, 0], [4, 0, 8, 9, 0, 0, 6, 0, 7], [2, 0, 9, 0, 0, 4, 0, 0, 0], [8, 0, 0, 7, 0, 0, 3, 6, 0], [9, 0, 0, 3, 0, 1, 0, 4, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0]]
# TURBOT: [[0, 6, 0, 0, 0, 8, 1, 4, 0], [0, 5, 0, 0, 0, 6, 9, 8, 0], [4, 8, 0, 0, 3, 0, 6, 0, 5], [0, 2, 6, 0, 8, 0, 3, 0, 4], [0, 1, 4, 6, 0, 3, 7, 0, 8], [3, 7, 8, 0, 0, 9, 5, 6, 0], [6, 4, 5, 3, 0, 2, 8, 0, 0], [1, 9, 2, 8, 7, 5, 4, 3, 6], [8, 3, 7, 0, 6, 4, 2, 5, 0]
# Turbot: [[9, 0, 6, 3, 0, 5, 8, 7, 1], [8, 0, 1, 7, 0, 6, 3, 0, 9], [0, 7, 0, 8, 9, 1, 2, 0, 6], [0, 0, 0, 0, 8, 7, 9, 1, 5], [0, 0, 8, 9, 1, 0, 0, 0, 7], [1, 9, 7, 0, 5, 0, 0, 8, 0], [6, 8, 0, 0, 7, 9, 1, 0, 0], [7, 3, 4, 1, 6, 2, 5, 9, 8], [0, 1, 9, 0, 3, 8, 7, 6, 0]]
# example hard: [[0, 0, 0, 0, 0, 0, 0, 4, 0], [3, 4, 0, 8, 0, 0, 7, 2, 0], [0, 5, 6, 4, 0, 0, 8, 9, 0], [0, 3, 0, 6, 8, 5, 4, 7, 0], [0, 0, 0, 7, 3, 4, 0, 6, 2], [7, 6, 4, 2, 1, 9, 5, 3, 8], [0, 0, 0, 3, 4, 0, 0, 8, 0], [6, 8, 3, 0, 0, 0, 2, 5, 4], [4, 0, 0, 5, 0, 8, 0, 1, 0]]
# DRAGON: [[6, 4, 0, 8, 5, 3, 0, 9, 0], [9, 0, 0, 6, 4, 1, 8, 5, 0], [1, 5, 8, 7, 2, 9, 6, 4, 3], [3, 2, 5, 1, 6, 7, 9, 8, 4], [4, 0, 1, 9, 8, 2, 3, 0, 5], [8, 9, 0, 4, 3, 5, 0, 2, 0], [2, 0, 9, 5, 1, 8, 4, 0, 0], [7, 1, 0, 2, 9, 4, 5, 0, 8], [5, 8, 4, 3, 7, 6, 2, 1, 9]]


@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('message')
def handle_message(data):
    send(data)


@socketio.on('start')
def start():
    global help_step
    global has_started
    help_step = 0
    has_started = start_game()
    print(sudoku.board)
    emit('start', {'hasStarted': has_started, 'startCoords': sudoku.start_coords})


@socketio.on('connect')
def test_connect():
    global help_step
    help_step = 0
    print('Server Connected')
    emit('serverStatus', {'board': sudoku.board, 'hasStarted': has_started, 'startCoords': sudoku.start_coords})


@socketio.on('numbers')
def new_numbers(data):
    global help_step
    help_step = 0
    cell_values = sudoku.update_numbers(int(data['number']), data['checkedCells'])
    emit('update cells', {'values': cell_values, 'checkedCells': data['checkedCells']})
    print("new Number")
    if has_started and sudoku.is_finished():
        print("victory")
        emit('victory')


@socketio.on('erase')
def erase(checked_cells):
    global help_step
    help_step = 0
    cell_values = sudoku.erase_cells(checked_cells)
    emit('update cells', {'values': cell_values, 'checkedCells': checked_cells})


@socketio.on('reset')
def reset():
    global has_started
    global help_step
    global technique_result
    global sudoku
    has_started = False
    help_step = 0
    technique_result = None
    sudoku = sudoku_board.SudokuBoard()
    emit('serverStatus', {'board': sudoku.board, 'hasStarted': has_started, 'startCoords': sudoku.start_coords})


@socketio.on('getCandidates')
def candidates():
    errors = sudoku.get_errors()
    if errors:
        print(errors)
        emit('showErrors', errors)
    else:
        sudoku.update_candidates()
        emit('showCandidates', sudoku.candidates)


@socketio.on('help')
def help():
    global help_step
    global technique_result
    errors = sudoku.get_errors()
    if errors:
        print(errors)
        emit('showErrors', errors)
        return
    if help_step == 0:
        sudoku.update_candidates()
        technique_result = technique_manager.try_techniques(sudoku.board, sudoku.candidates)
        if not technique_result:
            print("No suitable technique found!")
            return
        emit('help0',
             {'name': technique_result['name'], 'primaryCells': technique_result['primary_cells'],
              'secondaryCells': technique_result['secondary_cells']})
    elif help_step == 1:
        candidates()
        emit('help1', {'highlights': technique_result['highlights'], 'crossOuts': technique_result['cross_outs']})
    elif help_step == 2:
        emit('help2', {'name': technique_result['name'], 'explanation': technique_result['explanation']})
    elif help_step == 3:
        if technique_result['name'] in ['Naked Single', 'Hidden Single', 'Third Eye']:
            data = {'number': technique_result['highlights'][0]['value'],
                    'checkedCells': [technique_result['highlights'][0]['cell']]}
            emit('help3')
            new_numbers(data)
            help_step -= 1
        else:
            sudoku.remove_candidates(technique_result['cross_outs'])
            candidates()
            emit('help3')
    help_step += 1
    help_step %= 4


def start_game():
    if not sudoku.is_board_valid():
        return False
    sudoku.solved = deepcopy(sudoku.board)
    if not sudoku.solve(board=sudoku.solved):
        return False
    if not sudoku.is_uniquely_solvable():
        return False
    sudoku.calculate_start_coords()
    technique_manager.set_solved_board(sudoku.solved)
    return True


def list2board(num_list):
    num_list = [0 if x == '' else int(x) for x in num_list]
    return [num_list[i:i + 9] for i in range(0, len(num_list), 9)]


if __name__ == '__main__':
    socketio.run(app, debug=True)
