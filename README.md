# MovieFlex

**Live:** https://movies.vaibhavgawad.com

Movie recommendations by Vaibhav Gawad, first built for Microsoft Engage 2022.

Pick a movie you liked and MovieFlex suggests eight similar films. It uses
**content-based filtering**: each movie becomes a bag of words from its plot,
genres, keywords, top three cast members and director, and movies are compared
with **cosine similarity**. You can also browse by one or more genres.

**Video demo:** https://youtu.be/6_EAMuwWctk ·
**Algorithm walkthrough:** [spreadsheet](https://docs.google.com/spreadsheets/d/11AUtJWwsBh0lnXZyvuM5OW5qvQ5yovA1sd0_srtkAms/edit?usp=sharing)

## How it works

- `scripts/build_recommendations.py` runs **offline** with pandas and scikit-learn
  over the Kaggle [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
  It saves `data/movies.json` (about 3 MB): every movie's details plus the IDs of its
  12 most similar movies.
- The Django app (`trial/`) only reads that JSON, so the web app needs no numpy,
  pandas or scikit-learn and no database. It stays small enough for serverless hosting.
- Posters and IMDb links come from the TMDB API when `TMDB_API_KEY` is set. Without a
  key, everything still works and the app shows placeholder posters.

## Tech stack

Python 3.12 · Django 6 · WhiteNoise · scikit-learn and pandas (data build only) ·
plain HTML, CSS and JS

## Run locally

```sh
git clone https://github.com/vaibhav31s/moviesystem
cd moviesystem
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export DJANGO_DEBUG=true            # local only; in production set DJANGO_SECRET_KEY instead
export TMDB_API_KEY=your-key        # optional, for posters
python manage.py runserver
```

Then open http://127.0.0.1:8000/. Run the tests with `python manage.py test`.

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | yes (production) | Django secret key. Generate one with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `DJANGO_DEBUG` | no | `true` for local development only (default `false`) |
| `TMDB_API_KEY` | no | TMDB v3 API key or v4 read access token, for posters and IMDb links |
| `DJANGO_ALLOWED_HOSTS` | no | Extra hostnames, comma separated, e.g. a custom domain (`*.vercel.app` is always allowed) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | no | Extra origins for a custom domain, e.g. `https://movies.example.com` |

## Rebuild the recommendation data

1. Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle.
2. Run:

```sh
pip install -r requirements-dev.txt
python scripts/build_recommendations.py path/to/tmdb_5000_movies.csv path/to/tmdb_5000_credits.csv
```

## Deploy to Vercel

The repo is ready for Vercel's Python runtime. Django is detected from `manage.py`,
`pyproject.toml` points Vercel at `moviesystem.wsgi:application`, and WhiteNoise serves
`static/` from the function, so no build step is needed.

1. Import the GitHub repo in Vercel, or run `vercel` from the project folder.
2. Add the environment variables `DJANGO_SECRET_KEY` (required) and `TMDB_API_KEY`
   (optional, for posters).
3. Deploy.

## Routes

| Path | What it shows |
|---|---|
| `/` | Search, trending and all-time top rated |
| `/recommendations?movie=<title>` | The chosen movie and 8 recommendations (the form also accepts POST `name`) |
| `/genre?g=Action&g=Comedy` | Movies matching every selected genre |
| `/api/titles` and `/api/titles?q=<text>` | All titles, or title search (JSON) |
| `/product/<tmdb id>` | One movie and its similar movies (JSON) |
