#!/bin/bash
./whisper/build/bin/whisper \
  -m ./models/ggml-base.bin \
  --stream \
  --no-timestamps \
  --language ja
