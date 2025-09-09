# Sourcery and gcsfuse won't run on `arm` so force the use of `amd64` for the base image.
FROM --platform=linux/amd64 ghcr.io/astral-sh/uv:python3.13-bookworm AS base

# Install uv for everyone not just the current user.
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
#  && cp /root/.local/bin/uv /usr/local/bin/uv

# Add some labels so it looks nice in Github packages.
LABEL org.opencontainers.image.source=https://github.com/joejcollins/sandra-benes
LABEL org.opencontainers.image.description="sandra-benes image."
