from django.shortcuts import render
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from django.contrib.auth.decorators import login_required
import spotipy
# Create your views here.


@login_required
def index(request):
    cache_handler = spotipy.DjangoSessionCacheHandler(request=request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_handler=cache_handler)
    session = spotipy.Spotify(
        oauth_manager=auth_manager, requests_session=True)

    recent = session.current_user_recently_played(limit=5)
    recent_artists = [artist['uri'] for song in recent["items"]
                      for artist in song["track"]["artists"]]

    recs = session.recommendations(
        seed_artists=recent_artists[:5], limit=8)
    return render(request, 'stats/index.html', {
        "recs": recs
    })


@login_required
def recents(request):
    cache_handler = spotipy.DjangoSessionCacheHandler(request=request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_handler=cache_handler)
    session = spotipy.Spotify(
        oauth_manager=auth_manager, requests_session=True)

    recents = session.current_user_recently_played(limit=8)
    recents = recents["items"]
    return render(request, 'stats/recents.html', {
        "recents": recents
    })


@login_required
def fav_artists(request):
    cache_handler = spotipy.DjangoSessionCacheHandler(request=request)
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_handler=cache_handler)
    session = spotipy.Spotify(
        oauth_manager=auth_manager, requests_session=True)

    artists = session.current_user_top_artists()

    artist_ids = [artist["id"] for artist in artists["items"]]

    favorite_artists = [session.artist(artist_id)
                        for artist_id in artist_ids[:4]]
    return render(request, "stats/fav_artists.html", {
        "favorite_artists": favorite_artists
    })
