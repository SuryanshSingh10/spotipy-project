import spotipy
import random
from spotipy.oauth2 import SpotifyOAuth

# Define your client_id, client_secret, and redirect_uri
auth_manager = SpotifyOAuth(client_id='dc3477c7112f4c47a1334441387e2624',
                            client_secret='8dfb42cccbfb467e9dc1650872a540b4',
                            redirect_uri='https://open.spotify.com/?',
                            scope=['user-library-read', 'user-top-read', 'app-remote-control'])

sp = spotipy.Spotify(auth_manager=auth_manager)

def recommend_songs(mood):
    # Get the user's top tracks
    top_tracks = sp.current_user_top_tracks(time_range='medium_term', limit=50)

    # Get the audio features of the top tracks
    top_tracks_features = sp.audio_features(tracks=[track['id'] for track in top_tracks['items']])

    # Filter the top tracks based on the mood
    filtered_tracks = []
    for track in top_tracks_features:
        if track['valence'] > 0.5 and mood == 'happy':
            filtered_tracks.append(track)
        elif track['valence'] < 0.5 and mood == 'sad':
            filtered_tracks.append(track)
        elif track['energy'] < 0.5 and mood == 'relaxed':
            filtered_tracks.append(track)
        elif track['energy'] > 0.5 and mood == 'energized':
            filtered_tracks.append(track)

    # Choose a random song from the filtered dataset
    recommended_song = filtered_tracks[random.randint(0,len(filtered_tracks)-1)]

    # Get the song's album cover
    album_cover = sp.album(recommended_song['album']['id'])['images'][0]['url']

    # Print the song details
    print(f'Recommended Song: {recommended_song["name"]} by {recommended_song["artists"][0]["name"]}')
    print(f'Album: {recommended_song["album"]["name"]}')
    print(f'Album cover: {album_cover}')
    print(f'Preview URL: {recommended_song["preview_url"]}')
    
    # Play the recommended song
    sp.start_playback(uris=[recommended_song['uri']])

# Get the user's mood input
mood = input("What is your current mood? (happy, sad, relaxed, energized) ")

# Call the recommend_songs function
recommend_songs(mood)

