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

    socket.on('update cells', function (data) {
        console.log(data)
        updateCells(data['number'], data['checkedCells']);
    });

    // Updates whole board TODO: candidates
    function updateBoard(board){
       $('.cell').each(function (i, obj) {
           let coords = obj.id.split('');
           $(this).next().text(board[coords[0]][coords[1]][0]);
       });
    }

    // Updates content of cells
    function updateCells(number, cells){
        cells.forEach(id => {
            $('#' + id).next().text(number);
        });
    }

    // Send number with every checked Cell everytime a number is clicked
    // TODO: server should initiate change
    $('.number').on('click', function () {
        let dict = {
            'number': $(this).attr('name'),
            'checkedCells': getCheckedCells(),
        }
        socket.emit('numbers', dict);
    });

    // Returns all checked cells and unchecks them
    function getCheckedCells() {
        let checkedCells = [];
        $('.cell').each(function (i, obj) {
            if (obj.checked) {
                checkedCells.push(obj.id);
                obj.click();
            }
        });
        return checkedCells;
    }

    $('#erase').on('click', function() { 
        checkedCells = getCheckedCells();
        socket.emit('erase', checkedCells)
    }); 
    
    $('#candidate').on('click', function() { 
        console.log("Candidate Toggle")
    });

    $('#clear').on('click', function() { 
        console.log("Clear");
        socket.emit('clear');
    });
});
