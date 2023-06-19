$( function() {
    // Code for handling select all functionality
    $("#select_all_categories").click(function(){
        $('input[name="category"]').not(this).prop('checked', this.checked);
    });

    $("#select_all_locations").click(function(){
        $('input[name="location"]').not(this).prop('checked', this.checked);
    });

    // The datepicker
    initializeDatepicker();

    // The add transfer button click event
    $("#add_transfer_button").click(function() {
        var formGroup = '<div class="form-group row">' +
                            '<div class="col-sm-3">' +
                                '<input type="text" class="form-control" placeholder="Item">' +
                            '</div>' +
                            '<div class="col-sm-3">' +
                                '<select class="form-control">' +
                                    '<option value="14th">14th</option>' +
                                    '<option value="8th">8th</option>' +
                                '</select>' +
                            '</div>' +
                            '<div class="col-sm-3">' +
                                '<input type="text" class="form-control" placeholder="Amount">' +
                            '</div>' +
                            '<div class="col-sm-3">' +
                                '<input type="text" class="form-control date" placeholder="Date">' +
                            '</div>' +
                        '</div>';
        $("#form_container").append(formGroup);
        initializeDatepicker();
    });

    function initializeDatepicker() {
        $(".date").datepicker({ dateFormat: 'mm/dd/yy' });
    }
});