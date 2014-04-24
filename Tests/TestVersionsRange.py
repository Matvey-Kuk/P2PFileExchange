import unittest

from DatabaseEngineModule.VersionsRange import *


class TestVersionsRange(unittest.TestCase):

    def setUp(self):
        pass

    def test_dump_and_restore(self):
        a = VersionsRange(first=2, last=5)
        b = VersionsRange(dump=a.get_dump())
        self.assertEqual(a, b)

    def test_subtraction(self):

        #Проверим случай, если вычитаемое внутри диапазона полностью
        a = VersionsRange(first=2, last=15)
        b = VersionsRange(first=4, last=10)
        self.assertTrue(VersionsRange(first=2, last=3) in VersionsRange.subtraction(a, b))
        self.assertTrue(VersionsRange(first=11, last=15) in VersionsRange.subtraction(a, b))

        #Проверим случай, если вычитаемое заходит на диапазон слева и касается левого края
        a = VersionsRange(first=2, last=15)
        b = VersionsRange(first=2, last=10)
        self.assertTrue(VersionsRange(first=11, last=15) in VersionsRange.subtraction(a, b))
        self.assertEqual(len(VersionsRange.subtraction(a, b)), 1)

        #Проверим случай, если вычитаемое перекрывает левый край...
        a = VersionsRange(first=2, last=15)
        b = VersionsRange(first=0, last=10)
        self.assertTrue(VersionsRange(first=11, last=15) in VersionsRange.subtraction(a, b))
        self.assertEqual(len(VersionsRange.subtraction(a, b)), 1)

        #Проверим еще какую-то фигню...
        a = VersionsRange(first=2, last=15)
        b = VersionsRange(first=0, last=16)
        self.assertEqual(len(VersionsRange.subtraction(a, b)), 0)

        #И еще...
        a = VersionsRange(first=2, last=15)
        b = VersionsRange(first=16, last=20)
        self.assertTrue(VersionsRange(first=2, last=15) in VersionsRange.subtraction(a, b))
        self.assertEqual(len(VersionsRange.subtraction(a, b)), 1)