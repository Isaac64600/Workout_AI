document.addEventListener('DOMContentLoaded', function () {
    const exerciseSelect = document.getElementById('exerciseSelect');
    const exerciseVideo = document.getElementById('exerciseVideo');
    const videoSource = exerciseVideo.querySelector('source');

    exerciseSelect.addEventListener('change', function () {
        const selectedVideo = exerciseSelect.value;
        videoSource.setAttribute('src', selectedVideo);
        exerciseVideo.load();
    });
});
