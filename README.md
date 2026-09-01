# Open Voice OS Speech-to-Text (STT) on Docker or Podman

## What is Speech-to-Text (STT)?

*According to <https://aws.amazon.com/what-is/speech-to-text>:*

> Speech to text is a speech recognition software that enables the recognition and translation of spoken language into text through computational linguistics. It is also known as speech recognition or computer speech recognition. Specific applications, tools, and devices can transcribe audio streams in real-time to display text and act on it.

Open Voice OS supports different STT engines through a plugin mechanism. Each plugin exposes an HTTP endpoint that the voice assistant can use.

## Containerized STT plugins

This repository builds a set of OCI images for local Speech-to-Text engines. The images work with Docker, Podman, and Kubernetes.

| Image                                | Port | Description                                                                                                                                                          |
|--------------------------------------| ---  | ---                                                                                                                                                                  |
| `ovos-stt-plugin-chromium`           | 8082 | A STT plugin for OVOS using the Google Chrome browser API                                                                                                            |
| `ovos-stt-plugin-deepgram`           | 8083 | Cloud STT service from Deepgram, offered at enterprise scale                                                                                                         |
| `ovos-stt-plugin-fasterwhisper`      | 8080 | High-performance inference of OpenAI's Whisper automatic speech recognition (ASR) model                                                                              |
| `ovos-stt-plugin-fasterwhisper-cuda` | 8080 | High-performance inference of OpenAI's Whisper automatic speech recognition (ASR) model supporting Nvidia CUDA                                                       |
| `ovos-stt-plugin-citrinet`           | 8084 | Conversational AI toolkit built for researchers working on automatic speech recognition (ASR), natural language processing (NLP), and text-to-speech synthesis (TTS) |
| `ovos-stt-plugin-onnx-asr`           | 8085 | Offline ONNX Runtime ASR supporting models such as Nvidia Canary, Parakeet, and OpenAI Whisper                                                                      |
| `ovos-stt-plugin-onnx-asr-cuda`      | 8085 | Offline ONNX Runtime ASR supporting Nvidia CUDA                                                                                                                     |
| `ovos-stt-plugin-vosk`               | 8081 | Vosk is a speech recognition toolkit supporting more than 20 languages and dialects, works offline and able to run on lightweight devices                            |

This approach also lets you decentralize the STT server. The server does not have to run on the voice assistant. It can run on a remote server with more CPU and/or GPU power.

### Image alternatives

There are two implementations of the Faster Whisper STT plugin.

- `ovos-stt-plugin-fasterwhisper` uses only the CPU to transcribe (default).
- `ovos-stt-plugin-fasterwhisper-cuda` uses only the GPU to transcribe.

To use `ovos-stt-plugin-fasterwhisper-cuda`, review the `docker-compose.yml` file.

**Only one implementation can run at a time.**

There are also two implementations of the ONNX ASR STT plugin.

- `ovos-stt-plugin-onnx-asr` uses ONNX Runtime CPU execution.
- `ovos-stt-plugin-onnx-asr-cuda` uses ONNX Runtime GPU execution.

To use `ovos-stt-plugin-onnx-asr-cuda`, review the `docker-compose.cuda.yml` file.

## Requirements

### Docker or Podman

Docker or Podman (rootless) is required. `docker compose` (not `docker-compose`) or `podman-compose` helps simplify deployment of the stack using the `docker-compose.yml` files. For Docker, this command is embedded depending on the version. For Podman, the `podman-compose` command comes from a separate package.

**If you plan to pass through GPUs to use Nvidia CUDA with Docker or Podman, configure your container engine to support GPUs first.**

## How to build these images

The `base` image is the main layer for the other images. For example, the `fasterwhisper` image needs the `base` image built first.

```bash
git clone https://github.com/OpenVoiceOS/ovos-docker-stt.git
cd ovos-docker-stt
docker buildx build fasterwhisper/ -t smartgic/ovos-stt-server-fasterwhisper:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
  # Or:
podman buildx build fasterwhisper/ -t smartgic/ovos-stt-server-fasterwhisper:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
```

The `onnx-asr` image is available for `linux/amd64` only. Rebuild the base image first with the same tag, then build `onnx-asr` for `amd64`.

