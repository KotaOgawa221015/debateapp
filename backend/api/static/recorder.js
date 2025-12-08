// frontend/recorder.js

const WS_URL = "ws://127.0.0.1:8100/ws/stream";  // ← 社内LANならサーバIPでOK
let ws;
let mediaRecorder;
let audioStream;

const startBtn = document.getElementById("start");
const stopBtn  = document.getElementById("stop");
const partialBox = document.getElementById("partial");
const finalsList = document.getElementById("finals");

startBtn.addEventListener("click", startRecording);
stopBtn.addEventListener("click", stopRecording);

async function startRecording() {
  try {
    audioStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
  } catch (err) {
    alert("⚠ マイクのアクセスが拒否されました: " + err);
    return;
  }

  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";

  ws.onopen = () => {
    console.log("✅ WebSocket 接続完了");
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === "partial") {
      partialBox.textContent = msg.text;
    } else if (msg.type === "final") {
      const li = document.createElement("li");
      li.textContent = msg.text;
      finalsList.appendChild(li);
    }
  };

  ws.onerror = () => {
    alert("⚠ WebSocket 接続に失敗しました");
  };

  ws.onclose = () => {
    console.log("🔌 WebSocket 接続終了");
  };

  mediaRecorder = new MediaRecorder(audioStream, { mimeType: "audio/webm;codecs=opus" });

  mediaRecorder.ondataavailable = async (event) => {
    if (event.data && event.data.size > 0 && ws.readyState === 1) {
      const buffer = await event.data.arrayBuffer();
      ws.send(buffer);
    }
  };

  mediaRecorder.onstart = () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    stopBtn.disabled = false;
    stopBtn.removeAttribute("disabled");
    stopBtn.disabled = false;
    stopBtn.disabled = false;
    startBtn.setAttribute("disabled", true);
    stopBtn.removeAttribute("disabled");
    stopBtn.disabled = false;
    stopBtn.disabled = false;
    startBtn.textContent = "録音中...";
  };

  mediaRecorder.onstop = () => {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    startBtn.textContent = "開始";
  };

  mediaRecorder.start(200); // 200msごとに chunk 送信（低遅延）
  stopBtn.disabled = false;
  stopBtn.removeAttribute("disabled");
}
  
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }

  audioStream?.getTracks().forEach(track => track.stop());
  ws?.close();
  partialBox.textContent = "--";
}
