var pointer = [0, 0];

$(document).ready(function () {
    toggleCellHighlighting(pointer);

    $('.cell').on('click', function() { 
        $(this).parents('td').css('background-color', $(this).is(':checked') ? 'red' : 'white');
    });
});

// Simulate button click on keypress
// 0..9 = 96..105
// Left arrow = 37
// Up arrow = 38
// Right arrow = 39
// Down arrow = 40
// Shift = 16
// Space = 32
$(document).on('keydown', function(key) {
    let pressedKey = key.which;
    // Numpad to press numbers
    if (96 <= pressedKey && pressedKey <= 105){
        let digit = pressedKey - 96;
        $(`#${digit}`).click();
    }
    // Arrow Keys to move pointer
    if (37 <= pressedKey && pressedKey <= 40){
        toggleCellHighlighting(pointer);
        switch(pressedKey) {
            case 37: // Left
                if (pointer[1] > 0);
                    pointer[1] -= 1;
                break;
            case 38: // Up
                if (pointer[0] > 0);
                    pointer[0] -= 1;
                break;
            case 39: // Right
                if (pointer[1] < 8);
                    pointer[1] += 1;
                break;
            case 40: // Down
                if (pointer[0] < 8);
                    pointer[0] += 1;
                break;
        }
        toggleCellHighlighting(pointer)
    }
    // Space Bar to click cell
    if (pressedKey == 32) {
        let id = pointer[0].toString() + pointer[1].toString();
        $(`#${id}`).click();
    }
    // Shift Key to toggle Note
    if (pressedKey == 16) {
        $('#candidate').click();
    }
});

function toggleCellHighlighting(coord) {
    let id = coord[0].toString() + coord[1].toString();
    let obj = $(`#${id}`).parents('td');
    obj.css('color',obj.css('color') == 'rgb(0, 0, 255)' ? 'black' : 'blue');
}

function colorNumbers(coords) {
    coords.forEach(coord => {
        let id = coord[0].toString() + coord[1].toString();
        $(`#${id}`).next().css('color', 'blue');
    });
}

