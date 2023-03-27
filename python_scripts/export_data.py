import requests
import pandas as pd


def flatten_json(nested_json, parent_key='', sep='_'):
    """
    Converte un dizionario annidato in una struttura "piatta",
    con chiavi univoche basate sulle chiavi annidate.
    """
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                for index, item in enumerate(value):
                    items.extend(flatten_json(item, f"{new_key}{sep}{index}", sep=sep).items())
            else:
                items.append((new_key, value))
        else:
            items.append((new_key, value))
    return dict(items)


def main():
    base_url = "https://jpa.unicom.datawizard.it/fhir/MedicinalProductDefinition"
    # base_url = "http://localhost:3080/fhir/MedicinalProductDefinition"
    response = requests.get(base_url)

    data = response.json()

    entries = data.get('entry', [])
    entry_data = []
    for entry in entries:
        resource = entry.get('resource', {})
        flat_resource = flatten_json(resource)
        entry_data.append(flat_resource)

    next_url = None
    links = data.get('link', [])
    for link in links:
        if link.get('relation') == 'next':
            next_url = link.get('url')
            break

    while next_url:
        response = requests.get(next_url)
        data = response.json()
        entries = data.get('entry', [])
        for entry in entries:
            resource = entry.get('resource', {})
            flat_resource = flatten_json(resource)
            entry_data.append(flat_resource)
        links = data.get('link', [])
        next_url = None
        for link in links:
            if link.get('relation') == 'next':
                next_url = link.get('url')
                break

    df = pd.DataFrame.from_records(entry_data)

    df.to_excel("export.xlsx", index=False)


if __name__ == '__main__':
    main()
