from Tests.Functional.FunctionalTestEngine.FunctionalTestEngine import *

import tempfile
import unittest


class TestUsersDatabase(unittest.TestCase):

    def setUp(self):
        self.functional_tester = FunctionalTestEngine()
        self.instances = []
        for i in range(3):
            self.instances.append(self.functional_tester.make_instance())

    def test_register_user(self):
        print('Testing auth register_user command')
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

    def test_working_with_groups(self):
        print('Testing working with groups')
        self.assertEqual(
            self.functional_tester.send_command(self.instances[0], 'auth register group_administrator'),
            'Successfully registered!'
        )
        print('user added')
        sleep(5)
        self.assertEqual(
            self.functional_tester.send_command(self.instances[0], 'auth add_user_to_group group_name group_user'),
            'Succeed!'
        )
        print('group added')
        sleep(5)
        self.assertEqual(
            self.functional_tester.send_command(
                self.instances[0],
                'auth show_users_in_group group_administrator group_name'
            ),
            'Succeed!'
        )

    def test_save_keys_to_file_and_restore(self):
        print('Testing "auth save_keys" and "auth auth_as" commands')
        keys_file = tempfile.NamedTemporaryFile()
        self.functional_tester.send_command(self.instances[0], 'auth logout')
        self.functional_tester.send_command(self.instances[0], 'auth register username')
        self.assertEqual(
            self.functional_tester.send_command(self.instances[0], 'auth save_keys ' + keys_file.name),
            'Success.'
        )
        connection_time = self.functional_tester.send_command(
            self.instances[0],
            'auth show_last_connection_time username'
        )
        self.functional_tester.send_command(self.instances[0], 'auth logout')
        self.assertEqual(
            self.functional_tester.send_command(self.instances[0], 'auth load_keys ' + keys_file.name),
            'Logged in.'
        )
        connection_time2 = self.functional_tester.send_command(
            self.instances[1],
            'auth show_last_connection_time username'
        )
        self.assertEqual(
            connection_time,
            connection_time2
        )
        sleep(10)
        connection_time2 = self.functional_tester.send_command(
            self.instances[1],
            'auth show_last_connection_time username'
        )
        self.assertNotEqual(
            connection_time,
            connection_time2
        )
        self.functional_tester.send_command(self.instances[0], 'auth logout')

    def tearDown(self):
        self.functional_tester.kill_instances()