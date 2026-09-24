import unittest
from app import app

class NoongarAppTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Main functionality
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_seasons_returns_six(self):
        response = self.client.get('/api/seasons')
        data = response.get_json()
        self.assertEqual(len(data), 6)

    def test_get_signs_returns_data(self):
        response = self.client.get('/api/signs')
        data = response.get_json()
        self.assertGreater(len(data), 0)

    # Algorithmic core (season-stats)
    def test_season_stats_returns_six_seasons(self):
        response = self.client.get('/api/season-stats')
        data = response.get_json()
        self.assertEqual(len(data), 6)

    def test_season_stats_has_expected_fields(self):
        response = self.client.get('/api/season-stats')
        data = response.get_json()
        birak = data['Birak']
        self.assertIn('avg_max_temp', birak)
        self.assertIn('avg_min_temp', birak)
        self.assertIn('total_rainfall', birak)

    # Filtering
    def test_signs_filtered_by_season(self):
        response = self.client.get('/api/signs?season=Birak')
        data = response.get_json()
        for sign in data:
            self.assertEqual(sign['season_name'], 'Birak')

    def test_signs_search_finds_matches(self):
        response = self.client.get('/api/signs?q=kangaroo')
        data = response.get_json()
        self.assertGreater(len(data), 0)

    # Invalid input / edge cases
    def test_signs_filtered_by_invalid_season(self):
        response = self.client.get('/api/signs?season=NotARealSeason')
        data = response.get_json()
        self.assertEqual(len(data), 0)

    def test_signs_search_no_matches(self):
        response = self.client.get('/api/signs?q=zzzznotreal')
        data = response.get_json()
        self.assertEqual(len(data), 0)

    def test_season_page_handles_invalid_season(self):
        response = self.client.get('/season/NotARealSeason')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
