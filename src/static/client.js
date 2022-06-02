$(document).ready(function () {
    const socket = io.connect('http://127.0.0.1:5000/');
    var candidatesVisible = false;
    var startCoords = [];

    // Initialize connection
    socket.on('connect', function () {
        socket.send('User has connected!');
    });

    // Confirm arrival of message
    socket.on('message', function (data) {
        console.log('Received message: ' + JSON.stringify(data));
    });

    socket.on('start', function (status) {
        if (status['hasStarted']) {
            $('#start').hide();
            $('.started').show();
            startCoords = status['startCoords'];
            colorNumbers(startCoords, 'mediumblue');
        } else {
            $('#start').show();
            $('.started').hide();
            alert("Sudoku either not solvable or not uniquely solvable!");
        }
    });

    // Get current status of server after (re-)connecting
    socket.on('serverStatus', function (status) {
        updateBoard(status['board']);
        if (status['hasStarted']) {
            $('#start').hide();
            $('.started').show();
            startCoords = status['startCoords'];
            colorNumbers(startCoords, 'mediumblue');
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
            let id = $(this).attr('id');
            if ((child.prop('tagName') === 'P' && !Number(child.text())) || child.prop('tagName') === 'TABLE') {
                let html = "<table class='candidates'>";
                for (let i = 0; i < 3; i++) {
                    html += "<tr>";
                    for (let j = 0; j < 3; j++) {
                        let index = i * 3 + j;
                        html += "<td id=" + id + (index + 1) + ">" + (candidate[index]) + "</td>";
                    }
                    html += "</tr>";
                }
                html += "</table>";
                child.replaceWith(html);
            }
        });
    });

    socket.on('help0', function (technique_result) {
        $("#technique-name").text(technique_result['name']);
        $("#technique-explanation").text("");
        colorCells(technique_result['primaryCells'], 'rgb(255,216,115)');
        colorCells(technique_result['secondaryCells'], 'rgb(181,216,244)');
    });

    socket.on('help1', function (technique_result) {
        if (!candidatesVisible) {
            candidatesVisible = !candidatesVisible;
            $('#candidate').css('color', 'red');
        }
        colorCandidates(technique_result['crossOuts'], 'red');
        colorCandidates(technique_result['highlights'], 'limegreen');
    });

    socket.on('help2', function (technique_result) {
         $("#technique-explanation").text(technique_result['explanation']);
    });

    socket.on('help3', function () {
        if (!candidatesVisible) {
            candidatesVisible = !candidatesVisible;
            $('#candidate').css('color', 'red');
        }
        $("#technique-name").text("");
        $("#technique-explanation").text("");
        resetCellColor();
    });

    socket.on('victory', function () {
        console.log("VICTORY")
        $("#technique-name").text("Victory");
    });

    socket.on('update cells', function (data) {
        updateCells(data['values'], data['checkedCells']);
    });

    socket.on('showErrors', function (errors) {
        colorNumbers(errors, 'red');
    });

    // Send number with every checked Cell everytime a number is clicked
    $('.number').on('click', function () {
        resetCellColor();
        let dict = {
            'number': $(this).attr('id'),
            'checkedCells': getCheckedCells(),
        }
        socket.emit('numbers', dict);
        pointer2nextCell();
    });

    $('#candidate').on('click', function () {
        if(!startCoords.length)
            return;
        candidatesVisible = !candidatesVisible;
        if (candidatesVisible) {
            $('#candidate').css('color', 'red');
            updateCandidates();
        } else {
            hideCandidates();
        }
    });

    function hideCandidates(){
        $('#candidate').css('color', 'black');
        $('.cell').each(function (i, obj) {
            $($(this).children('table')[0]).replaceWith("<p></p>");
        });
    }

    $('#erase').on('click', function () {
        resetCellColor();
        socket.emit('erase', getCheckedCells());
    });

    $('#reset').on('click', function () {
        candidatesVisible = false;
        startCoords = [];
        $("#technique-name").text("");
        $("#technique-explanation").text("");
        resetCellColor();
        hideCandidates();
        socket.emit('reset');
    });

    $('#start').on('click', function () {
        resetCellColor();
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
        let tempJSON = JSON.stringify(startCoords);
        cellValues = cellValues.filter(x =>tempJSON.indexOf(cells[cellValues.indexOf(x)]) === -1);
        cells = cells.filter(x =>tempJSON.indexOf(x) === -1);
        colorNumbers(cells, 'black');
        cells.forEach((id, i) => {
            let text = cellValues[i] === 0 ? "" : cellValues[i];
            let obj = $('#' + id.join(''));
            $(obj.children('table')[0]).replaceWith("<p></p>");
            $(obj.children('p')[0]).text(text);
        });
        if (candidatesVisible)
            updateCandidates();
    }

    function updateBoard(board) {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                updateCells([board[i][j]], [[i, j]]);
            }
        }
    }
});

// Returns all checked cells and unchecks them
function getCheckedCells() {
    let checkedCells = [];
    $('.cell').each(function (i, obj) {
        if ($(this).prop('checked')) {
            checkedCells.push(obj.id.split('').map(Number));
            toggleCell($(this));
        }
    });
    // If no cell is selected, take the current pointer position
    if (!checkedCells.length)
        checkedCells.push(pointer);
    return checkedCells;
}

function candidateFormatter(candidates) {
    let formattedCandidates = [];
    for (let index in candidates) {
        if (candidates[index] === 0)
            formattedCandidates.push(" ");
        else
            formattedCandidates.push(Number(index) + 1);
    }
    return formattedCandidates;
}

// Update checked property
function toggleCell(cell) {
    cell.prop('checked', !cell.prop('checked'));
}
