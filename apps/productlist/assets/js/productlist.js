$(document).ready(function() {
    var baseurl = window.location.origin;
    var url = baseurl + '/fhir/MedicinalProductDefinition?_format=json';

    function buildAjaxUrl(data, searchParam) {
        var pageSize = data.length;
        var page = data.start / pageSize;
        return `${url}&_count=${pageSize}&_getpagesoffset=${pageSize * page}${searchParam}`;
    }

    function fetchSearchResults(searchValue) {
        var searchParams = [
            `_id:contains=${searchValue}`,
            `name:contains=${searchValue}`,
            `name.usage.country.coding.display:contains=${searchValue}` //TODO
        ];

        var promises = searchParams.map(param => fetch(url + '&' + param + '&_count=10000').then(response => response.json()));

        return Promise.all(promises).then(results => {
            var combinedEntries = results.flatMap(result => result.entry || []);
            var uniqueEntries = combinedEntries.reduce((acc, entry) => {
                if (!acc.some(e => e.resource.id === entry.resource.id)) {
                    acc.push(entry);
                }
                return acc;
            }, []);
            return {
                total: uniqueEntries.length,
                entries: uniqueEntries
            };
        });
    }

    function initializeDataTable(totalRecords) {
        if ($.fn.DataTable.isDataTable('#prod-table')) {
            $('#prod-table').DataTable().clear().destroy(); // Destroy existing DataTable
        }

        $('#prod-table').DataTable({
            "processing": true,
            "serverSide": true,
            "pageLength": 100,
            "ajax": function(data, callback, settings) {
                var searchValue = data.search.value;

                $('#loading').show(); // Show loading indicator

                if (searchValue) {
                    fetchSearchResults(searchValue).then(results => {
                        var data = results.entries.map((entry) => {
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
                            recordsTotal: results.total,
                            recordsFiltered: results.total,
                            data: data
                        });

                        $('#loading').hide(); // Hide loading indicator
                    }).catch((error) => {
                        console.error('Error fetching data:', error);
                        callback({
                            draw: data.draw,
                            recordsTotal: 0,
                            recordsFiltered: 0,
                            data: []
                        });
                        $('#loading').hide(); // Hide loading indicator
                    });
                } else {
                    var ajaxUrl = buildAjaxUrl(data, '');

                    fetch(ajaxUrl)
                        .then((response) => response.json())
                        .then((posts) => {
                            var recordsTotal = posts.total || totalRecords;
                            var recordsFiltered = recordsTotal;

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

                            $('#loading').hide(); // Hide loading indicator
                        })
                        .catch((error) => {
                            console.error('Error fetching data:', error);
                            callback({
                                draw: data.draw,
                                recordsTotal: 0,
                                recordsFiltered: 0,
                                data: []
                            });
                            $('#loading').hide(); // Hide loading indicator
                        });
                }
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

    // Replace alert with console log
    $.fn.dataTable.ext.errMode = 'none';
    $('#prod-table').on('error.dt', function(e, settings, techNote, message) {
        console.log('DataTables error:', message);
    });

    $('#loading').show(); // Show loading indicator at the beginning

    fetch(url + '&_count=20000').then((response) => response.json()).then((data) => {
        var totalRecords = data.total || 6000;
        initializeDataTable(totalRecords); // Initialize the DataTable when the page loads
        $('#loading').hide(); // Hide loading indicator
    }).catch((error) => {
        console.error('Error fetching total records:', error);
        initializeDataTable(6000); // Default value in case of error
        $('#loading').hide(); // Hide loading indicator
    });
});
