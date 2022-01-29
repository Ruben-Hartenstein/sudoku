$(document).ready(function () {
    $('.cell').on('click', function() { 
        $(this).parents('td').css('background-color', $(this).is(':checked') ? 'red' : 'white');
    });
});

// Simulate button click on keypress (0 = 48,1 = 49,...)
$(document).on('keypress', function(key) {
    let digit = key.which - 48;
    if (0 <= digit && digit <= 9){
        $(`#${digit}`).click();
    }
});

function colorNumbers(coords) {
    coords.forEach(coord => {
        let id = coord[0].toString() + coord[1].toString()
        $(`#${id}`).next().css('color', 'blue');
    });
}

