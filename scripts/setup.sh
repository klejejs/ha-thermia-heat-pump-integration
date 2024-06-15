#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

# Install dependencies

install_packages() {
  python -m pip \
    install \
    --upgrade \
    --disable-pip-version-check \
    "${@}"
}

install_packages "pip<23.2,>=21.3.1"
install_packages setuptools wheel
install_packages -r requirements.txt
