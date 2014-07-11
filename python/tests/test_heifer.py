import unittest

import sys

sys.path.append("../src")

try:
    import heifer
except ImportError:
    from python.src import heifer


class TestHeifer(unittest.TestCase):
    def test_method_online(self):

        heifer.connect()
        heifer._start_editing()

        keys = ['age', 'bcc', 'bcs', 'birth_date', 'birth_weight', 'breed',
                'date', 'hip', 'index', 'ladg', 'madg', 'weight']

        heifer_list = heifer.get_heifer_information("Index==4999")
        self.assertTrue(isinstance(heifer_list, list))

        for json_dict in heifer_list:
            # Assert all of the keys are in item
            intersection = set(keys).intersection(json_dict)
            self.assertEqual(12, len(intersection))

        heifer._save_cache("../src/heifer_cache.json")

    def test_method_offline(self):
        heifer.disconnect("../src/heifer_cache.json")

        keys = ['age', 'bcc', 'bcs', 'birth_date', 'birth_weight', 'breed',
                'date', 'hip', 'index', 'ladg', 'madg', 'weight']

        heifer_list = heifer.get_heifer_information("Index==4999")
        self.assertTrue(isinstance(heifer_list, list))

        for json_dict in heifer_list:
            # Assert all of the keys are in item
            intersection = set(keys).intersection(json_dict)
            self.assertEqual(12, len(intersection))


    def test_throw_exception(self):
        heifer.connect()

        with self.assertRaises(heifer.HeiferException) as context:
            heifer.get_heifer_information(["AAPL"])

        self.assertEqual('MSG', context.exception.args[0])

        with self.assertRaises(heifer.HeiferException) as context:
            heifer.get_heifer_information_(1)

        self.assertEqual('MSG', context.exception.args[0])

        with self.assertRaises(heifer.HeiferException) as context:
            heifer.get_heifer_information("INVALID_STOCK")

        self.assertEqual('MSG', context.exception.args[0])
