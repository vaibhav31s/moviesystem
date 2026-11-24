from unittest import mock

from django.test import SimpleTestCase, override_settings

from . import catalog, tmdb


@mock.patch.dict("os.environ", {"TMDB_API_KEY": ""})
class KeylessSmokeTests(SimpleTestCase):
    """The app must work without a TMDB key (placeholder posters)."""

    def test_home(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Trending")
        self.assertContains(r, "Posters are off")

    def test_recommendations_get_and_post(self):
        r = self.client.get("/recommendations", {"movie": "the dark knight rises"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Batman Begins")
        r = self.client.post("/recommendations", {"name": "Avatar", "movie_name": ""})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "You might also like")

    def test_unknown_movie(self):
        r = self.client.get("/recommendations", {"movie": "zzzz-not-a-movie"})
        self.assertEqual(r.status_code, 404)

    def test_genre(self):
        r = self.client.get("/genre", {"g": ["Action", "Comedy"]})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Action + Comedy")

    def test_titles_api(self):
        r = self.client.get("/api/titles", {"q": "avat"})
        self.assertEqual(r.json()["results"][0]["title"], "Avatar")
        self.assertGreater(len(self.client.get("/product/").json()["titles"]), 4000)

    def test_movieflix_redirects(self):
        self.assertRedirects(self.client.get("/movieflix"), "/", fetch_redirect_response=False)


class TmdbEnrichTests(SimpleTestCase):
    def test_posters_are_fetched_when_key_set(self):
        movie = catalog.find("Avatar")
        fake = {"poster": "https://image.tmdb.org/t/p/w500/x.jpg", "backdrop": None, "imdb_id": "tt0499549"}
        with mock.patch.dict("os.environ", {"TMDB_API_KEY": "k"}), mock.patch.object(tmdb, "_details", return_value=fake):
            [m] = tmdb.enrich([movie])
        self.assertEqual(m["poster"], fake["poster"])
        self.assertEqual(m["link"], "https://www.imdb.com/title/tt0499549/")

    def test_tmdb_errors_fall_back(self):
        movie = catalog.find("Avatar")
        with mock.patch.dict("os.environ", {"TMDB_API_KEY": "k"}), mock.patch.object(tmdb, "_details", side_effect=OSError):
            [m] = tmdb.enrich([movie])
        self.assertIsNone(m["poster"])
