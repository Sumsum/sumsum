import re
import unicodedata


invalid_pat = re.compile(r'[^-a-z0-9]')
limit_pat = re.compile(r'-{2,}')
uncamel_patterns = (
    re.compile('(.)([A-Z][a-z]+)'),
    re.compile('([a-z0-9])([A-Z])'),
)


def slugify(s):
    # normalize to ascii
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf8')
    # lowercase
    s = s.lower()
    # make invalid chars -
    s = invalid_pat.sub('-', s)
    # limit - to one
    s = limit_pat.sub('-', s)
    # strip -
    s = s.strip('-')
    return s


def uncamel(s, split_char='-'):
    """
    Make camelcase lowercase and use dash (or other char).

        >>> uncamel('CamelCase')
        'camel_case'
        >>> uncamel('CamelCamelCase')
        'camel_camel_case'
        >>> uncamel('Camel2Camel2Case')
        'camel2_camel2_case'
        >>> uncamel('getHTTPResponseCode')
        'get_http_response_code'
        >>> uncamel('get2HTTPResponseCode')
        'get2_http_response_code'
        >>> uncamel('HTTPResponseCode')
        'http_response_code'
        >>> uncamel('HTTPResponseCodeXYZ')
        'http_response_code_xyz'
    """
    for pat in uncamel_patterns:
        s = pat.sub(r'\1{}\2'.format(split_char), s)
    return s.lower()
