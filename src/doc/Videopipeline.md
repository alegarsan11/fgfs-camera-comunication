# FlightGear Live Camera Streaming (Minimal Full Guide)

## Goal
Stream a live “helicopter/drone-style” camera from FlightGear into VLC and/or a browser using FFmpeg, GStreamer, and MediaMTX.

---

## 1. System Overview

FlightGear does NOT output video directly. It provides a live MJPEG HTTP stream:

```

FlightGear
↓ (MJPEG HTTP frames)
FFmpeg or GStreamer (encoder)
↓ (H.264 video stream)
MediaMTX (server)
↓
VLC / Browser / WebRTC client

````

---

## 2. FlightGear Camera Source

Enable HTTP server:

```bash
fgfs --httpd=8080
````

Camera endpoint:

```
http://localhost:8080/screenshot?stream=1
```

This is MJPEG (image sequence, not video).

---

## 3. Media Server (required)

MediaMTX handles distribution:

```bash
mediamtx
```

Ports used:

* RTSP: 8554
* HLS: 8888
* WebRTC: 8889

---

## 4. FFmpeg Pipeline (simple method)

Convert MJPEG → H.264 → RTSP:

```bash
ffmpeg -f mjpeg -i "http://localhost:8080/screenshot?stream=1" \
-c:v libx264 -preset ultrafast -tune zerolatency \
-f rtsp rtsp://localhost:8554/fgcam
```

---

## 5. View Stream (VLC)

```bash
vlc rtsp://localhost:8554/fgcam
```

---

## 6. GStreamer Pipeline (advanced alternative)

Equivalent pipeline:

```bash
gst-launch-1.0 \
souphttpsrc location=http://localhost:8080/screenshot?stream=1 ! \
multipartdemux ! jpegdec ! \
videoconvert ! x264enc tune=zerolatency speed-preset=ultrafast ! \
rtspclientsink location=rtsp://localhost:8554/fgcam
```

Open:

```
http://localhost/fgcam.m3u8
```

---

## 7. WebRTC (low latency option)

MediaMTX automatically provides WebRTC:

```
http://localhost:8889
```

---

## 8. What is a Signaling Server?

WebRTC requires signaling to exchange connection info:

* IP addresses
* codecs
* session description (SDP)

IMPORTANT:

* It does NOT carry video
* It only helps peers connect

MediaMTX includes signaling internally.

---

## 9. Key Concepts

### Streaming vs Encoding vs Signaling

* Encoding (FFmpeg / GStreamer): converts video formats
* Streaming (MediaMTX): distributes video
* Signaling (WebRTC): negotiates connections

---

## 10. Recommended Setup

### Simple (stable)

```
FlightGear → FFmpeg → MediaMTX → VLC
```

### Advanced (flexible)

```
FlightGear → GStreamer → MediaMTX → WebRTC (browser)
```

---

## 11. Summary

You built a real-time video pipeline:

* Flight simulator camera input
* Live encoding (H.264)
* Streaming server (RTSP/HLS/WebRTC)
* Multi-client viewing (VLC, browser)

No files, no ZIPs — only live video frames.

```
```
