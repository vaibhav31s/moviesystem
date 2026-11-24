"""Movie catalog and recommendations, loaded from data/movies.json.

The JSON is produced offline by scripts/build_recommendations.py, so at
runtime this is plain Python: no numpy, pandas or scikit-learn.
"""
import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings

DATA_FILE = Path(settings.BASE_DIR) / "data" / "movies.json"


@lru_cache(maxsize=1)
def _load():
    with open(DATA_FILE, encoding="utf-8") as fh:
        movies = json.load(fh)

    # IMDb-style weighted rating so a 10/10 from 3 votes doesn't top the charts.
    votes = sorted(m["votes"] for m in movies)
    min_votes = votes[int(len(votes) * 0.8)]
    mean = sum(m["rating"] for m in movies) / len(movies)
    for m in movies:
        v, r = m["votes"], m["rating"]
        m["score"] = (v / (v + min_votes)) * r + (min_votes / (v + min_votes)) * mean

    by_id = {m["id"]: m for m in movies}
    by_title = {}
    for m in sorted(movies, key=lambda m: -m["popularity"]):
        by_title.setdefault(m["title"].casefold(), m)
    return movies, by_id, by_title


def all_movies():
    return _load()[0]


def get(movie_id):
    return _load()[1].get(movie_id)


@lru_cache(maxsize=1)
def titles():
    """Titles for search autocomplete, most popular first."""
    return [m["title"] for m in sorted(all_movies(), key=lambda m: -m["popularity"])]


@lru_cache(maxsize=1)
def genres():
    return sorted({g for m in all_movies() for g in m["genres"]})


def find(query):
    """Exact (case-insensitive) title match, else the most popular partial match."""
    q = (query or "").strip().casefold()
    if not q:
        return None
    by_title = _load()[2]
    if q in by_title:
        return by_title[q]
    for m in sorted(all_movies(), key=lambda m: -m["popularity"]):
        if q in m["title"].casefold():
            return m
    return None


def search(query, limit=8):
    q = (query or "").strip().casefold()
    if not q:
        return []
    hits = [m for m in all_movies() if q in m["title"].casefold()]
    hits.sort(key=lambda m: (not m["title"].casefold().startswith(q), -m["popularity"]))
    return hits[:limit]


def recommend(movie, limit=8):
    return [get(i) for i in movie["similar"][:limit] if get(i)]


def top_rated(limit=18):
    return sorted(all_movies(), key=lambda m: -m["score"])[:limit]


def trending(limit=18):
    return sorted(all_movies(), key=lambda m: -m["popularity"])[:limit]


def by_genres(selected, limit=24):
    wanted = set(selected)
    hits = [m for m in all_movies() if wanted.issubset(m["genres"])]
    return sorted(hits, key=lambda m: -m["score"])[:limit]
