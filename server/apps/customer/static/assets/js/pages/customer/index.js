(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define("/customer/", ["jquery", "Site"], factory);
  } else if (typeof exports !== "undefined") {
    factory(require("jquery"), require("Site"));
  } else {
    var mod = {
      exports: {}
    };
    factory(global.jQuery, global.Site);
    global.customer_index = mod.exports;
  }
})(this, function (_jquery, _Site) {
  "use strict";

  _jquery = babelHelpers.interopRequireDefault(_jquery);
  (0, _jquery.default)(document).ready(function ($$$1) {
    (0, _Site.run)();
  });

  (function () {
    (0, _jquery.default)(document).ready(function () {

      $('#customers thead tr:eq(1) th').each(function () {
        var title = $(this).text();
        if (title != '') {
          $(this).html('<input type="search" class="form-control w-full column_search" placeholder="' + title + ' üzrə axtarış." />');
        }
      });

      var defaults = Plugin.getDefaults("dataTable");

      var options = _jquery.default.extend(true, {}, defaults, {
        orderCellsTop: true,
        scrollX: true,
        initComplete: function () {
          var table = this.api();

          // Column Search Show Button
          var column_search_btn = $('<button class="btn btn-sm m-5" id="column_search_btn">Sütun axtarış</button>');
          $("#customers_filter").append(column_search_btn);
          column_search_btn.button();
          column_search_btn.on('click', function () {
            var show = $('#searchHeader').css('display') == 'none';
            var display = show ? '' : 'none';
            $('#searchHeader').css('display', display);
          });

          // Clear Search Inputs Button
          var clear_search_btn = $('<button class="btn btn-sm btn-danger m-5" id="clear_search_btn">Təmizlə</button>');
          $("#customers_filter").append(clear_search_btn);
          clear_search_btn.button();
          clear_search_btn.on('click', function () {
            $('#customers_filter input').val('');
            table.search('').draw();
            $('#searchHeader input').each(function () {
              $(this).val('');
              table.column($(this).parent().index()).search('').draw();
            });
          });

          (0, _jquery.default)(table.table().header()).on('keyup', ".column_search", function () {
            table.column($(this).parent().index()).search(this.value).draw();
          });
        },
        "aoColumnDefs": [{
          'bSortable': false,
          'aTargets': [-1]
        }],
        "iDisplayLength": 10,
        "sDom": '<"dt-panelmenu clearfix"Bfr>t<"dt-panelfooter clearfix"ip>',
        "buttons": [
          'copy',
          {
            extend: 'csv',
            text: 'CSV',
            charset: 'utf-8',
            extension: '.csv',
            fieldBoundary: '',
            filename: 'export',
            bom: true
          },
          'excel',
          'pdf',
          'print'
        ],
        "columns": [
          { "width": "1%" },
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          { "width": "6%" }
        ]
      });

      $('#customers').dataTable(options);

      setInterval(function () {
        $('#searchHeader th').each(function () {
          var cell_display = $('#customers thead tr:eq(0) th:eq(' + $(this).index() + ')').css('display');
          $(this).css('display', cell_display);
        });
      }, 200);
    });
  })();
});