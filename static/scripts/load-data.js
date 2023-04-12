function onOptionSelected(event) {
    $(event).css('color', 'black');
}

$(document).ready(function() {

//    var socket = io.connect('http://' + document.domain + ':' + location.port);

//   socket.on('update_table', function(data) {
//     // find the table row with the matching filename and remove the spinner icon
//     $(".tableName").filter(function() {
//       return $(this).text() === data.filename;
//     }).removeClass('fa fa-spinner fa-spin').css('color', 'black');
//   });

  $("input:file").change(function() {
    var filenames = '';
    for (var i = 0; i < this.files.length; i++) {       
      filenames += '<li class="tableName">' + this.files[i].name + '<span class="fa fa-spinner fa-spin ' + this.files[i].name.split('.')[0] + '" style="position: absolute;right: 19px;top: 15px; font-size: 24px;display:none;"></span></li>'; 
    }
    $(".gradient-list").append(filenames);
});

    
$('#load-data').click(function() {
var csv_files = $('#inputDataSource')[0].files;
$('.load-table-list').find('.fa-spinner').css('display', 'block');
$.each(csv_files, function(index, file) {
var form_data = new FormData();
form_data.append('csv_file', file);

$.ajax({
  url: "/uploadTable?accountType=" + $('#inputAccountType').val(),
  type: "POST",
  data: form_data,
  contentType: false,
  processData: false,
  success: function(response) {
    // alert("Data from " + file.name + " successfully inserted into database");
    // // socket.emit('upload_success', file.name);
    icon = '<span class="fa fa-check-circle ' + file.name.split('.')[0] + '_check' + '" style="color: #72e809;position: absolute;right: 19px;top: 15px; font-size: 24px;"></span>';
    $('.load-table-list').find('.'+ file.name.split('.')[0]).replaceWith(icon);
  },
  error: function(xhr) {
    console.log("Error: " + xhr.responseText);
  }
});
});
});
});
