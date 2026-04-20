// Load songs
function loadSongs() {
    fetch('/get_songs')
    .then(res => res.json())
    .then(data => {
        let html = "";

        data.forEach(song => {
            html += `
                <div style="margin:10px; cursor:pointer;"
                     onclick="playSong('${song.file_path}')">
                    🎵 ${song.title} - ${song.artist}
                </div>
            `;
        });

        document.getElementById("songList").innerHTML = html;
    });
}

// Play song
function playSong(filename) {
    const player = document.getElementById("audioPlayer");
    player.src = "/play/" + filename;
    player.play();
}

// Upload song
document.querySelector("form").addEventListener("submit", function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    fetch('/upload_song', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadSongs();
    });
});

// Load songs on page load
window.onload = loadSongs;