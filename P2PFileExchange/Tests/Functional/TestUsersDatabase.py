from Tests.Functional.FunctionalTestEngine.FunctionalTestEngine import *

import unittest


class TestUsersDatabase(unittest.TestCase):

    def setUp(self):
        self.functional_tester = FunctionalTestEngine()
        self.instances = []
        for i in range(20):
            self.instances.append(self.functional_tester.make_instance())

    def test_register_user(self):
        print(self.functional_tester.send_command(self.instances[0], 'auth register matvey'))

    def tearDown(self):
        print('test_ended')
        self.functional_tester.kill_instances()