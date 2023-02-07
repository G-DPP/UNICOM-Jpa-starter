import argparse
from datetime import datetime
import json
import os
import time
import urllib.parse as urlparse
from urllib.parse import urlencode

from utilites import get_resource, get_next_searchset

output_dir = '../downloaded_resources/'


def check_bundles():
    ids = set()
    dir = "../downloaded_resources/r4b.unicom.datawizard.it/MedicinalProductDefinition/2023_01_31_1675166181"
    for file in os.listdir(dir):
        with open(os.path.join(dir, file)) as json_file:
            data = json.load(json_file)
            for entry in data['entry']:
                ids.add(entry['resource']['id'])

    print(len(ids))
#"AdministrableProductDefinition, Ingredient, ManufacturedItemDefinition, PackagedProductDefinition, Substance, SubstanceDefinition"

def main(fhir_entrypoint=None, resource_name=None):
    #check_bundles()
    now = datetime.now()

    current_time = f'{now.strftime("%Y_%m_%d")}_{str(time.time()).split(".")[0]}'

    fhir_server_no_protocol = fhir_entrypoint.replace("https://", '').replace("http://", '')
    server_name = fhir_server_no_protocol.split("/")[0]
    next_output_dir = os.path.join(
        output_dir,
        server_name,
        resource_name,
        current_time,
    )

    if not os.path.isdir(next_output_dir):
        os.makedirs(next_output_dir)

    next_bundle = os.path.join(fhir_entrypoint, resource_name) + "/?"
    cont = 0
    while next_bundle:
        if "_bundletype=" not in next_bundle:
            next_bundle += "&_bundletype=transaction"
        else:
            next_bundle.replace("_bundletype=searchset", "_bundletype=transaction")
        next_bundle += "&_format=json"
        print(next_bundle)



        resource = get_resource(next_bundle)
        file_name = os.path.join(next_output_dir, f"{resource_name}_{cont}.json")
        with open(file_name, "w") as outfile:
            json.dump(resource, outfile, indent=2)
            cont += 1

        next_bundle = get_next_searchset(resource)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fhir_entrypoint")
    parser.add_argument("resource_name")
    args = parser.parse_args()
    main(**args.__dict__)
