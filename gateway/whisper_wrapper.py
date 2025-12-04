# gateway/whisper_wrapper.py
import subprocess
import threading
import queue
import sys

class WhisperStream:
    def __init__(self):
        self.proc = subprocess.Popen(
            ["./whisper/run_whisper.sh"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        self.q = queue.Queue()
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()

    def _read_loop(self):
        for line in self.proc.stdout:
            self.q.put(line.strip())

    def feed_audio(self, audio_bytes):
        if not self.proc:
            return None
        self.proc.stdin.buffer.write(audio_bytes)
        self.proc.stdin.flush()

        text = None
        while not self.q.empty():
            text = self.q.get()
        return text

    def close(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None
