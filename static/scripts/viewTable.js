$(document).ready(function() {

    var data = {
        "tableName": localStorage.getItem("tableName"),
        "emailId": localStorage.getItem('emailId'),
        "isAdmin": localStorage.getItem('isAdmin'),
        "accountType": localStorage.getItem('accountType')
    }

    if(data.isAdmin == "false") {
        $('.content-container').removeClass( "admin" ).addClass( "not-admin" );
    }
    var columns = [];
 
    $.ajax({ 
            url: '/viewTableInfo',
            type: 'GET',
            data: data,
            dataType: 'json',
            contentType: 'application/json',
            success: function(data){
                var keys = Object.keys(data[0]);
                for (var key in keys ) {
                    columns.push({ data: keys[key].toString(), title: keys[key].toString() });
                };
                $('#viewTable').DataTable({
                    // dom: 'Bfrtip',
                    processing: true,
                    bDestroy: true,
                    columns: columns,
                    searching: true,
                    bFilter: true,
                    data: data,
                    scrollY: '500px',
                    scrollX: '1000px',
                    scrollCollapse: true,
                    autoWidth: false,
                    dom: 'Blfrtip', 
                    responsive: true,
                    lengthMenu: [
                        [10, 25, 50, 100, 250 , 1000, -1], [ 10 ,25, 50, 100, 250, 1000, "All"],
                    ], 
                    buttons: [  
                        {  
                            extend: 'copy',  
                            className: 'btn btn-dark rounded-0',  
                            text: '<i class="fa fa-copy" title="Copy to Clipboard"></i>',
                            titleAttr: 'Copy to Clipboard',
                            title: data.tableName,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    search: 'applied',
                                    order: 'applied',
                                    page: 'current'
                                }
                            }
                        },  
                        {  
                            extend: 'csv',  
                            className: 'btn btn-dark rounded-0',  
                            text: '<i class="fa fa-file" title="Export as CSV"></i>' ,
                            titleAttr: 'CSV',
                            title: data.tableName,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    search: 'applied',
                                    order: 'applied',
                                    page: 'current'
                                }
                            }
                        },  
                        {  
                            extend: 'print',  
                            className: 'btn btn-dark rounded-0',  
                            text: '<i class="fa fa-print" title="Export as Print"></i>' ,
                            titleAttr: 'Print',
                            title: data.tableName,
                            exportOptions: {
                                columns: ':visible',
                                modifier: {
                                    search: 'applied',
                                    order: 'applied',
                                    page: 'current'
                                }
                            }
                        },
                        {  
                            extend: 'colvis',  
                            className: 'button-colvis',
                            // text: '<button type="button" title="Column Visibility">Column Visibility</button>' ,
                            titleAttr: 'Column Visibility'
                        },
                    ]
                    });
        }
    });
  });
  
