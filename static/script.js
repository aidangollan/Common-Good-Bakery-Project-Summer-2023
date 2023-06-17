$( function() {
    $( "#start_date" ).datepicker({ dateFormat: 'mm/dd/yy' });
    $( "#end_date" ).datepicker({ dateFormat: 'mm/dd/yy' });

    // Code for handling select all functionality
    $("#select_all_categories").click(function(){
        $('input[name="category"]').not(this).prop('checked', this.checked);
    });

    $("#select_all_locations").click(function(){
        $('input[name="location"]').not(this).prop('checked', this.checked);
    });
});