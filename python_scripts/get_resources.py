import json
import os.path
import shutil

import requests
# from python_scripts.utilities import next_bundle_page


class Settings:
    server_url = 'http://fhir.hl7.pt/fhir'
    result_directory = "./exported_resources"
    resources_to_export = [
        'Medication',
        'Patient',
        'SearchParameter',
        'MedicationStatement',
        'Condition',
        'Observation',
        'Practitioner',
        'Composition',
        'AllergyIntolerance',
        'MedicationRequest',
        'Encounter',
        'StructureDefinition',
        'Bundle'
    ]
#
#
# def get_resource(url):
#     json_response = requests.get(url).json()
#
# def main():
#     if os.path.isdir(Settings.result_directory):
#         shutil.rmtree(Settings.result_directory)
#     os.mkdir(Settings.result_directory)
#
#     for resource_name in Settings.resources_to_export:
#         url = os.path.join(Settings.server_url, resource_name)
#
#         json_response = requests.get(url).json()
#
#         request_result_filepath = f"Bundle-{resource_name}-{json_response['id']}"
#         with open(request_result_filepath, "w") as outfile:
#             json.dump(json_response.json(), outfile, indent=2)
#
#        while next_bundle_page(json_response):
#


def get_search_bundles(server_url="https://jpa.unicom.datawizard.it/fhir", resource_name="MedicinalProductDefinition", count=None, _is_next=False):
    url = os.path.join(server_url, resource_name) if (resource_name and not _is_next) else server_url
    if count:
        url = os.path.join(url, f"?_count={count}")
    result_bundle = requests.get(url).json()

    request_result_filepath = os.path.join(Settings.result_directory, resource_name, f"{result_bundle['id']}.json")
    with open(request_result_filepath, "w") as outfile:
        json.dump(result_bundle, outfile, indent=2)

    next_page = next(x for x in result_bundle['link'] if x['relation'] == 'next')
    get_search_bundles(next_page['url'], resource_name=resource_name, _is_next=True)


def main():
    for resource_name in Settings.resources_to_export:
        resources_folder = os.path.join(Settings.result_directory, resource_name)
        os.mkdir(resources_folder)
        try:
            get_search_bundles(
                server_url=Settings.server_url,
                resource_name=resource_name,
                count=20000,
            )
        except StopIteration:
            continue


if __name__ == '__main__':
    if os.path.isdir(Settings.result_directory):
        shutil.rmtree(Settings.result_directory)
    os.mkdir(Settings.result_directory)
    main()
