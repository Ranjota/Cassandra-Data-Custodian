function onOptionSelected(event) {
    $(event).css('color', 'black');
}

$(document).ready(function(){
    $("#table-list-search").on("keyup", function() {
        var value = this.value.toLowerCase().trim();
        $(".tableName").show().filter(function() {
          return $(this).text().toLowerCase().trim().indexOf(value) == -1;
        }).hide();
      });

        $('#tableListWrapper').css('display', 'none');
        $('#formAdminTables').css('display', 'block');    

        $('#load-data').click(function(){
            window.location.href = '/tableList?accountType=' + $('#inputTableAccountType').val()
        });
});