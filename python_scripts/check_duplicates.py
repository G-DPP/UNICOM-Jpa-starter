import requests


def main(url="http://localhost:8080/fhir/MedicinalProductDefinition", names=None):
    a = requests.get(url).json()
    names = names or []
    for entry in a['entry']:
        names.append(entry['resource']['name'][0]['productName'])

    try:
        next_page = next(x for x in a['link'] if x['relation'] == 'next')
        if next_page:
            main(next_page['url'], names)
    except StopIteration:
        for name in set(names):
            names.remove(name)
        print(f"Duplicate {names=}")


if __name__ == '__main__':
    main()