```bash
docker buildx build --platform linux/amd64 base/ -t smartgic/ovos-stt-server-base:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
docker buildx build --platform linux/amd64 onnx-asr/ -t smartgic/ovos-stt-server-onnx-asr:alpha --build-arg TAG=alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
  # Or:
podman buildx build --platform linux/amd64 base/ -t smartgic/ovos-stt-server-base:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
podman buildx build --platform linux/amd64 onnx-asr/ -t smartgic/ovos-stt-server-onnx-asr:alpha --build-arg TAG=alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
```

The `onnx-asr` CUDA image is available for `linux/amd64` only. Rebuild the CUDA base image first with the same tag, then build `onnx-asr` for `amd64`.

```bash
docker buildx build --platform linux/amd64 base/ -f base/Dockerfile.cuda -t smartgic/ovos-stt-server-base-cuda:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
docker buildx build --platform linux/amd64 onnx-asr/ -f onnx-asr/Dockerfile.cuda -t smartgic/ovos-stt-server-onnx-asr-cuda:alpha --build-arg TAG=alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
  # Or:
podman buildx build --platform linux/amd64 base/ -f base/Dockerfile.cuda -t smartgic/ovos-stt-server-base-cuda:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
podman buildx build --platform linux/amd64 onnx-asr/ -f onnx-asr/Dockerfile.cuda -t smartgic/ovos-stt-server-onnx-asr-cuda:alpha --build-arg TAG=alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
```

### Arguments

You can pass these arguments during the image build process.

| Name         | Value                              | Default   | Description                                                           |
| ---          | ---                                |-----------| ---                                                                   |
| `ALPHA`      | `true`                             | `false`   | Use the alpha releases from PyPI built from the `dev` branches        |
| `BUILD_DATE` | `$(date -u +'%Y-%m-%dT%H:%M:%SZ')` | `unknown` | Used as a `LABEL` in the Dockerfile to record the build date          |
| `TAG`        | `dev`                              | `dev`     | OCI image tag, (e.g. `docker pull smartgic/ovos-stt-server-base:dev`) |
| `VERSION`    | `0.0.8a`                           | `unknown` | Used as a `LABEL` in the Dockerfile to record the version             |

