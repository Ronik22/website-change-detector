from django.test import TestCase
import os
import shutil
from wcd_mainapp.html_wcd import HtmlWCD
from wcd_mainapp.image_wcd import ImageWCD
from wcd_mainapp.text_wcd import TextWCD

# Create your tests here.

class BaseTest(TestCase):
    def setUp(self):
        self.folder_name="./TEST_WCD_helpers"
        self.test_id = 1
        self.url = "https://github.com/Ronik22"
        self.full_css = "full"
        self.part_css = "full"
        self.high_threshold = 1.0
        self.low_threshold = 0.1

        if not os.path.exists(self.folder_name):
            os.mkdir(self.folder_name)
        return super().setUp()

    def tearDown(self):
        if os.path.exists(self.folder_name):
            shutil.rmtree(self.folder_name)
        print("teardown... deleting test folder")
        super().tearDown()

class WcdTest(BaseTest):
    def test_HTML_WCD_firsttime(self):
        ob = HtmlWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        self.assertEqual(info["firsttime"], True)

    def test_HTML_WCD_not_firsttime_high_threshold(self):
        ob = HtmlWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], True)
        self.assertLessEqual(info2["similarity"], self.high_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), True)

    def test_HTML_WCD_not_firsttime_low_threshold(self):
        ob = HtmlWCD(self.test_id, self.url, self.full_css, self.low_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], False)
        self.assertGreaterEqual(info2["similarity"], self.low_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), False)

    def test_Text_WCD_firsttime(self):
        ob = TextWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        self.assertEqual(info["firsttime"], True)

    def test_Text_WCD_not_firsttime_high_threshold(self):
        ob = TextWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], True)
        self.assertLessEqual(info2["similarity"], self.high_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), True)

    def test_Text_WCD_not_firsttime_low_threshold(self):
        ob = TextWCD(self.test_id, self.url, self.full_css, self.low_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], False)
        self.assertGreaterEqual(info2["similarity"], self.low_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), False)

    def test_Image_WCD_firsttime(self):  
        ob = ImageWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        self.assertEqual(info["firsttime"], True)

    def test_Image_WCD_not_firsttime_high_threshold(self):
        ob = ImageWCD(self.test_id, self.url, self.full_css, self.high_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], True)
        self.assertLessEqual(info2["similarity"], self.high_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), True)

    def test_Image_WCD_not_firsttime_low_threshold(self):
        ob = ImageWCD(self.test_id, self.url, self.full_css, self.low_threshold)
        ob.folder = self.folder_name
        info = ob.run()
        info2 = ob.run()
        self.assertEqual(info["firsttime"], True)
        self.assertEqual(info2["firsttime"], False)
        self.assertEqual(info2["ischanged"], False)
        self.assertGreaterEqual(info2["similarity"], self.low_threshold)
        self.assertEqual(os.path.exists(info2["filepath"]), False)
        

class URLTestNoLogin(TestCase):
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_tasks_nologin(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 302)
    
    def test_tasks_add_nologin(self):
        response = self.client.get('/tasks/add/')
        self.assertEqual(response.status_code, 302)