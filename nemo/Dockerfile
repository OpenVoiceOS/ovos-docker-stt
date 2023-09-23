ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT Nemo image"
LABEL org.opencontainers.image.description="NVIDIA NeMo is a conversational AI toolkit built for researchers working on automatic speech recognition (ASR), natural language processing (NLP), and text-to-speech synthesis (TTS)."
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.created=${BUILD_DATE}
LABEL org.opencontainers.image.documentation="https://openvoiceos.github.io/community-docs"
LABEL org.opencontainers.image.source="https://github.com/OpenVoiceOS/ovos-docker-stt"
LABEL org.opencontainers.image.vendor="Open Voice OS"

ARG ALPHA=false
ARG USER=ovos

SHELL ["/bin/bash", "-c"]

RUN pip3 install aiohttp \
  && if [ "${ALPHA}" == "true" ]; then \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-fasterwhisper streaming-stt-nemo neon-stt-plugin-nemo --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-fasterwhisper streaming-stt-nemo neon-stt-plugin-nemo; \
  fi \
  && mkdir -p ${HOME}/flagged \
  && rm -rf ${HOME}/.cache/*

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

ENTRYPOINT ovos-stt-server --engine neon-stt-plugin-nemo

EXPOSE 8080
