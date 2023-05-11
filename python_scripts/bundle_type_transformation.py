import json
import os.path
import pathlib
import shutil


class BundleTypes:
    transaction = 'transaction'
    searchset = 'searchset'
    batch = 'batch'


class Settings:
    json_input_folder = './exported_resources/'
    json_output_folder = './transformed_bundles/'
    server_url = ''


def bundle_entries_resources(bundle_dict):
    for entry in bundle_dict["entry"]:
        yield entry['resource']


def bundle_type_is(bundle_dict, bundle_type):
    return bundle_dict.get('type') == bundle_type


def searchset_to_transaction(bundle_dict, method):
    assert bundle_type_is(bundle_dict, BundleTypes.searchset), "This bundle is not searchset"

    entries = []
    res_bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": entries,
    }

    for resource_dict in bundle_entries_resources(bundle_dict):
        entries.append(transaction_entry(resource_dict, method))

    return res_bundle


def transaction_entry(resource_dict, method):
    resource_url = f"{resource_dict['resourceType']}/{resource_dict['id']}"
    return {
        'resource': resource_dict,
        'request': {
            'method': method.upper(),
            'url': resource_url
        },
        'fullUrl': os.path.join(Settings.server_url, resource_url)
    }


def main():
    for file_path in pathlib.Path(Settings.json_input_folder).glob('**/*.json'):
        with open(file_path, "r") as json_file:
            bundle_dict = json.load(json_file)

        transaction_bundle = searchset_to_transaction(bundle_dict, 'post')
        request_result_filepath = os.path.join(Settings.json_output_folder, f"{bundle_dict['id']}.json")
        with open(request_result_filepath, "w") as outfile:
            json.dump(transaction_bundle, outfile, indent=2)


if __name__ == '__main__':
    if os.path.isdir(Settings.json_output_folder):
        shutil.rmtree(Settings.json_output_folder)
    os.mkdir(Settings.json_output_folder)
    main()
