ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT FastWhisper image"
LABEL org.opencontainers.image.description="High-performance inference of OpenAI's Whisper automatic speech recognition (ASR) model"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.documentation="https://openvoiceos.github.io/community-docs"
LABEL org.opencontainers.image.source="https://github.com/OpenVoiceOS/ovos-docker"
LABEL org.opencontainers.image.vendor="Open Voice OS"

ARG ALPHA=false
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-fasterwhisper --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-fasterwhisper; \
  fi \
  && mkdir -p ${HOME}/flagged \
  && rm -rf ${HOME}/.cache/*

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv


ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-fasterwhisper
