from flask import Flask, render_template
from data import *

app = Flask(__name__)
# Define a route to display the top 10 tracks trends
@app.route('/')
def top_tracks_trends():
    # Get the top tracks and their trends
    global top_tracks
    global trends
    results = sp.current_user_top_tracks(limit=10, time_range='short_term')
    new_top_tracks = [track['name'] for track in results['items']]
    
    new_trends = []
    for track in new_top_tracks:
        if track in top_tracks:
            # Track has not moved in the list
            index = top_tracks.index(track)
            new_trends.append(trends[index])
        else:
            # New track has been added to the list
            new_trends.append('New Entry')
    
    for track in top_tracks:
        if track not in new_top_tracks:
            # Track has been removed from the list
            index = top_tracks.index(track)
            new_trends[index] = 'Dropped out'
    
    top_tracks = new_top_tracks
    trends = new_trends
    
    # Combine the data into a list of dictionaries
    updated_tracks = []
    for i in range(len(top_tracks)):
        track = {"rank": i+1, "name": top_tracks[i], "trend": trends[i]}
        updated_tracks.append(track)
    
    # Render the HTML template with the track data
    return render_template('index.html', tracks=updated_tracks)
    
if __name__ == '__main__':
    app.run(debug=True)



# # Define a route to display the top 10 tracks trends
# @app.route('/')
# def top_tracks_trends():
#     # Get the top tracks and their trends
#     top_tracks_list = top_tracks
    
    
#     # Combine the data into a list of dictionaries
#     updated_tracks = []
#     for i in range(len(top_tracks_list)):
#         track = {"rank": i+1, "name": top_tracks_list[i], "trend": trends[i]}
#         updated_tracks.append(track)
    
#     # Render the HTML template with the track data
#     return render_template('index.html', tracks=updated_tracks)

# if __name__ == '__main__':
#     app.run(debug=True)

