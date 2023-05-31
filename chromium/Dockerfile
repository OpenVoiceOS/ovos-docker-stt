ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT Chromium image"
LABEL org.opencontainers.image.description="A STT plugin for OVOS using the Google Chrome browser API"
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
  pip3 install ovos-stt-http-server SpeechRecognition git+https://github.com/OpenVoiceOS/ovos-stt-plugin-chromium.git --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-chromium; \
  fi \
  && rm -rf ${HOME}/.cache

USER $USER

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-chromium
