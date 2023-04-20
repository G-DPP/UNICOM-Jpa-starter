import requests
import json
import os
import tarfile
import urllib.request
import pathlib
from dotenv import load_dotenv
import shutil
import time

load_dotenv()

IG_URL = os.getenv('ig_url')
print(f"{IG_URL=}")

package_url = f"{IG_URL}/package.tgz"
print(f"{package_url=}")

server_url = os.getenv('import_server_url', f'http://localhost:{os.getenv("server_port", "8080")}')
server_url += "/fhir/"
print(f"The data will be uploaded to {server_url}")

result_dir = "./output"
if os.path.isdir(result_dir):
    shutil.rmtree(result_dir)
os.mkdir("./output")

resource_list = [
    'codesystem',
    'valueset',
    'structuredefinition',  # TODO: 400
    'bundle',
    'medicinalproductdefinition',
    'organization',
    'manufactureditemdefinition',
    'packagedproductdefinition',
    'regulatedauthorization',
    'administrableproductdefinition',
    'ingredient',
    'implementationguide',
    'searchparameter'
]


def create_or_update(request_url, resource_type, resource_id, data):
    headers = {
        "Content-Type": "application/fhir+json"
    }
    if resource_type.lower() == "structuredefinition" or resource_type.lower() == 'bundle' or resource_type.lower() == 'implementationguide':
        response = requests.post(request_url, json=data)
    else:
        url = f"{request_url}/{resource_id}"
        data = json.dumps(data)
        response = requests.put(url, headers=headers, data=data.encode())
    return response


def main():
    # urllib.request.urlretrieve(package_url, "package.tgz")
    # file = tarfile.open('package.tgz')
    # file.extractall('./')
    results = {}

    package_folder = "./packages"
    for item in resource_list:
        for file_path in pathlib.Path(package_folder).glob('**/*.json'):
            with open(file_path, "r") as json_file:
                file_name = str(file_path).rsplit('/', 1)[1]
                json_dict = json.load(json_file)
                resource_type = json_dict.get('resourceType', '')
                resource_id = json_dict.get('id', '')
                type = json_dict.get("type", '')

                if resource_type.lower() != item:
                    continue
                print("#-FILENAME "+file_name)

                request_url = f"{server_url}{resource_type}" if isinstance(type, dict) or type.lower() not in ["transaction", "batch"] else server_url
                a = create_or_update(request_url, resource_type, resource_id, json_dict)

                request_result_dir = f"{result_dir}/{a.status_code}"
                request_result_filepath = f"{request_result_dir}/{file_name}"
                if not os.path.isdir(request_result_dir):
                    os.mkdir(request_result_dir)

                with open(request_result_filepath, "w") as outfile:
                    json.dump(a.json(), outfile, indent=2)

                item_results = results.setdefault(item, {})
                item_results.setdefault(a.status_code, []).append(file_path)

                print(f"{file_path} -- {a.status_code}")
        print(f"FINISH RESOURCE {item}")
        time.sleep(3)

    print("Report")
    for item, status_codes in results.items():
        print(f"\n- {item} -----------")
        for status_code, resource_results in status_codes.items():
            print(f"\tstatus {status_code}: {len(resource_results)} resources")
    print("------------------------------")
    print("DONE!")


if __name__ == '__main__':
    main()
