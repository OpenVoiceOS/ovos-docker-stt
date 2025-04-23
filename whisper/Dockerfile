ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT Whisper image"
LABEL org.opencontainers.image.description="OpenAI's Whisper automatic speech recognition (ASR) model"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.documentation="https://openvoiceos.github.io/community-docs"
LABEL org.opencontainers.image.source="https://github.com/OpenVoiceOS/ovos-docker-stt"
LABEL org.opencontainers.image.vendor="Open Voice OS"

ARG ALPHA=true
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

COPY cpu.conf /etc/mycroft/mycroft.conf

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install ovos-stt-http-server SpeechRecognition git+https://github.com/TigreGotico/ovos-stt-plugin-whisper.git torch --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition git+https://github.com/TigreGotico/ovos-stt-plugin-whisper.git torch; \
  fi \
  && mkdir -p ${HOME}/flagged \
  && rm -rf ${HOME}/.cache/*

ENV PATH=/home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV=/home/${USER}/.venv

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-whisper

EXPOSE 8080
