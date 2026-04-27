# FlightGear Live Camera + Web Control System (Working Setup)

## Status
✔ Working system  
✔ FlightGear streaming video  
✔ Web browser control of camera  
✔ Node.js bridge translating commands  
✔ Media server running (MediaMTX)

---

# 1. System Overview

We built a full real-time control + streaming pipeline:


```
            ┌────────────────────┐
            │   HTML Interface   │
            │ (buttons / JS UI)  │
            └─────────┬──────────┘
                      │ WebSocket (:9090)
                      ↓
            ┌────────────────────┐
            │   Node.js Bridge   │
            │  (command parser)  │
            └─────────┬──────────┘
                      │ Telnet / setprop
                      ↓
            ┌────────────────────┐
            │   FlightGear       │
            │ camera system      │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │ MediaMTX Server    │
            │ RTSP / HLS / WS    │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │ VLC / Browser      │
            └────────────────────┘
```


---

# 2. Components Used

## FlightGear
Simulator providing camera system via property tree:

Key properties:
```

/sim/current-view/heading-offset-deg
/sim/current-view/pitch-offset-deg
/sim/current-view/roll-offset-deg

````

Start with:
```bash
fgfs --telnet=5400
````

---

## MediaMTX (Streaming Server)

Handles video streaming (RTSP/WebRTC/HLS):

```bash
mediamtx
```

Ports:

* RTSP: 8554
* HLS: 8888
* WebRTC: 8889

---

## Node.js Bridge (Control System)

Bridges WebSocket → FlightGear.

---

# 3. Bridge Code (FINAL WORKING VERSION)

```javascript id="bridge_final"
const WebSocket = require("ws");
const net = require("net");

const wss = new WebSocket.Server({ port: 9090 });

const FG_HOST = "127.0.0.1";
const FG_PORT = 5400;

function setProp(path, value) {
  const client = new net.Socket();

  client.connect(FG_PORT, FG_HOST, () => {
    const cmd = `set ${path} ${value}`;
    client.write(cmd + "\r\n");
    client.end();
  });
}

wss.on("connection", (ws) => {
  console.log("Client connected");

  ws.on("message", (msg) => {
    const data = JSON.parse(msg);

    const heading = data.heading ?? 0;
    const pitch = data.pitch ?? 0;

    setProp("/sim/current-view/heading-offset-deg", heading);
    setProp("/sim/current-view/pitch-offset-deg", pitch);
  });
});

console.log("Bridge running on ws://localhost:9090");
```

---

# 4. HTML Control Interface

```html id="html_final"
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>FlightGear Camera Control</title>
<style>
body { font-family: sans-serif; text-align: center; margin-top: 50px; }
button { font-size: 18px; margin: 5px; padding: 10px; }
</style>
</head>
<body>

<h2>FlightGear Camera Control</h2>

<button onmousedown="start('left')" onmouseup="stop()">⬅ Left</button>
<button onmousedown="start('right')" onmouseup="stop()">➡ Right</button><br>

<button onmousedown="start('up')" onmouseup="stop()">⬆ Up</button>
<button onmousedown="start('down')" onmouseup="stop()">⬇ Down</button><br>

<button onclick="reset()">Reset</button>

<script>
const ws = new WebSocket("ws://localhost:9090");

let interval;

let state = {
  heading: 0,
  pitch: 0
};

const STEP = 0.5;

function send() {
  ws.send(JSON.stringify(state));
}

function start(dir) {
  stop();

  interval = setInterval(() => {
    if (dir === "left") state.heading -= STEP;
    if (dir === "right") state.heading += STEP;
    if (dir === "up") state.pitch -= STEP;
    if (dir === "down") state.pitch += STEP;

    send();
  }, 30);
}

function stop() {
  if (interval) clearInterval(interval);
}

function reset() {
  state.heading = 0;
  state.pitch = 0;
  send();
}
</script>

</body>
</html>
```

---

# 5. Key Properties Used (IMPORTANT)

These are the ONLY camera-related properties used:

```
/sim/current-view/heading-offset-deg
/sim/current-view/pitch-offset-deg
/sim/current-view/roll-offset-deg
```

---

# 6. Why It Now Works

### Before:

* HTML sent commands ❌
* No bridge ❌
* FlightGear not receiving anything ❌

### Now:

* HTML sends WebSocket data ✔
* Node bridge translates commands ✔
* FlightGear receives property updates ✔
* Camera responds ✔

---

# 7. Important Notes

## ✔ Camera only moves if:

* Active view supports offsets
* No external script overwrites values

## ❌ Camera will NOT move if:

* cockpit view locks orientation
* FGCamera or aircraft scripts override view
* wrong property is used

---

# 8. What You Built

You now have a system equivalent to:

* Drone FPV controller
* Remote camera rig
* Real-time simulator camera steering

---

# 9. Next Possible Upgrades

If you want to improve this system:

### 🚀 1. Smooth inertia camera (physics-based)

### 🎮 2. Mouse drag FPV camera

### 🎥 3. Sync camera + RTSP video latency

### 🌐 4. Single-page control dashboard (video + control)

### 🚁 5. Helicopter chase camera mode

---

# END

Working FlightGear remote camera system achieved.

