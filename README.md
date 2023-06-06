# Open Voice OS Speech-to-Text (STT) on Docker or Podman

## What is a Speech-to-Text (STT)?

*According to https://aws.amazon.com/what-is/speech-to-text:*

> Speech to text is a speech recognition software that enables the recognition and translation of spoken language into text through computational linguistics. It is also known as speech recognition or computer speech recognition. Specific applications, tools, and devices can transcribe audio streams in real-time to display text and act on it.

Open Voice OS provides support to different STT engines via a plugin mechanism exposing HTTP endpoints to be consumed by the voice assistant.

## Containerized STT plugins

To facilitate the installation and the adoption of local Speech-to-Text engine, we build a set of OCI images compatible with Docker, Podman and Kubernetes as well.

| Image                                | Port       | Description                                                                                                                                                          |
| ---                                  | ---        | ---                                                                                                                                                                  |
| `ovos-stt-plugin-chromium`           | 8082->8080 | A STT plugin for OVOS using the Google Chrome browser API                                                                                                            |
| `ovos-stt-plugin-deepgram`           | 8083->8080 | Unmatched accuracy. Blazing fast. Enterprise scale. Hands-down the best price. Everything developers need to build with confidence and ship faster                   |
| `ovos-stt-plugin-fasterwhisper`      | 8080->8080 | High-performance inference of OpenAI's Whisper automatic speech recognition (ASR) model                                                                              |
| `ovos-stt-plugin-fasterwhisper-cuda` | 8080->8080 | High-performance inference of OpenAI's Whisper automatic speech recognition (ASR) model supporting Nvidia CUDA                                                       |
| `ovos-stt-plugin-nemo`               | 8084->8080 | Conversational AI toolkit built for researchers working on automatic speech recognition (ASR), natural language processing (NLP), and text-to-speech synthesis (TTS) |
| `ovos-stt-plugin-vosk`               | 8081->8080 | Vosk is a speech recognition toolkit supporting more than 20 languages and dialects, works offline and able to run on lightweight devices                            |

## Requirements

### Docker or Podman

Docker or Podman *(rootless)* is of course required and `docker compose` *(not `docker-compose`!!)* or `podman-compose` is a nice to have to simplify the whole process of deploying the whole stack by using the `docker-compose.yml` files *(for Docker, this command will be embedded depending the version, for Podman, `podman-compose` command comes from a different package)*.

**If you plan to passthrough GPUs in order to leverage Nvidia CUDA with Docker or Podman, please make you configured your container engine properly to support GPUs.**

## How to build these images

The `base` image is the main layer for the other images, for example the `fasterwhisper` image requires the `base` image to be build.

```bash
git clone https://github.com/OpenVoiceOS/ovos-docker-stt.git
cd ovos-docker-stt
docker buildx build fasterwhisper/ -t smartgic/ovos-stt-server-fasterwhisper:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
  # Or:
podman buildx build fasterwhisper/ -t smartgic/ovos-stt-server-fasterwhisper:alpha --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --no-cache
```

### Arguments

There are a list of available arguments that could be used during the image build process.

| Name         | Value                              | Default   | Description                                                           |
| ---          | ---                                | ---       | ---                                                                   |
| `ALPHA`      | `true`                             | `false`   | Using the alpha releases from PyPi built from the `dev` branches      |
| `BUILD_DATE` | `$(date -u +'%Y-%m-%dT%H:%M:%SZ')` | `unkown`  | Used as `LABEL` within the Dockerfile to determine the build date     |
| `TAG`        | `dev`                              | `dev`     | OCI image tag, (e.g. `docker pull smartgic/ovos-stt-server-base:dev`) |
| `VERSION`    | `0.0.8a`                           | `unknown` | Used as `LABEL` within the Dockerfile to determine the version        |

