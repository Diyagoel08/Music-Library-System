const audioPlayer = document.getElementById("audioPlayer");
const nowPlaying = document.getElementById("nowPlaying");

// LOAD SONGS
async function loadSongs() {
    const res = await fetch("http://127.0.0.1:5000/songs");
    const songs = await res.json();

    const grid = document.getElementById("songGrid");
    grid.innerHTML = "";

    songs.forEach(song => {
        const card = document.createElement("div");
        card.className = "song-card";

        card.innerHTML = `
            <h4>${song.title}</h4>
            <p>${song.artist}</p>
            <button onclick="playSong('${song.file_path}', '${song.title}')">▶ Play</button>
            <button onclick="deleteSong(${song.id})">❌</button>
        `;

        grid.appendChild(card);
    });
}

// PLAY SONG
function playSong(file, title) {
    audioPlayer.src = `/static/uploads/${file}`;
    audioPlayer.play();
    nowPlaying.innerText = "Now Playing: " + title;
}

// DELETE
async function deleteSong(id) {
    await fetch(`/songs/${id}`, { method: "DELETE" });
    loadSongs();
}

// SEARCH
async function searchSongs() {
    const query = document.getElementById("search").value;

    const res = await fetch(`/songs/search?q=${query}`);
    const songs = await res.json();

    const grid = document.getElementById("songGrid");
    grid.innerHTML = "";

    songs.forEach(song => {
        const card = document.createElement("div");
        card.className = "song-card";

        card.innerHTML = `
            <h4>${song.title}</h4>
            <p>${song.artist}</p>
            <button onclick="playSong('${song.file_path}', '${song.title}')">▶ Play</button>
        `;

        grid.appendChild(card);
    });
}

// ADD SONG
document.getElementById("songForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("title", title.value);
    formData.append("artist", artist.value);
    formData.append("file", file.files[0]);

    await fetch("/songs", {
        method: "POST",
        body: formData
    });

    loadSongs();
});

// AUTO LOAD
window.onload = loadSongs;