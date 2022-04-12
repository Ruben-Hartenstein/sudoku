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
             $('.started').show();
             colorNumbers(status.startCoords, 'blue');
         } else {
             $('#start').show();
             $('.started').hide();
             alert("Sudoku either not solvable or not uniquely solvable!");
         }
    });

    // Get current status of server after (re-)connecting
    socket.on('server status', function (status) {
        updateBoard(status.board);
        if (status.hasStarted) {
            $('#start').hide();
            $('.started').show();
            colorNumbers(status.startCoords, 'blue');
        } else {
            $('#start').show();
            $('.started').hide();
        }
    });

     socket.on('help0', function (result) {
        alert("Technique: " + result.name);
        colorCells(result.primaryCells, 'rgb(255,216,115)');
        colorCells(result.secondaryCells,'rgb(181,216,244)')
    });

    socket.on('update cells', function (data) {
        updateCells(data['values'], data['checkedCells']);
    });

    socket.on('showErrors', function(errors) {
        colorNumbers(errors, 'red');
    });

    // Send number with every checked Cell everytime a number is clicked
    $('.number').on('click', function () {
        //resetCellColor()
        let dict = {
            'number': $(this).attr('id'),
            'checkedCells': getCheckedCells(),
        }
        // If no cell is selected, take the current pointer position
        if (!dict['checkedCells'].length) {
            let id = pointer[0].toString() + pointer[1].toString();
            dict['checkedCells'].push(id);
        }
        socket.emit('numbers', dict);
    });

    // Update checked property and cell color
    $('.cell').on('click', function() {
        $(this).prop('checked', !$(this).prop('checked'));
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

function updateBoard(board){
   let cell = ""
   for (let i = 0; i < 9; i++) {
       for (let j = 0; j < 9; j++) {
           cell = i.toString() + j.toString();
           updateCells([board[i][j]], [cell]);
       }
   }
}

// Updates content of cells
function updateCells(cellValues, cells){
    colorNumbers(cells, 'black');
    cells.forEach((id, i) => {
        let text = cellValues[i] === 0 ? " " :  cellValues[i];
        $($('#' + id).children('p')[0]).text(text);
    });
}

// Returns all checked cells and unchecks them
function getCheckedCells() {
    let checkedCells = [];
    $('.cell').each(function (i, obj) {
        if ($(this).prop('checked')) {
            checkedCells.push(obj.id);
            obj.click();
        }
    });
    return checkedCells;
}
