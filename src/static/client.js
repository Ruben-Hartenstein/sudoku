$(document).ready(function () {
    const socket = io.connect('http://127.0.0.1:5000/');
    var showCandidates = false;

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

    socket.on('showCandidates', function (candidates) {
        var x = 0;
        var y = 0;
        $('.cell').each(function (i, obj) {
            y = i % 9;
            x = Math.floor(i / 9);
            let candidate = candidateFormatter(candidates[x][y]);
            let child = $($(this).children()[0]);
            if (!Number(child.text())) {
                child.replaceWith("<div> <table class='candidates'> <tr> <td>" + candidate[0] + "</td> <td>" + candidate[1] + "</td> <td>" + candidate[2] + "</td> </tr> <tr> <td>" + candidate[3] + "</td> <td>" + candidate[4] + "</td> <td>" + candidate[5] + "</td> </tr> <tr> <td>" + candidate[6] + "</td> <td>" + candidate[7] + "</td> <td>" + candidate[8] + "</td> </tr> </table> </div>\n");
            }
        });
    });

    socket.on('help0', function (result) {
        alert("Technique: " + result.name);
        colorCells(result.primaryCells, 'rgb(255,216,115)');
        colorCells(result.secondaryCells, 'rgb(181,216,244)');
    });

    socket.on('update cells', function (data) {
        updateCells(data['values'], data['checkedCells']);
    });

    socket.on('showErrors', function (errors) {
        colorNumbers(errors, 'red');
    });

    // Send number with every checked Cell everytime a number is clicked
    $('.number').on('click', function () {
        resetCellColor()
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
    $('.cell').on('click', function () {
        $(this).prop('checked', !$(this).prop('checked'));
    });

    $('#erase').on('click', function () {
        let checkedCells = getCheckedCells();
        socket.emit('erase', checkedCells);
    });

    $('#candidate').on('click', function () {
        showCandidates = !showCandidates;
        if (showCandidates) {
            $('#candidate').css('color', 'red');
            updateCandidates();
        } else {
            $('#candidate').css('color', 'black');
            $('.cell').each(function (i, obj) {
                $($(this).children('div')[0]).replaceWith("<p></p>");
            });
        }
    });

    $('#clear').on('click', function () {
        socket.emit('clear', "test");
    });

    $('#start').on('click', function () {
        socket.emit('start');
    });

    $('#help').on('click', function () {
        socket.emit('help');
    });

    function updateCandidates() {
        socket.emit('getCandidates');
    }

    // Updates content of cells
    function updateCells(cellValues, cells) {
        colorNumbers(cells, 'black');
        cells.forEach((id, i) => {
            let text = cellValues[i] === 0 ? "" : cellValues[i];
            let obj = $('#' + id);
            $(obj.children()[0]).replaceWith("<p></p>");
            $(obj.children('p')[0]).text(text);
        });
        if (showCandidates)
            updateCandidates();
    }

    function updateBoard(board) {
        let cell = ""
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                cell = i.toString() + j.toString();
                updateCells([board[i][j]], [cell]);
            }
        }
    }
});

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

    function candidateFormatter(candidates) {
        let formattedCandidates = [];
        for (let index in candidates) {
            if (candidates[index] == 0)
                formattedCandidates.push(" ");
             else
                formattedCandidates.push(Number(index) + 1);
        }
        return formattedCandidates;
    }
