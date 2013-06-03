var editor; // use a global for the submit and return data rendering in the examples
 
$(document).ready(function() {
    editor = new $.fn.dataTable.Editor( {
        "ajaxUrl": {
            "create":    "POST locations",
            "edit":      "PUT locations/_id_",
            "remove": "DELETE locations/_id_"
        },
        "domTable": "#example",
        "fields": [ {
                "label": "Name:",
                "name": "name"
            }, {
                "label": "Address:",
                "name": "address"
            }
        ]
    } );
 
    $('#example').dataTable( {
        "sDom": "Tfrtip",
        "sAjaxSource": "locations",
        "aoColumns": [
            { "mData": "name" },
            { "mData": "address" },
        ],
        "oTableTools": {
            "sRowSelect": "multi",
            "aButtons": [
                { "sExtends": "editor_create", "editor": editor },
                { "sExtends": "editor_edit",   "editor": editor },
                { "sExtends": "editor_remove", "editor": editor }
            ]
        }
    } );
} );