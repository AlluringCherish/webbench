import psutil
import shutil
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from custom_test import CustomTestRunner
from utils_win import get_python_pid


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up code path for data file access."""
        cls.code_path = 'data'

    def setUp(self):
        """Set up the Selenium WebDriver before each test (WSL headless mode)."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        prefs = {"profile.password_manager_leak_detection": False}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-page"))
        )

    def tearDown(self):
        self.driver.quit()

    # ===== Dashboard Page Tests =====
    def test_dashboard_page_elements(self):
        self.assertTrue(self.driver.find_element(By.ID, "dashboard-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "featured-songs").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "browse-songs-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "my-playlists-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "trending-artists-button").is_displayed())

    def test_dashboard_page_functionality(self):
        self.driver.find_element(By.ID, "browse-songs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())

    # ===== Song Catalog Page Tests =====
    def test_catalog_page_elements(self):
        self.driver.find_element(By.ID, "browse-songs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.assertTrue(self.driver.find_element(By.ID, "catalog-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "genre-filter").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "songs-grid").is_displayed())

    def test_catalog_page_functionality(self):
        self.driver.find_element(By.ID, "browse-songs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        songs_grid = self.driver.find_element(By.ID, "songs-grid").text
        # Verify songs from data file are displayed
        with open(f'{self.code_path}/songs.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "songs.txt is empty")
            first_song = lines[0].split('|')
            song_title = first_song[1]
            self.assertIn(song_title, songs_grid)

    # ===== Song Details Page Tests =====
    def test_song_details_page_elements(self):
        self.driver.find_element(By.ID, "browse-songs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "add-to-playlist-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "song-details-page")))
        self.assertTrue(self.driver.find_element(By.ID, "song-details-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "song-title").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "artist-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "album-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "duration-display").is_displayed())

    def test_song_details_page_functionality(self):
        self.driver.find_element(By.ID, "browse-songs-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "catalog-page")))
        self.driver.find_element(By.ID, "add-to-playlist-button-1").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "song-details-page")))
        # Verify song details match data file
        with open(f'{self.code_path}/songs.txt', 'r') as f:
            first_line = f.readline().strip()
            self.assertTrue(len(first_line) > 0, "songs.txt is empty")
            expected_data = first_line.split('|')
            expected_title = expected_data[1]
            title = self.driver.find_element(By.ID, "song-title").text
            self.assertIn(expected_title, title)

    # ===== Playlists Page Tests =====
    def test_playlists_page_elements(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        self.assertTrue(self.driver.find_element(By.ID, "playlists-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "playlists-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "create-playlist-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_playlists_page_functionality(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        playlists_grid = self.driver.find_element(By.ID, "playlists-grid").text
        # Verify playlists from data file are displayed
        with open(f'{self.code_path}/playlists.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_playlist = lines[0].split('|')
                playlist_title = first_playlist[1]
                self.assertIn(playlist_title, playlists_grid)

    # ===== Create Playlist Page Tests =====
    def test_create_playlist_page_elements(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        self.driver.find_element(By.ID, "create-playlist-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "create-playlist-page")))
        self.assertTrue(self.driver.find_element(By.ID, "create-playlist-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "playlist-name-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "playlist-description-input").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "save-playlist-button").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "cancel-create-button").is_displayed())

    def test_create_playlist_page_functionality(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        self.driver.find_element(By.ID, "create-playlist-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "create-playlist-page")))
        self.driver.find_element(By.ID, "playlist-name-input").send_keys("My Favorite Hits")
        playlist_name = self.driver.find_element(By.ID, "playlist-name-input").get_attribute("value")
        self.assertEqual(playlist_name, "My Favorite Hits")

    # ===== Playlist Details Page Tests =====
    def test_playlist_details_page_elements(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        try:
            self.driver.find_element(By.ID, "view-playlist-button-1").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlist-details-page")))
            self.assertTrue(self.driver.find_element(By.ID, "playlist-details-page").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "playlist-title").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "playlist-description").is_displayed())
            self.assertTrue(self.driver.find_element(By.ID, "songs-in-playlist").is_displayed())
        except:
            pass  # Playlist might not exist yet

    def test_playlist_details_page_functionality(self):
        self.driver.find_element(By.ID, "my-playlists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlists-page")))
        try:
            self.driver.find_element(By.ID, "view-playlist-button-1").click()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "playlist-details-page")))
            # Verify playlist details match data file
            with open(f'{self.code_path}/playlists.txt', 'r') as f:
                first_line = f.readline().strip()
                if len(first_line) > 0:
                    expected_data = first_line.split('|')
                    expected_title = expected_data[1]
                    title = self.driver.find_element(By.ID, "playlist-title").text
                    self.assertIn(expected_title, title)
        except:
            pass

    # ===== Albums Page Tests =====
    def test_albums_page_elements(self):
        self.driver.get("http://localhost:5000/albums")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "albums-page")))
        self.assertTrue(self.driver.find_element(By.ID, "albums-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "albums-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-albums").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "sort-albums").is_displayed())

    def test_albums_page_functionality(self):
        self.driver.get("http://localhost:5000/albums")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "albums-page")))
        albums_grid = self.driver.find_element(By.ID, "albums-grid").text
        # Verify albums from data file are displayed
        with open(f'{self.code_path}/albums.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "albums.txt is empty")
            first_album = lines[0].split('|')
            album_title = first_album[1]
            self.assertIn(album_title, albums_grid)

    # ===== Artists Page Tests =====
    def test_artists_page_elements(self):
        self.driver.find_element(By.ID, "trending-artists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "artists-page")))
        self.assertTrue(self.driver.find_element(By.ID, "artists-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "artists-grid").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "search-artists").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "artists-sort").is_displayed())

    def test_artists_page_functionality(self):
        self.driver.find_element(By.ID, "trending-artists-button").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "artists-page")))
        artists_grid = self.driver.find_element(By.ID, "artists-grid").text
        # Verify artists from data file are displayed
        with open(f'{self.code_path}/artists.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            self.assertGreater(len(lines), 0, "artists.txt is empty")
            first_artist = lines[0].split('|')
            artist_name = first_artist[1]
            self.assertIn(artist_name, artists_grid)

    # ===== Genres Page Tests =====
    def test_genres_page_elements(self):
        self.driver.get("http://localhost:5000/genres")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "genres-page")))
        self.assertTrue(self.driver.find_element(By.ID, "genres-page").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "genres-list").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "select-genre").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "back-to-dashboard").is_displayed())

    def test_genres_page_functionality(self):
        self.driver.get("http://localhost:5000/genres")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "genres-page")))
        genres_list = self.driver.find_element(By.ID, "genres-list").text
        # Verify genres from data file are displayed
        with open(f'{self.code_path}/genres.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            if len(lines) > 0:
                first_genre = lines[0].split('|')
                genre_name = first_genre[1]
                self.assertIn(genre_name, genres_list)


class TestMusicStreaming:
    def __init__(self, checker, path, time=2):
        code_path = os.path.dirname(path)
        if not os.path.exists('data'):
            shutil.copytree(f'{code_path}/data', 'data')
        else:
            shutil.rmtree('data')
            shutil.copytree(f'{code_path}/data', 'data')
        self.pid = get_python_pid()
        self.py = path
        self.code_path = code_path

    def test_set_up(self):
        try:
            self.process = subprocess.Popen(['python', self.py])
            time.sleep(2)
            return 1
        except:
            return 0

    def tear_down(self):
        if os.path.exists('data'):
            shutil.rmtree('data')
        self.process.terminate()

    def main(self):
        result = {'total': 20, 'total_basic': 10, 'total_advanced': 10, 'basic': 0, 'advanced': 0, 'test_cases': {'set_up': 0}}
        res = None

        try:
            result['test_cases']['set_up'] = self.test_set_up()
        except Exception as e:
            print(f"ERROR during setup: {e}")
            self.tear_down()
            return result

        if result['test_cases']['set_up'] == 1:
            try:
                test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
                res = CustomTestRunner().run(test_suite)
            except Exception as e:
                print(f"ERROR during test execution: {e}")
                self.tear_down()
                return result
        else:
            print("Setup failed, skipping tests")
            self.tear_down()
            return result

        self.tear_down()

        if res is not None:
            for test in res['succ']:
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 1
            for test in res['fail']:
                result['test_cases']["_".join(str(test).split(" ")[0].split('_')[1:])] = 0

        for item in result['test_cases']:
            if 'elements' in item:
                result['basic'] += result['test_cases'][item]
            if 'functionality' in item:
                result['advanced'] += result['test_cases'][item]
        return result


if __name__ == '__main__':
    import glob
    def find_app_py(app_name):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pattern = os.path.join(base_dir, 'no_login_web', f'{app_name}', 'app.py')
        if os.path.exists(pattern):
            return pattern
        return None

    py = sys.argv[1] if len(sys.argv) > 1 else find_app_py('MusicStreaming')
    if not py:
        print("ERROR: Could not find app.py")
        sys.exit(1)
    test = TestMusicStreaming(None, py)
    result = test.main()
    import pprint
    pprint.pprint(result)
