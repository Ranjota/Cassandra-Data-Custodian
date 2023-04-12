var editor;
$(document).ready(function() {
    editor = new $.fn.dataTable.Editor( {
        ajax: function ( method, url, data, success, error ) {
            $.ajax( {
                type: 'POST',
                url:  '/updateUser?id=' + $('#DTE_Field_id').val(),
                data: JSON.stringify(data),
                dataType: "json",
                success: function (json) {
                    var table = $('#userTable').DataTable();
                    table.ajax.reload();
                    success( json );
                }
            } );
        },
        // dataFilter: function (data) {
        //     // Parse the response data as JSON
        //     var responseData = JSON.parse(data);

        //     // Set the value of the isAdmin checkbox based on the backend response
        //     $('.admin-checkbox').prop('checked', responseData.isAdmin);

        //     // Return the parsed data
        //     return data;
        // },
        "table": "#userTable",
        "idSrc":  'id',
        "fields": [ 
            {
                "label": "id",
                "name": "id"
            },
            {
                "label": "First Name:",
                "name": "first_name"
            }, {
                "label": "Last name:",
                "name": "last_name"
            }, {
                "label": "Email Id:",
                "name": "email_id"
            }, {
                "label": "Year of birth:",
                "name": "year_of_birth"
            }, {
                "label": "IsAdmin:",
                "name":  "isAdmin"
            }, {
                "label": "Active User",
                "name": "isActiveUser"
            }, {
                "label": "Academic Period:",
                "name": "academic_period"
            },{
                "label": "Georgian College:",
                "name": "georgian_campus"
            },{
                "label": "Groups:",
                "name": "groups"
            },{
                "label": "Program Code:",
                "name": "program_code"
            }
        ]
    } );

     // New record
     $('a.editor-create').on('click', function (e) {
        e.preventDefault();
        editor.create( {
            title: 'Create new record',
            buttons: 'Add'
        } );
    } );
 
    // Edit record
    $('#userTable').on('click', 'td.editor-edit', function (e) {
        e.preventDefault();
        editor.edit( $(this).closest('tr'), {
            title: 'Edit record',
            buttons: 'Update'
        } );
    } );

    $('#userTable').DataTable({
        // serverSide: true,
        processing: true,
        ajax: { 
                url: '/userTableInfo',
                type: 'GET',
                dataSrc:  function (d) {
                    return d
                } 
        },
        searching: true,
        bFilter: true,
        columns: [
            {
                data: null,
                className: "dt-center editor-edit",
                defaultContent: '<i class="fa fa-pencil"/>',
                orderable: false
            },
            {
                data: null,
                className: "dt-center editor-delete",
                defaultContent: '<i class="fa fa-toggle"/>',
                orderable: false
            },
            {data: "id", title: "Student Id"},
            {data: "first_name", title: "First Name"},
            {data: "last_name", title: "Last Name"},
            {data: "email_id", title: "Email Id"},
            {data: "year_of_birth", title: "Year of Birth"},
            {data: "isAdmin", title: "Admin"},
            {data: "isActiveUser", title: "Active user"},
            {data: "academic_period", title: "Academic Period"},
            {data: "georgian_campus", title: "Georgian College"},
            {data: "groups", title: "Groups"},
            {data: "program_code", title: "Program Code"},
        ],
        columnDefs: [
            {
                "targets":[0, 5, 6],
                "orderable":true,
            },
        ],
        scrollX: '1000px',
        dom: 'Blfrtip',  
        buttons: [  
            {  
                extend: 'copy',  
                className: 'btn btn-dark rounded-0',  
                text: '<i class="fa fa-copy" title="Copy to Clipboard"></i>',
                titleAttr: 'Copy to Clipboard'
            },  
            {  
                extend: 'excel',  
                className: 'btn btn-dark rounded-0',  
                text: '<i class="fa fa-file-excel" title="Export as Excel"></i>',
                titleAttr: 'Excel'
            },  
            {  
                extend: 'pdf',  
                className: 'btn btn-dark rounded-0',  
                text: '<i class="fa fa-file-pdf" title="Export as PDF"></i>',
                titleAttr: 'PDF'
            },  
            {  
                extend: 'csv',  
                className: 'btn btn-dark rounded-0',  
                text: '<i class="fa fa-file" title="Export as CSV"></i>' ,
                titleAttr: 'CSV'
            },  
            {  
                extend: 'print',  
                className: 'btn btn-dark rounded-0',  
                text: '<i class="fa fa-print" title="Export as Print"></i>' ,
                titleAttr: 'Print'
            }  
        ]
        });
    }
);