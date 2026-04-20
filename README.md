# Harmony Music Library System

Harmony is a full-stack web application built with **Flask** and **MySQL** that allows users to manage their personal music collections. Users can register, log in, upload their favorite tracks, create custom playlists, and "like" songs to build a curated library.

---

## 🚀 Features

* **User Authentication:** Secure registration and login system using `bcrypt` for password hashing.
* **Music Library:** A personalized dashboard where users can view and search through their uploaded music collection.
* **Song Uploads:** Upload `.mp3` files with metadata such as title and artist, which are stored securely on the server.
* **Playlists:** Create custom playlists and manage songs within them (Add/Remove).
* **Favorites:** A "Like" system to quickly save and access favorite tracks in a dedicated "Liked Songs" section.
* **In-Browser Player:** An interactive audio player to listen to tracks directly within the application.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** MySQL
* **Authentication:** Bcrypt
* **Frontend:** HTML5, CSS3 (Custom Glassmorphism UI), JavaScript
* **Icons:** Font Awesome

---

## 📁 Project Structure

```text
├── app/
│   ├── controllers/         # Route handling (Auth, Songs, Playlists)
│   ├── models/              # Database helper functions
│   └── config.py            # Database connection setup
├── static/
│   ├── css/                 # Styling files (style.css, auth.css)
│   ├── js/                  # Frontend logic (dashboard.js, songs.js)
│   └── musics/              # Directory for uploaded audio files
├── templates/               # HTML Jinja2 templates
├── mysqldatabase.sql        # Database schema and seed data
├── requirements.txt         # Project dependencies
└── run.py                   # Main application entry point
```


---

## ⚙️ Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.x** and **MySQL Server** installed on your system.

### 2. Database Configuration
1.  Open your MySQL terminal or workbench.
2.  Import the schema and seed data from `mysqldatabase.sql`.
3.  Update the database credentials in `app/config.py` and `run.py` to match your local setup:
    ```python
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="music_library"
    ```
   

### 3. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```


### 4. Run the Application
Start the Flask server by running:
```bash
python run.py
```
The application will be available at `http://127.0.0.1:5000/`.

---

## 🗄️ Database Schema

The system uses five core tables to manage data:
* **users:** Stores credentials and profile info.
* **songs:** Stores metadata and file paths for uploaded music.
* **playlists:** Stores user-created collection names.
* **liked_songs:** A junction table for the "Favorites" feature.
* **playlist_songs:** A junction table linking songs to specific playlists.
