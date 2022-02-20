from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from copy import deepcopy
import sudoku_board

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

has_started = False
help_nr = 0
sudoku_board = sudoku_board.SudokuBoard([[[6, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [9, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [5, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [6, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[9, 0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [5, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [7, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [4, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [9, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [3, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [4, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [8, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [9, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [2, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[4, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [5, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                         [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [3, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]])


@app.route("/")
def home():
    return render_template("index.html")


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
    print("Server Connected")
    emit('server status',
         {'board': sudoku_board.board, 'hasStarted': has_started, 'startCoords': sudoku_board.start_coords})


@socketio.on('numbers')
def new_numbers(data):
    print(f"Emit: {data}")
    if data["isCandidate"]:
        cell_values = sudoku_board.update_candidates(data["number"], data["checkedCells"])
    else:
        cell_values = sudoku_board.update_numbers(data["number"], data["checkedCells"])
    print(cell_values)
    emit('update cells', {'values': cell_values, 'checkedCells': data["checkedCells"]})


@socketio.on('erase')
def erase(checked_cells):
    cell_values = sudoku_board.erase_cells(checked_cells)
    print(cell_values)
    emit('update cells', {'values': cell_values, 'checkedCells': checked_cells})


@socketio.on('clear')
def clear(string):
    print(string)


@socketio.on('help')
def help():
    global help_nr
    errors = sudoku_board.get_errors()
    print(errors)
    emit(f'help{help_nr}', errors)
    #help_nr += 1
    #sudoku_board.calculate_candidates()


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


if __name__ == "__main__":
    socketio.run(app, debug=True)