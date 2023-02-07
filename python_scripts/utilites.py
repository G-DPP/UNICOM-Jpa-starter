import os.path

import requests


def get_next_searchset(bundle):

    try:
        return next(x['url'] for x in bundle['link'] if x['relation'] == 'next')
    except StopIteration:
        return None


def get_resource(fhir_entrypoint='', resource_name=''):
    return requests.get(os.path.join(fhir_entrypoint, resource_name)).json()
