(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define("/sale/", ["jquery", "Site"], factory);
  } else if (typeof exports !== "undefined") {
    factory(require("jquery"), require("Site"));
  } else {
    var mod = {
      exports: {}
    };
    factory(global.jQuery, global.Site);
    global.sale_index = mod.exports;
  }
})(this, function (_jquery, _Site) {
  "use strict";

  _jquery = babelHelpers.interopRequireDefault(_jquery);
  (0, _jquery.default)(document).ready(function ($$$1) {
    (0, _Site.run)();
  });

  (function () {
    (0, _jquery.default)(document).ready(function () {

      $('#sales thead tr:eq(1) th').each(function () {
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

          // Date Search inputs
          var date_search = $('<label><input type="date" class="form-control" id="minDate" data-date="" data-date-format="dd/mm/yyyy" placeholder="Başlanğıc tarixi"><input type="date" class="form-control" id="maxDate" placeholder="Son tarix"></label>');
          $("#sales_filter").append(date_search);
          date_search.on('change', function () {
            table.draw();
          });

          // Column Search Show Button
          var column_search_btn = $('<button class="btn btn-sm m-5" id="column_search_btn">Sütun axtarış</button>');
          $("#sales_filter").append(column_search_btn);
          column_search_btn.button();
          column_search_btn.on('click', function () {
            var show = $('#searchHeader').css('display') == 'none';
            var display = show ? '' : 'none';
            $('#searchHeader').css('display', display);
          });

          // Clear Search Inputs Button
          var clear_search_btn = $('<button class="btn btn-sm btn-danger m-5" id="clear_search_btn">Təmizlə</button>');
          $("#sales_filter").append(clear_search_btn);
          clear_search_btn.button();
          clear_search_btn.on('click', function () {
            $('#sales_filter input').val('');
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
        drawCallback: function ( row, data, start, end, display ) {
            var api = this.api(), data;

            // Remove the formatting to get integer data for summation
            var intVal = function ( i ) {
                return typeof i === 'string' ?
                    i.replace(/[\$,]/g, '')*1 :
                    typeof i === 'number' ?
                        i : 0;
            };

            // Total over all pages
            var total = api
                .rows( {search:'applied'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b[6].replace(' ₼', ''));
                }, 0 );

            var total_paid = api
                .rows( {search:'applied'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b[7].replace(' ₼', ''));
                }, 0 );

            var total_debt = api
                .rows( {search:'applied'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b[8].replace(' ₼', ''));
                }, 0 );

            var total_income = api
                .rows( {search:'applied'} )
                .data()
                .reduce( function (a, b) {
                    return intVal(a) + intVal(b[9].replace(' ₼', ''));
                }, 0 );

            // Update status DIV
            $('#total').html('<b>Bütün Ümumi Qiymət Toplamı:</b> <u>'+ total + ' ₼</u>');
            $('#total_paid').html('<b>Bütün Ödənilən Qiymət Toplamı:</b> <u>'+ total_paid + ' ₼</u>');
            $('#total_debt').html('<b>Bütün Borc Toplamı:</b> <u>'+ total_debt + ' ₼</u>');
            $('#total_income').html('<b>Bütün Gəlir Toplamı:</b> <u>'+ total_income + ' ₼</u>');
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
          null,
          null,
          null,
          null,
          { "width": "6%" }
        ]
      });

      $('#sales').dataTable(options);

      setInterval(function () {
        $('#searchHeader th').each(function () {
          var cell_display = $('#sales thead tr:eq(0) th:eq(' + $(this).index() + ')').css('display');
          $(this).css('display', cell_display);
        });
      }, 200);
    });
  })();

  $.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var minDate = $('#minDate').val();
        var maxDate = $('#maxDate').val();
        var min = minDate ? new Date(minDate) : null;
        var max = maxDate ? new Date(maxDate) : null;
        var dateString = data[11].split(' ')[0].split('/');
        var date = new Date(dateString[2], dateString[1] - 1, dateString[0]);
 
        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date && max === null ) ||
            ( min <= date && date <= max )
        ) {
            return true;
        }
        return false;
    }
  );
});