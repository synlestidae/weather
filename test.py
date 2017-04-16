import unittest
import os
import sys
import json
from apiclient.http import HttpMockSequence
from db import setup_database
from user import Users
import sqlite3
from app import authorise_user

#data = None
# with open("client_secrets.json") as json_file:
#  data = json.load(data_file)


def get_test_connection():
    return sqlite3.connect('test_database.db')


def mockOAuthHTTPSeq():
    sequence = HttpMockSequence([
        ({'status': '200'}, """{
      "access_token": "ya29.GlsuBHHALQIPW9cJOm2l64XgOLr1IuFG9-9dy6-f0HcgxSdjrAzCgUILuLWeX9gtWw4P6hQjq9auED1pOqFKEtaWL0wqyroYZZYtbGZ91r32UkWNqHAoLOtyR7J4", 
      "token_type": "Bearer", 
      "expires_in": 3600, 
      "refresh_token": "1/IeRDLrcjf-n0BiDiHHhyNmlzESUFIICB-E6rhdiXmsM", 
      "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImVhYzY0YTBjZmMxMjljMGFiYzFlN2E2NGE2M2EyMGMyNGIwMDQ4OGEifQ.eyJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTExMDI0Nzg4NDE2OTA1MzE5MjkiLCJhdF9oYXNoIjoiWlRDZ0FNUlNqcGhEVi1uU1d0MGdWUSIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsImlhdCI6MTQ5MjI5MTQ0MiwiZXhwIjoxNDkyMjk1MDQyfQ.f4T4ULWdn-Xnm4VIoILnBvDpe-GGsufFFY9IN2Z9_ZJfnV1X6BkXlI3d9SUW-gKzuAO8YSxKP7owh6eL93ls0HXpCAYIYnh2faG7tWplRu_LvSCRau12fMd5FFbeuOHbmJ2OA5pOddHIEaEj-YofNu2EEbMUSsA81R8dqaqnt8xBhHqoB-TEC9nKeaEtoDPw6vHMgkx2OThfhxQrKOiQJSHRMaj-tYR4i8uNMPSPpQ8lHmYnZ53GUiNb6rCDqUlmK2RN-uLtc2l_s72n9WfOxXNDMcD7pvj2zTtLS4_EHuuzpsYpmcz-TSu9v-f9TGUIJ29XJy4842LH0HTIMaIrUQ"}"""),
        ({'status': 200}, open('test_discover.json').read()),
        ({'status': 200}, open("test_me.json").read())])
    return sequence


class test_XXX_Test_Group_Name(unittest.TestCase):
    def setUp(self):
        test_database = get_test_connection()  # sqlite3.connect('database.db')
        setup_database(test_database)
        # XXX code to do setup
        self.oauth_http = mockOAuthHTTPSeq()

    def connect(self):
        return sqlite3.connect('test_database.db')

    def tearDown(self):
        # XXX code to do tear down
        os.unlink("test_database.db")

    def test_adds_one_user_to_database(self):
        users = Users(self.connect())
        person_id = authorise_user("4/7J5j83SwLmZGEg6mADDnotLWdZnMyiRZFzOIWtE1Wxk", "",
                                   self.oauth_http,
                                   self.connect())
        self.assertEqual(len(users.get_users()), 1)

    def test_adds_one_user_to_database(self):
        users = Users(self.connect())
        person_id = authorise_user("4/7J5j83SwLmZGEg6mADDnotLWdZnMyiRZFzOIWtE1Wxk", "",
                                   self.oauth_http,
                                   self.connect())
        self.assertEqual(len(users.get_users()), 1)

    #  Examples:
    # self.assertEqual(fp.readline(), 'This is a test')
    # self.assertFalse(os.path.exists('a'))
    # self.assertTrue(os.path.exists('a'))
    # self.assertTrue('already a backup server' in c.stderr)
    # self.assertIn('fun', 'disfunctional')
    # self.assertNotIn('crazy', 'disfunctional')
    # with self.assertRaises(Exception):
    #	raise Exception('test')
    #
    # Unconditionally fail, for example in a try block that should raise
    # self.fail('Exception was not raised')

    #@unittest.skipIf('SKIP_SLOW_TESTS' in os.environ, 'Requested fast tests')
    # def test_XXX_Slow_Test_Name(self):
    #    raise NotImplementedError('Insert test code here.')


unittest.main()
