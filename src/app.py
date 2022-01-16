from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import sudoku_board

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

sudoku_board = sudoku_board.SudokuBoard()

@app.route("/")
def home():
    return render_template("index.html")


@socketio.on('message')
def handle_message(data):
    #print('received message: ' + data)
    send(data)


@socketio.on('connect')
def test_connect():
    print("Server Connected")
    emit('server status', {'board': sudoku_board.board})


@socketio.on('numbers')
def new_numbers(data):
    sudoku_board.updateCell(data["number"], data["checkedCells"])
    print(f"Emit: {data}")


def list2board(num_list):
    num_list = [0 if x == '' else int(x) for x in num_list]
    return [num_list[i:i + 9] for i in range(0, len(num_list), 9)]


if __name__ == "__main__":
    socketio.run(app, debug=True)
