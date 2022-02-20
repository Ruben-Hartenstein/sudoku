$(document).ready(function () {
    const socket = io.connect('http://127.0.0.1:5000/');
    var isCandidate = false;

    // Initialize connection
    socket.on('connect', function () {
        socket.send('User has connected!');
    });

    // Confirm arrival of message
    socket.on('message', function (data) {
        console.log('Received message: ' + JSON.stringify(data));
    });

    socket.on('start', function (status) {
         if (status.hasStarted) {
             $('#start').hide();
             $('#started').show();
             colorNumbers(status.startCoords, 'blue');
         } else {
             $('#start').show();
             $('#started').hide();
             alert("Sudoku either not solvable or not uniquely solvable!")
         }
    });

    // Get current status of server after (re-)connecting
    socket.on('server status', function (status) {
        updateBoard(status.board);
        if (status.hasStarted) {
            $('#start').hide();
            $('#started').show();
            console.log(status.startCoords)
            colorNumbers(status.startCoords, 'blue');
        } else {
            $('#start').show();
            $('#started').hide();
        }
    });

    socket.on('update cells', function (data) {
        updateCells(data['values'], data['checkedCells']);
    });

    socket.on('help0', function(errors) {
        console.log("help0")
        colorNumbers(errors, 'red');
    });

    // Send number with every checked Cell everytime a number is clicked
    $('.number').on('click', function () {
        let dict = {
            'number': $(this).attr('id'),
            'isCandidate': isCandidate,
            'checkedCells': getCheckedCells(),
        }
        // If no cell is selected, take the current pointer position
        if (!dict['checkedCells'].length) {
            let id = pointer[0].toString() + pointer[1].toString();
            dict['checkedCells'].push(id);
        }
        socket.emit('numbers', dict);
    });

    $('#erase').on('click', function() {
        let checkedCells = getCheckedCells();
        socket.emit('erase', checkedCells);
    }); 
    
    $('#candidate').on('click', function() {
        isCandidate = !isCandidate;
        if (isCandidate) {
            $('#candidate').css('color', 'red');
        } else {
            $('#candidate').css('color', 'black');
        }
    });

    $('#clear').on('click', function() { 
        socket.emit('clear', "test");
    });

     $('#start').on('click', function () {
        socket.emit('start');
     });

     $('#help').on('click', function () {
        socket.emit('help');
     });
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

// Updates whole board TODO: candidates
function updateBoard(board){
   $('.cell').each(function (i, obj) {
       let coords = obj.id.split('');
       let text = board[coords[0]][coords[1]][0] == 0 ? " " :  board[coords[0]][coords[1]][0];
       $(this).next().text(text);
   });
}

// Updates content of cells
function updateCells(cellValues, cells){
    colorNumbers(cells, 'black');
    cells.forEach((id, i) => {
        let text = "";
        if(cellValues[i][0] == 0){
            let candidates = cellValues[i].slice(1)
            text = candidates.some(Boolean) ? candidates : " "
        } else {
            text = cellValues[i][0]
        }
        $('#' + id).next().text(text);
    });
}