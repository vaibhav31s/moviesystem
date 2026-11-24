from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from . import catalog, tmdb


def _base_context(**extra):
    return {"tmdb_enabled": tmdb.enabled(), "all_genres": catalog.genres(), **extra}


def index(request):
    return render(
        request,
        "index.html",
        _base_context(
            trending=tmdb.enrich(catalog.trending(12)),
            top=tmdb.enrich(catalog.top_rated(12)),
        ),
    )


@require_http_methods(["GET", "POST"])
def recommendations(request):
    query = request.POST.get("name") or request.GET.get("movie") or request.GET.get("name") or ""
    if not query.strip():
        return redirect("Homepage")

    movie = catalog.find(query)
    if movie is None:
        return render(
            request,
            "recommendations.html",
            _base_context(query=query, suggestions=catalog.search(query.split()[0] if query.split() else query)),
            status=404,
        )

    picked, *recs = tmdb.enrich([movie] + catalog.recommend(movie, 8))
    return render(request, "recommendations.html", _base_context(query=query, movie=picked, recs=recs))


def genre(request):
    valid = set(catalog.genres())
    selected = [g for g in (request.GET.getlist("g") or request.POST.getlist("g")) if g in valid]
    results = tmdb.enrich(catalog.by_genres(selected)) if selected else []
    return render(request, "genre.html", _base_context(selected=selected, results=results))


def movieflix(request):
    return redirect("Homepage")


def titles(request):
    q = request.GET.get("q")
    if q is not None:
        return JsonResponse({"results": [{"title": m["title"], "year": m["year"]} for m in catalog.search(q)]})
    return JsonResponse({"titles": catalog.titles()})


def product_details(request, id):
    try:
        movie = catalog.get(int(id))
    except ValueError:
        movie = None
    if movie is None:
        raise Http404("Movie not found")
    data = {k: v for k, v in movie.items() if k != "score"}
    data["similar"] = [{"id": m["id"], "title": m["title"]} for m in catalog.recommend(movie, 12)]
    return JsonResponse(data)
