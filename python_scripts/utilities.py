def next_bundle_page(json_response):
    try:
        next_page = next(x for x in json_response['link'] if x['relation'] == 'next')
        if next_page:
            return next_page
    except StopIteration:
        return None