Pre-built images are available [here](https://hub.docker.com/u/smartgic). The `docker-compose.yml` file references them by default.

## How to use these images

The `docker-compose.yml` file provisions the container stack (volumes and services) with the required configuration for each service. `docker compose` and `podman-compose` both support environment files. Check the `.env` file.

```bash
git clone https://github.com/OpenVoiceOS/ovos-docker-stt.git
mkdir -p ~/ovos-tts-stt/config
chown ${USER}:${USER} -R ~/ovos-tts-stt
cd ovos-docker-stt
docker compose up -d
  # Or:
podman-compose up -d
```

To reduce overhead from image downloads and extraction, use the `--parallel` option to process images in batches of `x` (an integer).

```bash
docker compose --parallel 3 up -d
  # Or:
podman-compose --parallel 3 up -d
```

If you only plan to use the Faster Whisper STT server, reference it on the command line.

```bash
docker compose up -d ovos_stt_fasterwhisper
  # Or:
podman-compose up -d ovos_stt_fasterwhisper
```

Some variables might need tuning to match your setup, such as the timezone and directories. Check the `.env` file before running `docker compose` or `podman-compose`.

Change the `OVOS_USER` variable only if you build the Docker images with a different user than `ovos`.

## How to update the current stack

The easiest way to update a stack already deployed by `docker compose` or `podman-compose` is to use `docker compose` or `podman-compose` again.

Each service sets `pull_policy` to `always`. Every time a new image is uploaded with the same tag, `docker compose` or `podman-compose` pulls it and re-creates the container from the new image.

```bash
docker compose up -d
  # Or:
podman-compose up -d
```

To change the tag to deploy, update the `.env` file with the new value.

## Configure the STT plugins

The `~/ovos/config/mycroft.conf` configuration file configures the STT plugin. Adapt the sample below to fit your setup.

```json
{
  "logs": {
    "path": "stdout"
  },
  "stt": {
    "module": "ovos-stt-plugin-fasterwhisper",
    "ovos-stt-plugin-fasterwhisper": {
        "model": "whisper-large-v3-turbo",
        "compute_type": "float16",
        "use_cuda": true,
        "cpu_thread": 8
    },
    "ovos-stt-plugin-vosk-streaming": {
        "model": "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip",
        "verbose": false
    },
    "ovos-stt-plugin-vosk": {
        "model": "http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
        "verbose": false
    },
    "ovos-stt-plugin-deepgram": {
      "key": "GET A KEY FROM DEEPGRAM WEBSITE :)"
    },
    "ovos-stt-plugin-chromium": {
        "lang": "en-US",
        "pfilter": false,
        "debug": false
    },
    "ovos-stt-plugin-onnx-asr": {
        "model": "nemo-parakeet-tdt-0.6b-v3",
        "quantization": "int8"
    }
  }
}
```

If you do not plan to use Nvidia CUDA with the STT Faster Whisper plugin, set `use_cuda` to `false` and `compute_type` to `int8`.

If you plan to use Nvidia CUDA with the ONNX ASR plugin, omit `quantization` so the GPU image uses the non-quantized ONNX model files. The CUDA image also supports explicit ONNX Runtime providers.

```json
{
  "stt": {
    "module": "ovos-stt-plugin-onnx-asr",
    "ovos-stt-plugin-onnx-asr": {
        "model": "nemo-parakeet-tdt-0.6b-v3",
        "providers": [
            "CUDAExecutionProvider",
            "CPUExecutionProvider"
        ]
    }
  }
}
```

## Configure the voice assistant

Once the STT servers are running, configure the voice assistant to reference them. Add the section below to your `~/ovos/config/mycroft.conf` configuration file.

```json
{
  "stt": {
      "module": "ovos-stt-plugin-server",
      "fallback_module": "ovos-stt-plugin-vosk",
      "ovos-stt-plugin-server": {
        "urls": [
          "http://192.168.1.227:8080/stt",
          "http://192.168.1.227:8081/stt",
          "http://192.168.1.227:8082/stt",
          "http://192.168.1.227:8083/stt",
          "http://192.168.1.227:8084/stt",
          "http://192.168.1.227:8085/stt",
          "https://stt.openvoiceos.org/stt"
        ]
      }
  }
}
```

This configuration sets `ovos-stt-plugin-server` as the default STT plugin. The plugin holds a list of six STT servers. If one is down, the plugin tries the next one, and so on.

If all the STT servers from `ovos-stt-plugin-server` are down, the voice assistant falls back to the `ovos-stt-plugin-vosk` STT server running locally.

## Debug

### Is the STT alive?

To check if a STT server is up and running, call the `/status` endpoint (`jq` is not required, but it helps).

```bash
curl -v http://192.168.1.227:8080/status | jq
```

### Logging

Enable debug mode in `~/ovos/config/mycroft.conf` to get more detail from the logs. Restart all containers to apply the configuration change.

```json
{
  "debug": true,
  "log_level": "DEBUG",
  "logs": {
    "path": "stdout"
  }
}
```

### Container debugging

To see all container logs at the same time, run the command that matches how you deployed the stack:

```bash
docker compose logs -f --tail 200
  # Or:
podman-compose logs -n -f --tail 200
```

To see the logs of a specific container, run:

```bash
docker logs -f --tail 200 ovos_stt_fasterwhisper
  # Or:
podman logs -f --tail 200 ovos_stt_fasterwhisper
```

To go inside a container and run multiple commands, run this (`bash` is the shell available in the container):

```bash
docker exec -ti ovos_stt_fasterwhisper bash
  # Or:
podman exec -ti ovos_stt_fasterwhisper bash
```

If the configuration file is not valid JSON, `jq` returns an error like this:

```text
parse error: Expected another key-value pair at line 81, column 3
```

To get the CPU, memory, and I/O use per container, run:

```bash
docker stats -a --no-trunc
  # Or:
podman stats -a --no-trunc
```

### Validate configuration

Use the `jq` command to check that the `mycroft.conf` configuration file is valid JSON.

```bash
cat ~/ovos/config/mycroft.conf | jq
```

## Related projects

- [OpenVoiceOS/ovos-docker-tts](https://github.com/OpenVoiceOS/ovos-docker-tts) — Docker images for Open Voice OS Text-to-Speech (TTS) engines

## Support

- [Matrix channel](https://matrix.to/#/#openvoiceos:matrix.org)
- [Open Voice OS documentation](https://openvoiceos.github.io/community-docs/)
- [Contribute to Open Voice OS](https://openvoiceos.github.io/community-docs/contributing/)
- [Report bugs related to these Docker images](https://github.com/OpenVoiceOS/ovos-docker-stt/issues)
