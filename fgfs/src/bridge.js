const WebSocket = require("ws");
const net = require("net");

const wss = new WebSocket.Server({ port: 9090 });

const fg = new net.Socket();

fg.connect(5400, "127.0.0.1", () => {
  console.log("Connected to FlightGear");
});

let target = { heading: 0, pitch: 0 };
let state  = { heading: 0, pitch: 0 };

function setProp(path, value) {
  fg.write(`set ${path} ${value}\r\n`);
}

// Revice la comunicacion del HTML con orden de movimiento
wss.on("connection", (ws) => {

  ws.on("message", (msg) => {
    try {
      const data = JSON.parse(msg);

      if (data.type !== "camera") return;

      target.heading = data.heading ?? 0;
      target.pitch   = data.pitch ?? 0;

    } catch (e) {
      console.log("bad msg");
    }
  });

});

// Movimiento lento del motor
setInterval(() => {

  state.heading += (target.heading - state.heading) * 0.08;
  state.pitch   += (target.pitch - state.pitch) * 0.08;

  setProp("/sim/current-view/heading-offset-deg", state.heading);
  setProp("/sim/current-view/pitch-offset-deg", state.pitch);

}, 30);

console.log("Bridge running (target smooth mode)");