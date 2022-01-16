$(document).ready(function () {
    $('.cell').on('click', function() { 
        $(this).parents('td').css("background-color", $(this).is(":checked") ? "red" : "white");
    });    
});