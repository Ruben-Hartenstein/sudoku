from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from copy import deepcopy
import sudoku_board
from src.solutions import technique_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

has_started = False
help_step = 0
technique_result = None

sudoku_board = sudoku_board.SudokuBoard([[6, 0, 1, 0, 9, 4, 0, 0, 0],
                                         [0, 7, 5, 0, 1, 0, 6, 0, 0],
                                         [9, 4, 8, 0, 2, 7, 5, 0, 0],
                                         [8, 2, 0, 0, 7, 5, 4, 0, 0],
                                         [0, 0, 9, 0, 0, 0, 0, 5, 3],
                                         [0, 0, 4, 0, 0, 0, 2, 0, 8],
                                         [0, 0, 0, 0, 0, 1, 9, 6, 2],
                                         [4, 0, 2, 0, 3, 0, 1, 0, 5],
                                         [0, 0, 0, 9, 8, 2, 3, 0, 0]])


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
    emit('start', {'hasStarted': has_started, 'startCoords': sudoku_board.start_coords})


@socketio.on('connect')
def test_connect():
    global help_step
    help_step = 0
    print('Server Connected')
    emit('server status',
         {'board': sudoku_board.board, 'hasStarted': has_started, 'startCoords': sudoku_board.start_coords})


@socketio.on('numbers')
def new_numbers(data):
    global help_step
    help_step = 0
    print(f'Emit: {data}')
    cell_values = sudoku_board.update_numbers(int(data['number']), data['checkedCells'])
    print(cell_values)
    emit('update cells', {'values': cell_values, 'checkedCells': data['checkedCells']})


@socketio.on('erase')
def erase(checked_cells):
    global help_step
    help_step = 0
    cell_values = sudoku_board.erase_cells(checked_cells)
    print(cell_values)
    emit('update cells', {'values': cell_values, 'checkedCells': checked_cells})


@socketio.on('clear')
def clear(string):
    global help_step
    help_step = 0
    print(string)


@socketio.on('getCandidates')
def candidates():
    errors = sudoku_board.get_errors()
    if errors:
        print(errors)
        emit('showErrors', errors)
    else:
        sudoku_board.update_candidates()
        emit('showCandidates', sudoku_board.candidates)


@socketio.on('help')
def help():
    global help_step
    global technique_result
    print(help_step)
    errors = sudoku_board.get_errors()
    if errors:
        print(errors)
        emit('showErrors', errors)
        return
    if help_step == 0:
        sudoku_board.update_candidates()
        technique_result = technique_manager.try_techniques(sudoku_board.board, sudoku_board.candidates)
        if not technique_result:
            print("No suitable technique found!")
            return
        print("HELP0")
        print(technique_result['name'])
        print(technique_result['primary_cells'])
        print(technique_result['secondary_cells'])
        emit(f'help0',
             {'name': technique_result['name'], 'primaryCells': technique_result['primary_cells'],
              'secondaryCells': technique_result['secondary_cells']})
    elif help_step == 1:
        print("HELP1")
        print(technique_result['cross_outs'])
        print(technique_result['highlights'])
        emit(f'help1', {'highlights': technique_result['highlights'], 'crossOuts': technique_result['cross_outs'], 'candidates': sudoku_board.candidates})
    elif help_step == 2:
        print("HELP2")
        print(technique_result['name'])
        print(technique_result['explanation'])
        emit(f'help2', {'name': technique_result['name'], 'explanation': technique_result['explanation']})
    help_step += 1
    help_step %= 3
    print(help_step)


def start_game():
    if not sudoku_board.is_board_valid():
        return False
    sudoku_board.solved = deepcopy(sudoku_board.board)
    if not sudoku_board.solve(board=sudoku_board.solved):
        return False
    if not sudoku_board.is_uniquely_solvable():
        return False
    sudoku_board.calculate_start_coords()
    technique_manager.set_solved_board(sudoku_board.solved)
    return True


def list2board(num_list):
    num_list = [0 if x == '' else int(x) for x in num_list]
    return [num_list[i:i + 9] for i in range(0, len(num_list), 9)]


if __name__ == '__main__':
    socketio.run(app, debug=True)
