function getJoke() {
    fetch('/get-joke')
    .then(response => response.json())
    .then(data => {
        document.getElementById('joke').innerText = data.joke;
    })
    .catch(error => console.log(error));
}