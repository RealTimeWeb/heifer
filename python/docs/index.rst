.. facebook documentation master file, created by
   sphinx-quickstart on Tue Jul 30 14:19:10 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to Facebook Service's documentation!
============================================

The Facebook Service library offers access to your Facebook likes, statuses, and
friends list.

.. code-block:: python

  >>> import facebook

You can get information for your profile or for someone else's (public) facebook profile

.. code-block:: python

  >>> ACCESS_TOKEN = CAACEdEose0cBAId0gptt0yZAuj4NAZAO4aokpZCBuaHnZCorCV1hncZCMSMWCYtTL1AKx0fzGOpQAHXly6fIDllCUrkl0
  >>> user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
  >>> user_dict
  {'id': u'18394577592', 'name': u'John Doe', 'likes': [{'name': 'Football', 'category': 'Sports'}], 'statuses': [{'message': "Hello", 'from': 'Jane Doe', 'id': '11238249823', 'updated_time': '???'}]}

If you wish to access information within the dictionary, you can do so by
specifying the key to use and the value will be returned.

.. code-block:: python

  >>> user_dict['name']
  u'John Doe'
  >>> user_dict['likes']
  [{'name': 'Football', 'category': 'Sports'}]
  >>> user_dict['statuses']
  [{'message': "Hello", 'from': 'Jane Doe', 'id': '11238249823', 'updated_time': '???'}]

Here is the complete list of information that can be retrieved from the dictionary

========================  ============
Keys                      Explanation
========================  ============
id                        the id for the facebook user
name                      the name of the facebook user
likes                     a list of like dictionaries for a facebook user
statuses                  a list of status dictionaries for a facebook user
========================  ============

The built-in cache allows you to work online:

.. code-block:: python

  >>> facebook.connect() # unnecessary: default is connected

or offline:

.. code-block:: python

  >>> facebook.disconnect()
  >>> facebook.get_facebook_information(ACCESS_TOKEN)
  {'id': u'18394577592', 'name': u'John Doe', 'likes': [{'name': 'Football', 'category': 'Sports'}], 'statuses': [{'message': "Hello", 'from': 'Jane Doe', 'id': '129486948', 'updated_time': '???'}]}

But remember there must be data in the cache already!

.. code-block:: python

  >>> facebook.get_facebook_information(ACCESS_TOKEN)
  facebook.FacebookException: There were no results

Populating the cache
^^^^^^^^^^^^^^^^^^^^

Say you want to add your information to the cache

.. code-block:: python

  >>> facebook._start_editing()
  >>> user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
  >>> facebook._save_cache()

Now the file "cache.json" file will have an entry for your information, and
you can use that as an input to the function when disconnected.

You can also create a different cache file by passing a filename to the
_save_cache() method, and use that cache by passing its name to the
disconnect() method.

For example, this will populate a file called "me.json"

.. code-block:: python

  >>> facebook._start_editing()
  >>> user_dict = facebook.get_facebook_information(ACCESS_TOKEN)
  >>> facebook._save_cache("me.json")

To use that cached file, specify the json file name when you call disconnect():

.. code-block:: python

  >>> facebook.disconnect("me.json")

Finally, you can put multiple entries into the cache for a given input, simulating multiple calls. These items will be appended. If the cache runs out, it will start returning empty reports.

.. code-block:: python

  >>> facebook.connect()
  >>> facebook._start_editing()
  >>> facebook.get_facebook_information(ACCESS_TOKEN)
  >>> facebook.get_facebook_information(ACCESS_TOKEN, fb_id="129486948")
  >>> facebook._save_cache()
  >>> facebook.disconnect()
  >>> facebook.get_facebook_information(ACCESS_TOKEN)
  {'id': u'18394577592', 'name': u'John Doe', 'likes': [{'name': 'Football', 'category': 'Sports'}], 'statuses': [{'message': "Hello", 'from': 'Jane Doe', 'id': '129486948', 'updated_time': '???'}]}
  >>> facebook.get_facebook_information(ACCESS_TOKEN, fb_id="129486948")
  {'id': u'129486948', 'name': u'Jane Doe', 'likes': [{'name': 'Football', 'category': 'Sports'}], 'statuses': [{'message': "Hello", 'from': 'John Doe', 'id': '18394577592', 'updated_time': '???'}]}


Exceptions
----------

.. autoexception:: facebook.FacebookException


.. Classes
.. -------

.. .. autoclass:: facebook.Stock

Methods
-------

.. autofunction:: facebook.connect()

.. autofunction:: facebook.disconnect()

.. autofunction:: facebook.get_messages(access_token=None)

.. autofunction:: facebook.get_facebook_information(access_token=None)