from __future__ import print_function
import sys
import json
from datetime import datetime as dt

HEADER = {'User-Agent': 'RealTimeWeb Heifer library for educational purposes'}
PYTHON_3 = sys.version_info >= (3, 0)

if PYTHON_3:
    import urllib.error
    import urllib.request as request
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus


# Auxilary


def _parse_float(value, default=0.0):
    """
    Attempt to cast *value* into a float, returning *default* if it fails.
    """
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _iteritems(_dict):
    """
    Internal method to factor-out Py2-to-3 differences in dictionary item
    iterator methods

    :param dict _dict: the dictionary to parse
    :returns: the iterable dictionary
    """
    if PYTHON_3:
        return _dict.items()
    else:
        return _dict.iteritems()


def _urlencode(query, params):
    """
    Internal method to combine the url and params into a single url string.

    :param str query: the base url to query
    :param dict params: the parameters to send to the url
    :returns: a *str* of the full url
    """
    return query + '?' + '&'.join(
        key + '=' + quote_plus(str(value)) for key, value in _iteritems(params))


def _get(url):
    """
    Internal method to convert a URL into it's response (a *str*).

    :param str url: the url to request a response from
    :returns: the *str* response
    """
    if PYTHON_3:
        req = request.Request(url, headers=HEADER)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    else:
        req = urllib2.Request(url, headers=HEADER)
        response = urllib2.urlopen(req)
        return response.read()


def _recursively_convert_unicode_to_str(input):
    """
    Force the given input to only use `str` instead of `bytes` or `unicode`.

    This works even if the input is a dict, list, or a string.

    :params input: The bytes/unicode input
    :returns str: The input converted to a `str`
    """
    if isinstance(input, dict):
        return {_recursively_convert_unicode_to_str(
            key): _recursively_convert_unicode_to_str(value) for key, value in
                input.items()}
    elif isinstance(input, list):
        return [_recursively_convert_unicode_to_str(element) for element in
                input]
    elif not PYTHON_3:
        return input.encode('utf-8')
    elif PYTHON_3 and isinstance(input, str):
        return str(input.encode('ascii', 'replace').decode('ascii'))
    else:
        return input


# Cache

_CACHE = {}
_CACHE_COUNTER = {}
_EDITABLE = False
_CONNECTED = True
_PATTERN = "repeat"


def _start_editing(pattern="repeat"):
    """
    Start adding seen entries to the cache. So, every time that you make a request,
    it will be saved to the cache. You must :ref:`_save_cache` to save the
    newly edited cache to disk, though!
    """
    global _EDITABLE, _PATTERN
    _EDITABLE = True
    _PATTERN = pattern


def _stop_editing():
    """
    Stop adding seen entries to the cache.
    """
    global _EDITABLE
    _EDITABLE = False


def _add_to_cache(key, value):
    """
    Internal method to add a new key-value to the local cache.
    :param str key: The new url to add to the cache
    :param str value: The HTTP response for this key.
    :returns: void
    """
    if key in _CACHE:
        _CACHE[key].append(value)
    else:
        _CACHE[key] = [_PATTERN, value]
        _CACHE_COUNTER[key] = 0


def _clear_key(key):
    """
    Internal method to remove a key from the local cache.
    :param str key: The url to remove from the cache
    """
    if key in _CACHE:
        del _CACHE[key]


def _save_cache(filename="cache.json"):
    """
    Internal method to save the cache in memory to a file, so that it can be used later.

    :param str filename: the location to store this at.
    """
    with open(filename, 'w') as f:
        json.dump({"data": _CACHE, "metadata": ""}, f)


def _lookup(key):
    """
    Internal method that looks up a key in the local cache.

    :param key: Get the value based on the key from the cache.
    :type key: string
    :returns: void
    """
    if key not in _CACHE:
        return ""
    if _CACHE_COUNTER[key] >= len(_CACHE[key][1:]):
        if _CACHE[key][0] == "empty":
            return ""
        elif _CACHE[key][0] == "repeat" and _CACHE[key][1:]:
            return _CACHE[key][-1]
        elif _CACHE[key][0] == "repeat":
            return ""
        else:
            _CACHE_COUNTER[key] = 1
    else:
        _CACHE_COUNTER[key] += 1
    if _CACHE[key]:
        return _CACHE[key][_CACHE_COUNTER[key]]
    else:
        return ""


def connect():
    """
    Connect to the online data source in order to get up-to-date information.

    :returns: void
    """
    global _CONNECTED
    _CONNECTED = True


