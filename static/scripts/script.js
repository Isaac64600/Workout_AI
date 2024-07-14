document.addEventListener('DOMContentLoaded', function () {
    const exerciseSelect = document.getElementById('exerciseSelect');
    const exerciseVideo = document.getElementById('exerciseVideo');
    const videoSource = document.getElementById('videoSource');
    const videoFeed = document.getElementById('videoFeed');

    if (!exerciseSelect || !exerciseVideo || !videoSource || !videoFeed) {
        console.error('One or more elements were not found.');
        return;
    }

    exerciseSelect.addEventListener('change', function () {
        const selectedValue = exerciseSelect.value;
        console.log('Selected value:', selectedValue);

        videoSource.setAttribute('src', selectedValue);
        exerciseVideo.load();

        if (selectedValue === "../static/videos/push_ups.mp4") {
            videoFeed.setAttribute('src', 'video_feed');
        } else if (selectedValue === "../static/videos/pull_ups.mp4") {
            videoFeed.setAttribute('src', 'video_feed_pull_up');
        } else if (selectedValue === "../static/videos/squat.mp4") {
            videoFeed.setAttribute('src', 'video_feed_squat');
        }

        console.log('Updated video source:', videoSource.getAttribute('src'));
        console.log('Updated video feed source:', videoFeed.getAttribute('src'));
    });
});
