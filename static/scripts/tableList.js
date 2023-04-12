$(document).ready(function(){

    var accountType = '';
    if(localStorage.getItem('isAdmin')) {
        var urlParams = new URLSearchParams(window.location.search);
        accountType = urlParams.get('accountType');
        // $('#viewOtherTables').css('display', 'block');
    }
    

    localStorage.setItem('accountType', accountType)
    var data = {
        "emailId": localStorage.getItem('emailId'),
        "isAdmin": localStorage.getItem('isAdmin'),
        "accountType": accountType
    }

    $("#table-list-search").on("keyup", function() {
        var value = this.value.toLowerCase().trim();
        $(".tableName").show().filter(function() {
          return $(this).text().toLowerCase().trim().indexOf(value) == -1;
        }).hide();
      });

    $.ajax({
        type: 'POST',
        url: '/tableListInfo',
        cache:false,
        dataType : "json",
        data: JSON.stringify(data),
        contentType : "application/json",
        traditional: true,
        success: function(response) {
            $.each( response.tableNames, function( key, value ) {
                $('.list-heading1').html(response.accountType);
                $('#table_list').append('<li class="tableName">'+ value + '</li>');
            });
        }
    });

     $(document).on( 'click', '.tableName', function () {
         var tableName = $(this).text();
         localStorage.setItem("tableName", "");
         localStorage.setItem("tableName", tableName);
         window.location.href = '/viewTable?table=' + tableName 
    });
});