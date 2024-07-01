$(document).ready(function() {
    var baseurl = window.location.origin;
    var url = baseurl + '/fhir/MedicinalProductDefinition?_format=json';

    function buildAjaxUrl(data) {
        var pageSize = data.length;
        var page = data.start / pageSize;
        var searchParam = data.search.value ? `&name:contains=${data.search.value}` : ''; // Aggiunge il parametro di ricerca se presente
        return `${url}&_count=${pageSize}&_getpagesoffset=${pageSize * page}${searchParam}`;
    }

    function fetchTotalRecords() {
        return fetch(url + '&_count=20000')
            .then((response) => response.json())
            .then((data) => {
                return data.total || 6000;
            })
            .catch((error) => {
                console.error('Error fetching total records:', error);
                return 6000;
            });
    }

    function initializeDataTable(recordsTotal) {
        if ($.fn.DataTable.isDataTable('#prod-table')) {
            $('#prod-table').DataTable().clear().destroy(); // Distrugge la DataTable esistente
        }

        $('#prod-table').DataTable({
            "processing": true,
            "serverSide": true,
            "pageLength": 100,
            "ajax": function(data, callback, settings) {
                var ajaxUrl = buildAjaxUrl(data);

                fetch(ajaxUrl)
                    .then((response) => response.json())
                    .then((posts) => {
                        var recordsFiltered = posts.total || recordsTotal;

                        var data = posts.entry.map((entry) => {
                            var current_row = [];

                            current_row.push(entry.resource.id || 'N/A');
                            current_row.push(entry.resource.name?.[0]?.productName ? `<b>${entry.resource.name[0].productName}</b>` : 'N/A');
                            current_row.push(entry.resource.name?.[0]?.usage?.[0]?.country?.coding?.[0]?.display || 'N/A');

                            var viewerLink = `<a target="_blank" href="https://idmp-viewer.azurewebsites.net/display-product?url=${baseurl}/fhir/MedicinalProductDefinition/${entry.resource.id}">Viewer</a>
                                              <br>
                                              <a target="_blank" href="${baseurl}/apps/visualiser/index.html?url=${baseurl}/fhir/MedicinalProductDefinition/${entry.resource.id}">New Viewer</a>`;
                            current_row.push(viewerLink);

                            var formatLinks = `<a target="_blank" href="${baseurl}/fhir/MedicinalProductDefinition/${entry.resource.id}?_format=xml">XML</a>
                                               <br>
                                               <a href="${baseurl}/fhir/MedicinalProductDefinition/${entry.resource.id}?_format=json">JSON</a>`;
                            current_row.push(formatLinks);

                            var validationLink = `<a target="_blank" href="${baseurl}/fhir/MedicinalProductDefinition/${entry.resource.id}/$validate">FHIR Validation</a>`;
                            current_row.push(validationLink);

                            return current_row;
                        });

                        callback({
                            draw: data.draw,
                            recordsTotal: recordsTotal,
                            recordsFiltered: recordsFiltered,
                            data: data
                        });
                    })
                    .catch((error) => {
                        console.error('Error fetching data:', error);
                        callback({
                            draw: data.draw,
                            recordsTotal: 0,
                            recordsFiltered: 0,
                            data: []
                        });
                    });
            },
            "columns": [
                { "title": "ID" },
                { "title": "Name" },
                { "title": "Country" },
                { "title": "Viewer Links" },
                { "title": "Formats" },
                { "title": "Validation" }
            ]
        });
    }

    $.fn.dataTable.ext.errMode = 'none';
    $('#prod-table').on('error.dt', function(e, settings, techNote, message) {
        console.log('DataTables error:', message);
    });

    // Recupera il totale dei record e inizializza la DataTable
    fetchTotalRecords().then(totalRecords => {
        initializeDataTable(totalRecords); // Inizializza la DataTable con il totale dei record
    });
});
