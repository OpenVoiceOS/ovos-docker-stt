ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT ONNX ASR image"
LABEL org.opencontainers.image.description="Offline ONNX Runtime ASR using models such as Nvidia Canary, Parakeet, and OpenAI Whisper"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.documentation="https://openvoiceos.github.io/community-docs"
LABEL org.opencontainers.image.source="https://github.com/OpenVoiceOS/ovos-docker-stt"
LABEL org.opencontainers.image.vendor="Open Voice OS"

ARG ALPHA=false
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

COPY cpu.conf /etc/mycroft/mycroft.conf

RUN if [ "$(uname -m)" != "x86_64" ]; then \
  echo "ovos-stt-plugin-onnx-asr image is supported only on linux/amd64" >&2; \
  exit 1; \
  fi \
  && pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  MYCROFT_LOOSE_REQUIREMENTS=1 pip3 install git+https://github.com/OpenVoiceOS/ovos-stt-http-server.git@dev SpeechRecognition onnxruntime git+https://github.com/TigreGotico/ovos-stt-plugin-onnx-asr.git --pre; \
  else \
  MYCROFT_LOOSE_REQUIREMENTS=1 pip3 install git+https://github.com/OpenVoiceOS/ovos-stt-http-server.git@dev SpeechRecognition onnxruntime git+https://github.com/TigreGotico/ovos-stt-plugin-onnx-asr.git; \
  fi \
  && mkdir -p ${HOME}/flagged \
  && rm -rf ${HOME}/.cache/*

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-onnx-asr

EXPOSE 8080
