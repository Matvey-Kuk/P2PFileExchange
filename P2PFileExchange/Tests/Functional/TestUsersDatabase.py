from Tests.Functional.FunctionalTestEngine.FunctionalTestEngine import *

import unittest


class TestUsersDatabase(unittest.TestCase):

    def setUp(self):
        self.functional_tester = FunctionalTestEngine()
        self.instances = []
        for i in range(3):
            self.instances.append(self.functional_tester.make_instance())

    def test_register_user(self):
        for i in range(len(self.instances)):
            self.assertEqual(
                self.functional_tester.send_command(self.instances[i], 'auth register user' + str(i)),
                'Successfully registered!'
            )
            print('Instance is successfully checked.')
            sleep(5)
        sleep(5 * len(self.instances))
        for i in range(len(self.instances)):
            answer = self.functional_tester.send_command(self.instances[i], 'auth show')
            for i in range(len(self.instances)):
                self.assertTrue(('user' + str(i)) in answer)
        for i in range(len(self.instances)):
            self.assertEqual(
                sorted(
                    self.functional_tester.send_command(self.instances[i], 'auth show_users').split(' ')
                ),
                ['user0', 'user1', 'user2']
            )
            print('Instance is successfully checked.')

    def tearDown(self):
        self.functional_tester.kill_instances()