import unittest

from DatabaseEngineModule2.Alteration import *
from DatabaseEngineModule2.VersionsRange import *


class TestAlteration(unittest.TestCase):

    def setUp(self):
        pass

    def test_init(self):
        alteration = Alteration({'key': 'value'}, VersionsRange(version=0))
        alteration_2 = Alteration({'key': 'value'}, VersionsRange(version=0))
        self.assertTrue(alteration.get_creation_time() < alteration_2.get_creation_time())

    def test_merge(self):
        #Проверим случай, когда "шарики" относятся к разным версиям и более поздняя перекрывает.
        alteration = Alteration(
            {
                'a': 1,
                'b': 1
            }
            , VersionsRange(version=0)
        )
        alteration_2 = Alteration(
            {
                'b': 2,
                'c': 2
            }
            , VersionsRange(version=0)
        )
        merged = Alteration.merge([alteration, alteration_2])
        # self.assertEqual(
        #     merged.get_changes(),
        #     {
        #         'a': 1,
        #         'b': 1,
        #         'c': 2
        #     }
        # )