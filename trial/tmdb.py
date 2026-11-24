"""Optional poster/IMDb lookups from TMDB.

Everything works without a key: callers get None and fall back to
placeholder posters. Accepts either a v3 API key or a v4 read access token.
"""
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

import requests

log = logging.getLogger(__name__)

API = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TIMEOUT = 4

_session = requests.Session()


def api_key():
    return os.environ.get("TMDB_API_KEY", "").strip()


def enabled():
    return bool(api_key())


def _get(path):
    key = api_key()
    params, headers = {"language": "en-US"}, {"accept": "application/json"}
    if key.startswith("eyJ"):  # v4 read access token (a JWT)
        headers["Authorization"] = f"Bearer {key}"
    else:
        params["api_key"] = key
    resp = _session.get(f"{API}{path}", params=params, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


@lru_cache(maxsize=4096)
def _details(movie_id):
    data = _get(f"/movie/{movie_id}")
    poster = data.get("poster_path")
    backdrop = data.get("backdrop_path")
    return {
        "poster": f"{IMAGE_BASE}{poster}" if poster else None,
        "backdrop": f"https://image.tmdb.org/t/p/w1280{backdrop}" if backdrop else None,
        "imdb_id": data.get("imdb_id") or None,
    }


def details(movie_id):
    if not enabled():
        return None
    try:
        return _details(movie_id)
    except Exception as exc:  # network error, bad key, rate limit...
        log.warning("TMDB lookup failed for %s: %s", movie_id, exc)
        return None


def enrich(movies):
    """Return copies of `movies` with poster/backdrop/imdb_id filled in (concurrently)."""
    movies = [dict(m) for m in movies]
    if enabled() and movies:
        with ThreadPoolExecutor(max_workers=min(12, len(movies))) as pool:
            for movie, extra in zip(movies, pool.map(details, [m["id"] for m in movies])):
                movie.update(extra or {})
    for m in movies:
        m.setdefault("poster", None)
        m.setdefault("backdrop", None)
        m.setdefault("imdb_id", None)
        m["hue"] = (m["id"] * 47) % 360  # colour for the placeholder poster
        m["link"] = (
            f"https://www.imdb.com/title/{m['imdb_id']}/"
            if m["imdb_id"]
            else f"https://www.themoviedb.org/movie/{m['id']}"
        )
    return movies
