"""Build data/movies.json from the Kaggle "TMDB 5000 Movie Dataset".

This is the offline half of the recommender. It reproduces the original
content-based approach (genres + keywords + top 3 cast + director + overview,
bag of words, cosine similarity) and stores only the top matches per movie,
so the web app never needs pandas, scikit-learn or a 200 MB similarity matrix.

Usage:
    pip install -r requirements-dev.txt
    python scripts/build_recommendations.py path/to/tmdb_5000_movies.csv path/to/tmdb_5000_credits.csv
"""
import argparse
import ast
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_N = 12
OUT = Path(__file__).resolve().parent.parent / "data" / "movies.json"


def names(raw, limit=None):
    items = [d["name"] for d in ast.literal_eval(raw)]
    return items[:limit] if limit else items


def director(raw):
    return [d["name"] for d in ast.literal_eval(raw) if d.get("job") == "Director"][:1]


def squash(words):
    # "Sam Worthington" -> "SamWorthington" so multi-word names stay one token
    return [w.replace(" ", "") for w in words]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("movies_csv")
    parser.add_argument("credits_csv")
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()

    movies = pd.read_csv(args.movies_csv)
    credits = pd.read_csv(args.credits_csv).drop(columns=["title"])
    df = movies.merge(credits, left_on="id", right_on="movie_id")
    df = df.dropna(subset=["overview"]).reset_index(drop=True)

    genres = df["genres"].apply(names)
    keywords = df["keywords"].apply(names)
    cast = df["cast"].apply(lambda c: names(c, 3))
    crew = df["crew"].apply(director)

    tags = (
        df["overview"].str.split()
        + genres.apply(squash)
        + keywords.apply(squash)
        + cast.apply(squash)
        + crew.apply(squash)
    ).apply(lambda words: " ".join(words).lower())

    vectors = CountVectorizer(max_features=5000, stop_words="english").fit_transform(tags)
    similarity = cosine_similarity(vectors)

    ids = df["id"].tolist()
    out = []
    for i, row in df.iterrows():
        ranked = similarity[i].argsort()[::-1]
        similar = [int(ids[j]) for j in ranked if j != i][:TOP_N]
        year = str(row["release_date"])[:4] if isinstance(row["release_date"], str) else ""
        out.append(
            {
                "id": int(row["id"]),
                "title": row["title"],
                "year": year,
                "genres": genres[i],
                "rating": round(float(row["vote_average"]), 1),
                "votes": int(row["vote_count"]),
                "popularity": round(float(row["popularity"]), 2),
                "overview": row["overview"],
                "director": crew[i][0] if crew[i] else "",
                "cast": cast[i],
                "similar": similar,
            }
        )

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {len(out)} movies to {args.out}")


if __name__ == "__main__":
    main()
