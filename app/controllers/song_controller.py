import os
from flask import Blueprint, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename

# Blueprint definition
song = Blueprint('song', __name__)

UPLOAD_FOLDER = 'static/musics'

# ---------------- 1. UPLOAD SONG (FIXED) ----------------
@song.route('/upload', methods=['POST'])
def upload_song():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    artist = request.form.get('artist')
    file = request.files.get('file')

    if file and file.filename != '':
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Database logic
        from run import mysql
        cur = mysql.connection.cursor()
        file_path = f"musics/{filename}"
        
        cur.execute("INSERT INTO songs (user_id, title, artist, file_path) VALUES (%s, %s, %s, %s)", 
                    (session['user_id'], title, artist, file_path))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('dashboard'))

# ---------------- 2. TOGGLE LIKE ----------------
@song.route('/like/<int:song_id>', methods=['POST'])
def toggle_like(song_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from run import mysql
    cur = mysql.connection.cursor()
    
    # Check if already liked
    cur.execute("SELECT * FROM liked_songs WHERE user_id = %s AND song_id = %s", (session['user_id'], song_id))
    liked = cur.fetchone()
    
    if liked:
        cur.execute("DELETE FROM liked_songs WHERE user_id = %s AND song_id = %s", (session['user_id'], song_id))
    else:
        cur.execute("INSERT INTO liked_songs (user_id, song_id) VALUES (%s, %s)", (session['user_id'], song_id))
    
    mysql.connection.commit()
    cur.close()
    return redirect(request.referrer or url_for('dashboard'))

# ---------------- 3. VIEW LIKED LIST ----------------
@song.route('/liked-list')
def liked_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    from run import mysql
    cur = mysql.connection.cursor()
    
    # Fetch liked songs
    query = """
        SELECT s.*, 1 AS is_liked FROM songs s
        JOIN liked_songs ls ON s.id = ls.song_id 
        WHERE ls.user_id = %s
    """
    cur.execute(query, (session['user_id'],))
    songs = cur.fetchall()
    
    # Fetch playlists for sidebar consistency
    cur.execute("SELECT * FROM playlists WHERE user_id = %s", (session['user_id'],))
    playlists = cur.fetchall()
    
    cur.close()
    
    return render_template('dashboard.html', 
                           songs=songs, 
                           playlists=playlists, 
                           username=session.get('username'), 
                           page_title="Liked Songs")