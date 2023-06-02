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
    "module": "ovos-stt-plugin-fasterwhisper",
    "ovos-stt-plugin-fasterwhisper": {
        "model": "small",
        "cpu_threads": 32
    },
    "ovos-stt-plugin-vosk-streaming": {
        "model": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
    },
    "ovos-stt-plugin-vosk": {
        "model": "http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    },
    "ovos-stt-plugin-deepgram": {
      "key": "CHANGE-ME"
    },
    "ovos-stt-plugin-chromium": {
        "lang": "en-US",
        "pfilter": false
    }
  }
}
```

CUDA usage

nvidia-container-toolkit
https://github.com/containers/podman/discussions/16101


```json
{
  "stt": {
    "module": "ovos-stt-plugin-fasterwhisper",
    "ovos-stt-plugin-fasterwhisper": {
        "model": "large-v2",
        "use_cuda": true
    },
    "ovos-stt-plugin-vosk-streaming": {
        "model": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
    },
    "ovos-stt-plugin-vosk": {
        "model": "http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    },
    "ovos-stt-plugin-deepgram": {
      "key": "CHANGE-ME"
    },
    "ovos-stt-plugin-chromium": {
        "lang": "en-US",
        "pfilter": false
    }
  }
}
```