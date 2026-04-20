from flask import Blueprint, request, render_template, redirect, url_for, session, flash
import os

# Create the blueprint
playlist = Blueprint('playlist', __name__)

# ---------------- 1. CREATE PLAYLIST ----------------
@playlist.route('/create_playlist', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    name = request.form.get('playlist_name')
    user_id = session['user_id']

    if not name:
        return redirect(url_for('dashboard'))

    try:
        from run import mysql
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO playlists (user_id, name) VALUES (%s, %s)", (user_id, name))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error creating playlist: {e}")

    return redirect(url_for('dashboard'))

# ---------------- 2. VIEW PLAYLIST SONGS ----------------
@playlist.route('/playlist/<int:playlist_id>')
def view(playlist_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    from run import mysql
    cur = mysql.connection.cursor()

    # 1. Fetch Playlist Metadata
    cur.execute("SELECT name FROM playlists WHERE id = %s AND user_id = %s", (playlist_id, user_id))
    playlist_info = cur.fetchone()
    
    if not playlist_info:
        return redirect(url_for('dashboard'))

    # 2. Fetch Songs in this Playlist (Using the JOIN from your Step 5)
    query = """
        SELECT s.*, 
        CASE WHEN ls.song_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked
        FROM songs s
        JOIN playlist_songs ps ON s.id = ps.song_id
        LEFT JOIN liked_songs ls ON s.id = ls.song_id AND ls.user_id = %s
        WHERE ps.playlist_id = %s
    """
    cur.execute(query, (user_id, playlist_id))
    songs = cur.fetchall()

    # 3. Fetch all playlists for the sidebar
    cur.execute("SELECT * FROM playlists WHERE user_id = %s", (user_id,))
    all_playlists = cur.fetchall()

    cur.close()
    
    # We reuse dashboard.html but change the heading
    return render_template('dashboard.html', 
                           songs=songs, 
                           playlists=all_playlists, 
                           username=session.get('username'), 
                           page_title=f"Playlist: {playlist_info['name']}")

# ---------------- 3. ADD SONG TO PLAYLIST ----------------
@playlist.route('/add_to_playlist', methods=['POST'])
def add_song():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    playlist_id = request.form.get('playlist_id')
    song_id = request.form.get('song_id')

    try:
        from run import mysql
        cur = mysql.connection.cursor()
        
        # Check if song already exists in playlist to avoid duplicates
        cur.execute("SELECT * FROM playlist_songs WHERE playlist_id=%s AND song_id=%s", (playlist_id, song_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)", (playlist_id, song_id))
            mysql.connection.commit()
        
        cur.close()
    except Exception as e:
        print(f"Error adding song: {e}")

    return redirect(request.referrer or url_for('dashboard'))

# ---------------- 4. REMOVE SONG FROM PLAYLIST ----------------
@playlist.route('/remove_song/<int:playlist_id>/<int:song_id>', methods=['POST'])
def remove_song(playlist_id, song_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        from run import mysql
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM playlist_songs WHERE playlist_id=%s AND song_id=%s", (playlist_id, song_id))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error removing song: {e}")

    return redirect(request.referrer or url_for('dashboard'))