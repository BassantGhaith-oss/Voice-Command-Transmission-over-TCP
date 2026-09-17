import socket
import sounddevice as sd
import wavio 
import whisper

print("loading audio...")

model = whisper.load_model("base")

print("Ready! send you command...")

sample_rate = 16000
Duration_sec = 8
Filename = "output.wav"

def record_to_wav():
    audio = sd.rec(int(Duration_sec * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    wavio.write(Filename, audio, sample_rate, sampwidth=2)

if __name__ == "__main__":
    record_to_wav()

def transcribe(Filename):
    result = model.transcribe(Filename)
    text = result["text"].strip().lower()
    return text

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(("0.0.0.0",5000))

server.listen(1)

print("waiting for client...")

conn,addr = server.accept()

print("client connected: ",addr)



while True:
    record_to_wav()
    text = transcribe(Filename)
    conn.sendall(text.encode())
    
conn.close()