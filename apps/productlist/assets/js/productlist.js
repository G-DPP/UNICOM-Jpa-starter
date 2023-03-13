var baseurl=window.location.origin
var url=baseurl+'/fhir/ManufacturedItemDefinition?_format=json';
url=baseurl+'/fhir/MedicinalProductDefinition?_format=json&_count=20000';
fetch(url)
    .then((response) => {
        return response.json()
    })
    .then((posts) => {
        for (prod in posts.entry) {
            var t = $('#prod-table').DataTable();
            t.pageLength=2;
            t.iDisplayLength= 50;
            current_row = []

            try { current_row.push(posts.entry[prod].resource.id)
            } catch (error){ current_row.push(error) }

            try { current_row.push('<b>'+posts.entry[prod].resource.name[0].productName+'</b>')
            } catch (error){ current_row.push(error) }

            try { current_row.push(posts.entry[prod].resource.name[0].usage[0].country.coding[0].display)
            } catch (error){ current_row.push(error) }

            try { current_row.push( '<a target="_blank" href="https://idmp-viewer.azurewebsites.net/display-product?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">Viewer</a> <br> <a target="_blank" href="'+baseurl+'/apps/visualiser/index.html?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">New Viewer</a>' )
            } catch (error){ current_row.push(error) }

            try { current_row.push( '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=xml">XML</a> <br> <a href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=json">JSON</a>' )
            } catch (error){ current_row.push(error) }

            try { current_row.push( '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'/$validate">FHIR Validation</a>' )
            } catch (error){ current_row.push(error) }

            t.row.add( current_row ).draw();

//                t.row.add([
//                    posts.entry[prod].resource.id,
//                    '<b>'+posts.entry[prod].resource.name[0].productName,
//                    posts.entry[prod].resource.name[0].usage[0].country.coding[0].display,
//                    '<a target="_blank" href="https://idmp-viewer.azurewebsites.net/display-product?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">Viewer</a> <a target="_blank" href="https://jpa.unicom.datawizard.it/apps/visualiser/index.html?url='+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'">New Viewer</a>',
//                    '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=xml">XML</a> <a href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'?_format=json">JSON</a>',
//                    '<a target="_blank" href="'+baseurl+'/fhir/MedicinalProductDefinition/'+posts.entry[prod].resource.id+'/$validate">FHIR Validation</a>',
//                ]).draw();
        }
    })