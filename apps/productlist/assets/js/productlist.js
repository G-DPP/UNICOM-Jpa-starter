var baseurl=window.location.origin
var url=baseurl+'/fhir/ManufacturedItemDefinition?_format=json';
url=baseurl+'/fhir/MedicinalProductDefinition?_format=json&_count=20000';
fetch(url)
    .then((response) => {
        return response.json()
    })
    .then((posts) => {
            for (prod in posts.entry) {
                /*
                let li = document.createElement("li");
                let node = document.createTextNode(posts.entry[prod].resource.name[0].productName);
                li.classList.add('list-group-item')
                li.classList.add('list-group-item-action')
                li.appendChild(node);
                container.appendChild(li);
                */
                /*
                var tbodyRef = document.getElementById('prod-table').getElementsByTagName('tbody')[0];
                var newRow = tbodyRef.insertRow();
                var newCell = newRow.insertCell();
                newCell.innerHTML=posts.entry[prod].resource.id;
                var newCell = newRow.insertCell();
                newCell.innerHTML=posts.entry[prod].resource.name[0].productName;
                */
                var t = $('#prod-table').DataTable();
                t.pageLength=2;
                t.iDisplayLength= 50;
                t.row.add( [
                    posts.entry[prod].resource.id,
                    '<b>'+posts.entry[prod].resource.name[0].productName,
                    posts.entry[prod].resource.name[0].countryLanguage[0].country.coding[0].display,
                    '<a target="_blank" href="https://idmp-viewer.azurewebsites.net/display-product?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">Viewer</a> <a target="_blank" href="https://jpa.unicom.datawizard.it/apps/visualiser/index.html?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">New Viewer</a>',
                    '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=xml">XML</a> &nbsp;&nbsp;&nbsp; <a href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=json">JSON</a>',
                    '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'/$validate">FHIR Validation</a>'
                ] ).draw();
            }
        }
    )