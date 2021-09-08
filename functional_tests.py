#!/usr/bin/env python

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest


class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        server = "http://127.0.0.1:4444/wd/hub"
        self.browser = webdriver.Remote(
            command_executor=server,
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class HomePageViewTest(SeleniumTestCase):
    def test_user_can_see_homepage(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('Bloodhound', self.browser.title)


class ApiHomePageViewTest(SeleniumTestCase):
    def test_user_can_see_api_homepage(self):
        self.browser.get('http://localhost:8000/api')

        self.assertIn('Api Root', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
