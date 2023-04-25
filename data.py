import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
# Initialize Spotify API client with client_id parameter
scope = "user-top-read user-library-read user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id='b15266cc8a7d494db418f65e6f698ffe', client_secret='f256f78f0c16400089ab4ab25ab48f48', redirect_uri='http://localhost:8888/callback'))

# Initialize previous top tracks list
prev_top_tracks = []

def update_trends(top_tracks):
    global prev_top_tracks
    global trends
    
    # If there is no previous top tracks list, initialize trends to all zeros
    if not prev_top_tracks:
        trends = [0] * len(top_tracks)
    else:
        trends = []
        for i, track in enumerate(top_tracks):
            if track in prev_top_tracks:
                prev_index = prev_top_tracks.index(track)
                diff = prev_index - i
                if diff == 0:
                    trends.append(0)
                elif diff < 0:
                    trends.append(1)
                else:
                    trends.append(-1)
            else:
                trends.append(0)
    
    # Update previous top tracks list
    prev_top_tracks = top_tracks.copy()
    
    return trends

# Retrieve user's top 10 tracks
results = sp.current_user_top_tracks(limit=10, time_range='short_term')
top_tracks = [track['name'] for track in results['items']]

# Initialize trends
trends = update_trends(top_tracks)

# Display results in console
print("Your top 10 tracks are:")
for i, track_name in enumerate(top_tracks):
    print(f"{i+1}. {track_name}")

from datetime import datetime, timedelta

# Set time window to past 24 hours
now = datetime.now()
yesterday = now - timedelta(days=1)

# Get the user's recently played tracks
results = sp.current_user_recently_played(limit=50)

# Get the timestamp of the last played track
last_played_at = results['items'][-1]['played_at']

# Convert the timestamp to milliseconds and add 1
after = int(round(pd.Timestamp(last_played_at).timestamp() * 1000)) + 1

# Use the after parameter in the next request
results = sp.current_user_recently_played(limit=50, after=after)

recent_tracks = [track['track']['name'] for track in results['items']]

# Assign trend values based on play count
trend_values = []
for track in top_tracks:
    count = recent_tracks.count(track)
    trend_values.append(count)
# Normalize trend values to range -1 to 1
min_val = min(trend_values)
max_val = max(trend_values)
if max_val == min_val:
    normalized = [0] * len(trend_values)
else:
    normalized = [((val - min_val) / (max_val - min_val) * 2) - 1 for val in trend_values]

# Map values to uptrend or downtrend
trends = []
for val in normalized:
    if val >= 0:
        trends.append('Uptrend')
    else:
        trends.append('Downtrend')