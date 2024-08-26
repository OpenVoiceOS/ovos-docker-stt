ARG TAG=alpha
FROM smartgic/ovos-stt-server-base:${TAG}

ARG BUILD_DATE=unknown
ARG VERSION=unknown

LABEL org.opencontainers.image.title="Open Voice OS OCI STT Citrinet image"
LABEL org.opencontainers.image.description="Citrinet is a version of QuartzNet [ASR-MODELS6] that extends ContextNet [ASR-MODELS2], utilizing subword encoding (via Word Piece tokenization) and Squeeze-and-Excitation mechanism [ASR-MODELS4] to obtain highly accurate audio transcripts while utilizing a non-autoregressive CTC based decoding scheme for efficient inference."
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
  pip3 install ovos-stt-http-server SpeechRecognition git+https://github.com/OpenVoiceOS/ovos-stt-plugin-citrinet.git --pre; \
  else \
  pip3 install ovos-stt-http-server SpeechRecognition ovos-stt-plugin-citrinet; \
  fi \
  && mkdir -p ${HOME}/flagged \
  && rm -rf ${HOME}/.cache/*

ENV PATH /home/${USER}/.venv/bin:$PATH
ENV VIRTUAL_ENV /home/${USER}/.venv

ENTRYPOINT ovos-stt-server --engine ovos-stt-plugin-citrinet

EXPOSE 8080
