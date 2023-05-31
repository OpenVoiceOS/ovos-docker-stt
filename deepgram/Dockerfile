ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT Deepgram image"
LABEL org.opencontainers.image.description="Unmatched accuracy. Blazing fast. Enterprise scale. Hands-down the best price. Everything developers need to build with confidence and ship faster"
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
  pip3 install ovos-stt-http-server SpeechRecognition git+https://github.com/OpenVoiceOS/ovos-stt-plugin-deepgram.git --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-deepgram; \
  fi \
  && rm -rf ${HOME}/.cache

USER $USER

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-deepgram
