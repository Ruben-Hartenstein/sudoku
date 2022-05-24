var pointer = [0, 0];

$(document).ready(function () {
    $('.cell').on('click', function() {
        toggleCell($(this));
        toggleCellHighlighting(pointer, false);
        pointer = $(this).attr('id').split('').map(Number);
        let color = $(this).prop('checked') ? 'lightgrey' : 'white'
        colorCells([pointer], color);
        toggleCellHighlighting(pointer, true);
    });
});

// Simulate button click on keypress
// 1..9 = 97..105
// 1..9 = 49..57
// Left arrow = 37
// Up arrow = 38
// Right arrow = 39
// Down arrow = 40
// Shift = 16
// Space = 32
// Tab = 9
// Delete = 46
// Backspace = 8
$(document).keydown(function(e) {
   let pressedKey = e.keyCode;
    // Numpad to press numbers
    if (97 <= pressedKey && pressedKey <= 105) {
        let digit = pressedKey - 96;
        $(`#${digit}`).click();
        return false;
    }
    // Number bar to press numbers
    if (49 <= pressedKey && pressedKey <= 57) {
        let digit = pressedKey - 48;
        $(`#${digit}`).click();
        return false;
    }
    // Arrow Keys to move pointer
    if (37 <= pressedKey && pressedKey <= 40) {
        toggleCellHighlighting(pointer, false);
        switch(pressedKey) {
            case 37: // Left
                pointer[1] -= 1;
                if (pointer[1] === -1)
                    pointer[1] = 8;
                break;
            case 38: // Up
                pointer[0] -= 1;
                if (pointer[0] === -1)
                    pointer[0] = 8;
                break;
            case 39: // Right
                pointer[1] += 1;
                if (pointer[1] === 9)
                    pointer[1] = 0;
                break;
            case 40: // Down
                pointer[0] += 1;
                if (pointer[0] === 9)
                    pointer[0] = 0;
                break;
        }
        toggleCellHighlighting(pointer, true);
        return false;
    }
    // Space Bar to click cell
    if (pressedKey === 32) {
        let id = pointer[0].toString() + pointer[1].toString();
        $(`#${id}`).click();
        return false;
    }
    // Shift Key to toggle Note
    if (pressedKey === 16) {
        $('#candidate').click();
        return false;
    }
    // Tab to move pointer to next cell (with linebreak)
    if(pressedKey === 9){
        pointer2nextCell();
        return false;
    }
    // Delete
    if(pressedKey === 46 || pressedKey === 8){
        $('#erase').click()
        return false;
    }
});

function pointer2nextCell(){
    toggleCellHighlighting(pointer, false);
    pointer[1] += 1;
    if (pointer[1] === 9){
        pointer[1] = 0;
        pointer[0] += 1;
        if (pointer[0] === 9)
            pointer[0] = 0
    }
    toggleCellHighlighting(pointer, true);
}

function toggleCellHighlighting(coord, isOn) {
    let id = coord[0].toString() + coord[1].toString();
    let obj = $(`#${id}`);
    //obj.css('background', isOn ? 'radial-gradient(ellipse at center, red 0%, #e70000 25%, rgba(169,0,0,0) 89%, rgba(158,0,0,0) 100%)': 'white');
    obj.css('outline', isOn ? '2px solid yellowgreen' : '1px none black');
}

function colorNumbers(coords, color) {
    coords.forEach(coord => {
        let id = coord[0].toString() + coord[1].toString();
        $($(`#${id}`).children('p')[0]).css('color', color);
    });
}

function colorCandidates(candidates, color) {
    candidates.forEach(candidate => {
        let id = candidate['cell'][0].toString() + candidate['cell'][1].toString();
        id += candidate['value']
        $(`#${id}`).css('color', color);
    });
}

function colorCells(coords, color) {
    coords.forEach(coord => {
        let id = coord[0].toString() + coord[1].toString();
        $(`#${id}`).css('background', color);
    });
}

function resetCellColor() {
    let coords = [];
    $('.cell').each(function() {
        coords.push($(this).attr('id').split('').map(Number));
    });
    colorCells(coords, 'white')
}
