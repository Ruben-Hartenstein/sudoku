from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from copy import deepcopy
import sudoku_board
from src.solutions import naked_single

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

has_started = False
help_nr = 0
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
    global has_started
    has_started = start_game()
    emit('start', {'hasStarted': has_started, 'startCoords': sudoku_board.start_coords})


@socketio.on('connect')
def test_connect():
    print('Server Connected')
    emit('server status',
         {'board': sudoku_board.board, 'hasStarted': has_started, 'startCoords': sudoku_board.start_coords})


@socketio.on('numbers')
def new_numbers(data):
    global help_nr
    print(f'Emit: {data}')
    cell_values = sudoku_board.update_numbers(data['number'], data['checkedCells'])
    print(cell_values)
    help_nr = 0
    emit('update cells', {'values': cell_values, 'checkedCells': data['checkedCells']})


@socketio.on('erase')
def erase(checked_cells):
    global help_nr
    cell_values = sudoku_board.erase_cells(checked_cells)
    print(cell_values)
    help_nr = 0
    emit('update cells', {'values': cell_values, 'checkedCells': checked_cells})


@socketio.on('clear')
def clear(string):
    print(string)


@socketio.on('help')
def help():
    global help_nr
    if help_nr == 0:
        errors = sudoku_board.get_errors()
        if errors:
            print(errors)
            emit('showErrors', errors)
        else:
            sudoku_board.update_candidates()
            technique = naked_single.NakedSingle(sudoku_board.board, sudoku_board.candidates)
            technique.execute_technique()
            result = technique.get_result()
            print(result['name'])
            print(result['cross_outs'])
            print(result['fields'])
            print(result['associated_fields'])
            emit(f'help0', {'name': result['name'], 'fields': result['fields'], 'associatedFields': result['associated_fields']})
            help_nr += 1
    if help_nr == 1:
        help_nr = 0
        pass


def start_game():
    if not sudoku_board.is_board_valid():
        return False
    sudoku_board.solved = deepcopy(sudoku_board.board)
    if not sudoku_board.solve(board=sudoku_board.solved):
        return False
    if not sudoku_board.is_uniquely_solvable():
        return False
    sudoku_board.calculate_start_coords()
    return True


def list2board(num_list):
    num_list = [0 if x == '' else int(x) for x in num_list]
    return [num_list[i:i + 9] for i in range(0, len(num_list), 9)]


if __name__ == '__main__':
    socketio.run(app, debug=True)
