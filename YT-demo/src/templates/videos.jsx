import React, { useState, useEffect } from 'react';

function VideoList() {
  const [videos, setVideos] = useState([]);
  const url = 'http://127.0.0.1:5000';
  useEffect(() => {
    // Make a GET request to your Flask API endpoint for videos
    fetch(`${url}/api/videos`)
      .then((response) => response.json())
      .then((data) => setVideos(data.videos))
      .catch((error) => console.error('Error fetching videos:', error));
  }, []);
  console.log(videos);
  return (
    <div>
      <h1>Video List</h1>
      <ul>
        {videos.map((video) => (
          <li key={video.id}>
            <h3>{video.filename}</h3>
            <video width="320" height="240" controls>
              <source src={`${url}/get_video/${video.id}`} type={video.mime_type} />
              Your browser does not support the video tag.
            </video>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default VideoList;
