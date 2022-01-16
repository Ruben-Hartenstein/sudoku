$(document).ready(function () {
    var socket = io.connect('http://127.0.0.1:5000/');

    // Initialize connection
    socket.on('connect', function () {
        socket.send('User has connected!');
    });

    // Confirm arrival of message
    socket.on('message', function (data) {
        console.log('Received message: ' + JSON.stringify(data));
    });

    // Get current status of server after (re-)connecting
    socket.on('server status', function (board) {
        updateBoard(board.board);
    });

    // Clears whole board TODO: Write function for it
    $('#clear').on('click', function () {
        socket.emit('clear');
    });

    // Send number with every checked Cell everytime a number is clicked
    // TODO: server should initiate change
    $('.number').on('click', function () {
        let dict = {
            'number': $(this).attr('name'),
            'checkedCells': getCheckedCells(),
        }
        updateCells(dict['number'], dict['checkedCells']);
        socket.emit('numbers', dict);
    });

    // Updates whole board TODO: candidates
    function updateBoard(board){
        console.log(board);
       $('.cell').each(function (i, obj) {
           let coords = obj.id.split('');
           $(this).next().text(board[coords[0]][coords[1]]);
       });
    }

    // Updates content of cells
    function updateCells(number, cells){
        cells.forEach(id => {
            $('#' + id).next().text(number);
        });
    }

    // Returns all checked cells and unchecks them
    function getCheckedCells() {
        let checkedCells = [];
        $('.cell').each(function (i, obj) {
            if (obj.checked) {
                checkedCells.push(obj.id);
                obj.click()
            }
        });
        return checkedCells;
    }
});
