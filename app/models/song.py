def get_liked_songs(mysql, user_id):
    cur = mysql.connection.cursor()
    query = """
        SELECT s.*, 1 as is_liked 
        FROM songs s
        JOIN liked_songs ls ON s.id = ls.song_id
        WHERE ls.user_id = %s
    """
    cur.execute(query, (user_id,))
    songs = cur.fetchall()
    cur.close()
    return songs