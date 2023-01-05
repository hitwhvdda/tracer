def check_single_point_skip_link(item):
    return ('file' in item) \
        and (item['file']) \
        and (item['line'] and type(item['line']) == int)


def check_two_point_skip_link(item):
    return ('source' in item \
        and item['source'])  \
        and (item['source']['file']) \
        and (item['source']['line'] and type(item['source']['line']) == int) \
        and ('sink' in item \
        and item['sink']) \
        and (item['sink']['file']) \
        and (item['sink']['line'] and type(item['sink']['line']) == int)


def check_single_point(item):
    return check_single_point_skip_link(item) and item['code']


def check_two_point(item):
    return check_two_point_skip_link(item) \
        and item['source']['code'] \
        and item['sink']['code']
