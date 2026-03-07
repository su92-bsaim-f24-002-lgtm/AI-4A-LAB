/**
 * Webcam handling – start / stop camera and capture a snapshot.
 */
const Webcam = (() => {
  let stream = null;
  const video = document.getElementById("video");
  const canvas = document.getElementById("snapshot-canvas");

  async function start() {
    if (stream) return;
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "user",
        width: { ideal: 640 },
        height: { ideal: 480 },
      },
    });
    video.srcObject = stream;
  }

  function stop() {
    if (!stream) return;
    stream.getTracks().forEach((t) => t.stop());
    stream = null;
    video.srcObject = null;
  }

  function capture() {
    if (!stream) return null;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);
    return canvas.toDataURL("image/jpeg", 0.9);
  }

  function isActive() {
    return stream !== null;
  }

  return { start, stop, capture, isActive };
})();
