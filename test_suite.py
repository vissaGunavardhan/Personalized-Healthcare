import os
import unittest
import json
from app import app
import database
from abdm_service import ABDMService
from ocr_engine import OCREngine

class DigitalHealthPortalTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        database.init_db()

    def test_01_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HealthVault", response.data)
        self.assertIn(b"Unified Digital Health Vault", response.data)

    def test_02_demo_login_ramesh(self):
        response = self.client.get('/demo-login/ramesh', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ramesh Kumar", response.data)

    def test_03_ocr_page_and_api(self):
        # View page
        res = self.client.get('/ocr')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Medical Report OCR", res.data)

        # Test preset OCR API
        res_api = self.client.post('/api/ocr/analyze', data={'preset': 'diabetes'})
        self.assertEqual(res_api.status_code, 200)
        data = json.loads(res_api.data)
        self.assertTrue(data['success'])
        self.assertIn('biomarkers', data['extracted'])
        self.assertGreater(len(data['extracted']['biomarkers']), 0)
        self.assertIn('overview', data['summary'])

    def test_04_health_summary_page(self):
        res = self.client.get('/health-summary')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Plain-Language Health Explainer", res.data)

    def test_05_unified_profile_page(self):
        # Login first
        self.client.get('/demo-login/ramesh')
        res = self.client.get('/profile')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Vitals & Physiological Metrics", res.data)
        self.assertIn(b"Active Medications", res.data)

    def test_06_abdm_page_and_card(self):
        res = self.client.get('/abdm')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"AYUSHMAN BHARAT DIGITAL MISSION", res.data)
        self.assertIn(b"ABHA Number", res.data)
        self.assertIn(b"abdm-flip-card", res.data)

    def test_07_abdm_generator_service(self):
        abha_num = ABDMService.generate_abha_number()
        parts = abha_num.split('-')
        self.assertEqual(len(parts), 4)
        self.assertEqual(len(parts[0]), 2)
        self.assertEqual(len(parts[1]), 4)
        self.assertEqual(len(parts[2]), 4)
        self.assertEqual(len(parts[3]), 4)

        abha_addr = ABDMService.generate_abha_address("Gunavardhan Vissa")
        self.assertTrue(abha_addr.endswith("@abdm"))

    def test_08_language_switching(self):
        res = self.client.get('/set-language/hi', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('language'), 'hi')

    def test_09_consent_toggle(self):
        self.client.get('/demo-login/ramesh')
        res = self.client.post('/api/abdm/consent/toggle', data={'consent_id': '1', 'status': 'Revoked'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['new_status'], 'Revoked')

if __name__ == '__main__':
    unittest.main()
