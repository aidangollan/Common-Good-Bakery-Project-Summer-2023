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
    $("#add_item_button").click(function() {
        var newItem = $(".transfer-item").first().clone();
        $("#form_container").append(newItem);
        initializeDatepicker();
    });

    $("#submit_transfer_button").click(function() {
        var transfers = [];
        $(".transfer-item").each(function(index){
            var item = $(this).find('input[name="item"]').val();
            var location = $(this).find('select[name="location"]').val();
            var amount = $(this).find('input[name="amount"]').val();
            var date = $(this).find('input[name="date"]').val();
            transfers.push({[`item${index}`]: item, [`location${index}`]: location, [`amount${index}`]: amount, [`date${index}`]: date});
        });
        $.post('/add_transfer', transfers);
    });

    function initializeDatepicker() {
        $(".date").datepicker({ dateFormat: 'mm/dd/yy' });
    }
});