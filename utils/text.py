import re
import unicodedata


invalid_pat = re.compile(r'[^-a-z0-9]')
limit_pat = re.compile(r'-{2,}')


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
