# In progress

```bash
docker compose up -d ovos_stt_fasterwhisper
```

```bash
docker compose up -d
```

```json
{
  "stt": {
    "module": "ovos-stt-plugin-deepgram",
    "ovos-stt-plugin-fasterwhisper": {
        "model": "small",
        "cpu_threads": 10
    },
    "ovos-stt-plugin-vosk-streaming": {
        "model": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
    },
    "ovos-stt-plugin-vosk": {
        "model": "http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    },
    "ovos-stt-plugin-deepgram": {
      "key": "CHANGE-ME"
    }
  }
}
```
