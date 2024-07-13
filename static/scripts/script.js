document.addEventListener('DOMContentLoaded', function () {
    const exerciseSelect = document.getElementById('exerciseSelect');
    const exerciseVideo = document.getElementById('exerciseVideo');
    const videoSource = exerciseVideo.querySelector('source');
    const videoFeed = document.getElementById('videoFeed')

    exerciseSelect.addEventListener('change', function () {
        const selectedValue = exerciseSelect.value;
        if (selectedValue === "video_feed") {
            videoSource.setAttribute('src', '../static/videos/push_ups.mp4');
            videoFeed.setAttribute('src', 'video_feed');
            console.log('push up')
        } else if (selectedValue === "video_feed_pull_up") {
            videoSource.setAttribute('src', '../static/videos/pull_ups.mp4');
            videoFeed.setAttribute('src', 'video_feed_pull_up');
            console.log('pull up')
        }
        exerciseVideo.load();
    });
});