def disconnect(filename="../src/cache.json"):
    """
    Connect to the local cache, so no internet connection is required.

    :returns: void
    """
    global _CONNECTED, _CACHE
    try:
        with open(filename, 'r') as f:
            _CACHE = _recursively_convert_unicode_to_str(json.load(f))['data']
    except (OSError, IOError) as e:
        raise HeiferException(
            "The cache file '{}' was not found.".format(filename))
    for key in _CACHE.keys():
        _CACHE_COUNTER[key] = 0
    _CONNECTED = False


# Exceptions

class HeiferException(Exception):
    pass


# Domain Objects


class Heifer(object):
    """
    A Heifer contains
    """

    def __init__(self, age=None, bcc=None, bcs=None, birth_weight=None,
                 birth_date=None, breed=None, date=None, hip=None, index=None,
                 ladg=None, loc=None, madg=None, weight=None):

        """
        Creates a new heifer

        :returns: Heifer
        """

        self.age = age
        self.bcc = bcc
        self.bcs = bcs
        self.birth_weight = birth_weight
        self.birth_date = birth_date
        self.breed = breed
        self.date = date
        self.hip = hip
        self.index = index
        self.ladg = ladg
        self.madg = madg
        self.weight = weight

    def __unicode__(self):
        string = """ <Heifer Index: {0}, Breed: {1}> """
        return string.format(self.index, self.breed)

    def __repr__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def __str__(self):
        string = self.__unicode__()

        if not PYTHON_3:
            return string.encode('utf-8')

        return string

    def _to_dict(self):
        heifer_dict = dict(age=self.age, bcc=self.bcc, bcs=self.bcs,
                           birth_weight=self.birth_weight, breed=self.breed,
                           hip=self.hip, index=self.index, ladg=self.ladg,
                           madg=self.madg, weight=self.weight,
                           birth_date=self.birth_date.strftime("%m/%d/%Y"),
                           date=self.date.strftime("%m/%d/%Y"))

        return heifer_dict


    @staticmethod
    def _from_json(json_data):
        """
        Creates a Heifer from json data.

        :param json_data: The raw json data to parse
        :type json_data: dict
        :returns: Heifer
        """
        if json_data is None:
            return Heifer()
        try:
            json_dict = json_data
            age = json_dict['Age']
            bcc = json_dict['BCC']
            bcs = json_dict['BCS']
            birth_weight = json_dict['Birth Wt']
            birth_date = dt.strptime(json_dict['Birthdate'], "%Y-%m-%d %H:%M:%S")
            breed = json_dict['Brd']
            date = dt.strptime(json_dict['Date'], "%Y-%m-%d %H:%M:%S")
            hip = json_dict['Hip']
            index = json_dict['Index']
            ladg = json_dict['LADG']
            loc = json_dict['Loc']
            madg = json_dict['MADG']
            weight = json_dict['Wt']

            heifer = Heifer(age=age, bcc=bcc, bcs=bcs, birth_weight=birth_weight,
                            birth_date=birth_date, breed=breed, date=date, hip=hip,
                            index=index, ladg=ladg, loc=loc, madg=madg, weight=weight)
            return heifer

        except KeyError:
            raise HeiferException("The given information was incomplete.")


# Service Methods


def _fetch_heifer_info(params):
    """
    Internal method to form and query the server

    :param dict params: the parameters to pass to the server
    :returns: the JSON response object
    """
    from collections import OrderedDict

    baseurl = 'http://think.cs.vt.edu:5000/heifer1'
    # An ordered dictionary is necessary since an ordinary dictionary has no ordering which causes
    # problems when trying to retrieve an item from the cache
    ordered_dict = OrderedDict(
        sorted(_iteritems(params), key=lambda x: x[1], reverse=True))
    query = _urlencode(baseurl, ordered_dict)

    if PYTHON_3:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib.error.HTTPError:
            raise HeiferException("Make sure you entered a valid query")
    else:
        try:
            result = _get(query) if _CONNECTED else _lookup(query)
        except urllib2.HTTPError:
            raise HeiferException("Make sure you entered a valid query")

    if not result:
        raise HeiferException("There were no results")

    result = result.replace("// ", "")  # Remove Double Slashes
    result = " ".join(
        result.split())  # Remove Misc 1+ Spaces, Tabs, and New Lines

    try:
        if _CONNECTED and _EDITABLE:
            _add_to_cache(query, result)
        json_res = json.loads(result)
    except ValueError:
        raise HeiferException("Internal Error")

    return json_res


def get_heifer_information(query):
    """
    Forms and poses the query to get information from the database
    :param query: the values to retrieve
    :return: the JSON response
    """
    if not isinstance(query, str):
        raise HeiferException("Please enter a valid query")

    params = {'where': query}
    json_res = _fetch_heifer_info(params)
    json_list = json_res['_items']

    heifers = []

    for json_dict in json_list:
        heifer = Heifer._from_json(json_dict)
        heifers.append(heifer)

    return [heifer._to_dict() for heifer in heifers]