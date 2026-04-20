-- ==========================================
-- 1. DATABASE INITIALIZATION
-- ==========================================
CREATE DATABASE IF NOT EXISTS music_library;
USE music_library;

-- We use SET FOREIGN_KEY_CHECKS to allow dropping tables in any order
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS liked_songs;
DROP TABLE IF EXISTS playlist_songs;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- ==========================================
-- 2. CORE TABLES
-- ==========================================

-- USERS: Handles Authentication and Personal Data
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SONGS: Stores music metadata and server file paths
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, 
    title VARCHAR(100) NOT NULL,
    artist VARCHAR(100) DEFAULT 'Unknown Artist',
    album VARCHAR(100) DEFAULT 'Single',
    genre VARCHAR(50),
    file_path VARCHAR(255) NOT NULL,  
    cover_image VARCHAR(255) DEFAULT 'default_cover.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- PLAYLISTS: User-created music collections
CREATE TABLE playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ==========================================
-- 3. JUNCTION TABLES (The Step 1 Update)
-- ==========================================

-- LIKED_SONGS: Connects Many Users to Many Songs (The Heart Button Logic)
CREATE TABLE liked_songs (
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- PLAYLIST_SONGS: Connects Many Songs to Many Playlists
CREATE TABLE playlist_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id INT,
    song_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- ==========================================
-- 4. SEED DATA (Admin & 13 Original Songs)
-- ==========================================

-- Admin User
INSERT INTO users (id, username, email, password) 
VALUES (1, 'Admin', 'admin@harmony.com', 'admin123');

-- 13 Original Rap & Hindi Tracks
INSERT INTO songs (user_id, title, artist, genre, file_path)
VALUES 
(1, 'Tum Hi Ho', 'Arijit Singh', 'Romantic', 'musics/tum_hi_ho.mp3'),
(1, 'Channa Mereya', 'Arijit Singh', 'Sad', 'musics/channa_mereya.mp3'),
(1, 'Kesariya', 'Arijit Singh', 'Romantic', 'musics/kesariya.mp3'),
(1, 'Asal Mein', 'Darshan Raval', 'Indie Pop', 'musics/asal_mein.mp3'),
(1, 'Tera Zikr', 'Darshan Raval', 'Pop', 'musics/tera_zikr.mp3'),
(1, 'Bhula Dunga', 'Darshan Raval', 'Sad Pop', 'musics/bhula_dunga.mp3'),
(1, 'Sheila Ki Jawani', 'Sunidhi Chauhan', 'Dance', 'musics/sheila.mp3'),
(1, 'Kamli', 'Sunidhi Chauhan', 'Dance', 'musics/kamli.mp3'),
(1, 'Ae Watan', 'Sunidhi Chauhan', 'Patriotic', 'musics/ae_watan.mp3'),
(1, 'Desi Girl', 'Sunidhi Chauhan', 'Bollywood', 'musics/desi_girl.mp3'),
(1, 'Roke Na Ruke', 'Zayn', 'Rap', 'musics/roke_na_ruke.mp3'),
(1, 'Red Dot', 'Zayn', 'Rap', 'musics/red_dot.mp3'),
(1, 'Nunchaku', 'Zayn', 'Rap', 'musics/nunchaku.mp3');

-- Default Playlist for Testing
INSERT INTO playlists (user_id, name, description) 
VALUES (1, 'Favorites', 'The best hits from the collection');

-- ==========================================
-- 5. PERFORMANCE OPTIMIZATION (Indexes)
-- ==========================================
CREATE INDEX idx_song_search ON songs(title, artist);
CREATE INDEX idx_user_playlists ON playlists(user_id);