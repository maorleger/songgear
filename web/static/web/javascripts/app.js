 $(document).ready( function () {
    $('.data-table').DataTable({
        "columns": [
            { "orderable": false },
            null,
            null,
            null,
            null
          ],
        "order" : [[1, "asc"], [3, "asc"]]
    });
} );