Pre-build images are already available [here](https://hub.docker.com/u/smartgic) and are the default referenced within the `docker-compose.yml` file.

## How to use these images

`docker-compose.yml` file provides an easy way to provision the container stack *(volumes and services)* with the required configuration for each of them. `docker compose` or `podman-compose` both support environment files, check the `.env` file.

```bash
git clone https://github.com/OpenVoiceOS/ovos-docker-stt.git
mkdir -p ~/ovos/config
chown ${USER}:${USER} -R ~/ovos
cd ovos-docker-stt
docker compose up -d
  # Or:
podman-compose up -d
```

To reduce the potential overhead due to the image downloads and extracts, the `--parallel` option could be user in order to process the images by batch of `x` *(where `x` is an integer)*.

```bash
docker compose --parallel 3 up -d
  # Or:
podman-compose --parallel 3 up -d
```

If you only plan to use the Faster Whisper STT server then you could reference it to the command line.

```bash
docker compose up -d ovos_stt_fasterwhisper
  # Or:
podman-compose up -d ovos_stt_fasterwhisper
```

Some variables might need to be tuned to match your setup such as the timezone, the directories, *etc...*, have a look into the `.env` files befor running `docker compose` or `podman-compose`.

The `OVOS_USER` variable should be changed **only** if you build the Docker images with a different user than `ovos`.

## How to update the current stack

The easiest way to update a stack already deployed by `docker compose` or `podman-compose` is to use `docker compose` or `podman-compose`. :relaxed:

Because the `pull_policy` option of each service is set to `always`, everytime that a new image is uploaded with the same tag then `docker compose` or `podman-compose` will pull-it and re-create the container based on this new image.

```bash
docker compose up -d
  # Or:
podman-compose up -d
```

If you want to change the tag to deploy, update the `.env` file with the new value.

## Configuration the STT plugins

`~/ovos/config/mycroft.conf` configuration file is used to configura the STT plugin. Make sure to adapt the sample below to fit your requirements.

```json
{
  "logs": {
    "path": "stdout"
  },
  "stt": {
    "module": "ovos-stt-plugin-fasterwhisper",
    "ovos-stt-plugin-fasterwhisper": {
        "model": "large-v2",
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
    }
  }
}
```

If you don't plan to use Nvidia CUDA with the STT Faster Whisper plugin, then `use_cuda` should be set to `false` and `compute_type` set to `int8`.

## Configure the voice assistant

Once the STT servers are up and running, the voice assistant must be configured to reference them. Please make sure to add the section below to your `~/ovos/config/mycroft.conf` configuration file.

```json
{
  "stt": {
      "module": "ovos-stt-plugin-server",
      "fallback_module": "ovos-stt-plugin-vosk",
      "ovos-stt-plugin-server": {
        "url": [
          "http://192.168.1.227:8080/stt",
          "http://192.168.1.227:8081/stt",
          "http://192.168.1.227:8082/stt",
          "http://192.168.1.227:8083/stt",
          "http://192.168.1.227:8084/stt",
          "https://stt.openvoiceos.org/stt"
        ]
      }
  }
}
```

The configuration means that `ovos-stt-plugin-server` will be used as default STT plugin. The plugin has a list of five *(5)* STT servers, if one is down then the plugin goes to the next one, etc...

If all the STT servers from `ovos-stt-plugin-server` are down then the voice assistant will fallback to the `ovos-stt-plugin-vosk` STT server running locally to the voice assistant.

## Debug

### Is the STT alive?

In order to check if a STT server is up and running, the `/status` endpoint should be called *(`jq` command is not mandatory just nice to have)*.

```bash
curl -v http://192.168.1.227:8080/status | jq
```

### Logging

Enable debug mode in `~/ovos/config/mycroft.conf` to get more verbosity from the logs. All containers will have to be restarted to receive the configuration change.

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

To access all the container logs at the same time, run the following command *(make sure it matches the `docker compose` or `podman-compose` command you run to deploy the stack)*:

```bash
docker compose logs -f --tail 200
  # Or:
podman-compose logs -n -f --tail 200
```

To access the logs of a specific container, run the following command:

```bash
docker logs -f --tail 200 ovos_stt_fasterwhisper
  # Or:
podman logs -f --tail 200 ovos_stt_fasterwhisper
```


To go inside a container and run multiple commands, run the following command *(where `bash` is the available shell in there)*:

```bash
docker exec -ti ovos_stt_fasterwhisper bash
  # Or:
podman exec -ti ovos_stt_fasterwhisper bash
```

If the configuration file is not valid JSON, `jq` will return something like this:

```text
parse error: Expected another key-value pair at line 81, column 3
```

To get the CPU, memory and I/O consumption per container, run the following command:

```bash
docker stats -a --no-trunc
  # Or:
podman stats -a --no-trunc
```

### Validate configuration

Make sure `mycroft.conf` configuration file is JSON valid by using the `jq` command.

```bash
cat ~/ovos/config/mycroft.conf | jq
```

## Support

- [Matrix channel](https://matrix.to/#/#openvoiceos:matrix.org)
- [Open Voice OS documentation](https://openvoiceos.github.io/community-docs/)
- [Contribute to Open Voice OS](https://openvoiceos.github.io/community-docs/contributing/)
- [Report bugs related to these Docker images](https://github.com/OpenVoiceOS/ovos-docker-stt/issues)
