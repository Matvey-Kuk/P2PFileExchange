# from Tests.Functional.FunctionalTestEngine.FunctionalTestEngine import *
#
# import unittest
#
#
# class TestUsersDatabase(unittest.TestCase):
#
#     def setUp(self):
#         self.functional_tester = FunctionalTestEngine()
#         self.instances = []
#         for i in range(2):
#             self.instances.append(self.functional_tester.make_instance())
#
#     def test_show_peers(self):
#         for i in range(len(self.instances)):
#             self.assertIn(
#                 '127.0.0.1:',
#                 self.functional_tester.send_command(self.instances[i], 'p2p show_peers')
#             )
#             print('Instance is successfully checked.')
#
#     def tearDown(self):
#         self.functional_tester.kill_instances()