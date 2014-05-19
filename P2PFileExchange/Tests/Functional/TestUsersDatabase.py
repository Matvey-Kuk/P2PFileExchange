from FunctionalTests.FunctionalTester import FunctionalTester

import unittest


class TestUsersDatabase(unittest.TestCase):

    def setUp(self):
        self.functional_tester = FunctionalTester()
        self.instances = []
        for i in range(2):
            self.instances.append(self.functional_tester.make_instance())

    def test_register_user(self):
        print(self.functional_tester.send_command(self.instances[0], 'auth register matvey'))

    def tearDown(self):
        print('test_ended')
        self.functional_tester.kill_instances()