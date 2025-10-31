const logo = document.getElementById('logo');
const turboAudio = document.getElementById('turbo-audio');

clicks = 0;

logo.addEventListener('click', () => {
    clicks += 1;
    if (clicks == 10) {
        turboAudio.play();
        clicks = 0;
    }
});