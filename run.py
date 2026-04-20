from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQL
from app.controllers.auth_controller import auth
from app.controllers.song_controller import song
from app.controllers.playlist_controller import playlist

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = "supersecretkey"

# Database Config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shinchan08' 
app.config['MYSQL_DB'] = 'music_library'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' 

mysql = MySQL(app)

# --- REGISTER BLUEPRINTS (This connects your controllers) ---
app.register_blueprint(auth)
app.register_blueprint(song)
app.register_blueprint(playlist)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    search_query = request.args.get('search')
    cur = mysql.connection.cursor()
    
    if search_query:
        query = """
            SELECT s.*, CASE WHEN ls.song_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked
            FROM songs s
            LEFT JOIN liked_songs ls ON s.id = ls.song_id AND ls.user_id = %s
            WHERE s.title LIKE %s OR s.artist LIKE %s
        """
        cur.execute(query, (user_id, f"%{search_query}%", f"%{search_query}%"))
    else:
        query = """
            SELECT s.*, CASE WHEN ls.song_id IS NOT NULL THEN 1 ELSE 0 END AS is_liked
            FROM songs s
            LEFT JOIN liked_songs ls ON s.id = ls.song_id AND ls.user_id = %s
        """
        cur.execute(query, (user_id,))
        
    songs = cur.fetchall()
    cur.execute("SELECT * FROM playlists WHERE user_id = %s", (user_id,))
    playlists = cur.fetchall()
    cur.close()
    
    return render_template('dashboard.html', songs=songs, playlists=playlists, username=session.get('username'), page_title="Your Music Collection")

if __name__ == '__main__':
    app.run(debug=True)