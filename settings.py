import os
cwd = os.path.dirname(os.path.realpath(__file__))

WEB_BIND_HOST = "127.0.0.1"
WEB_BIND_PORT = 7575
DEBUG = False

WHISPER_BINARY = f"{cwd}/whisper.cpp/main"
WHISPER_MODEL = f"{cwd}/whisper.cpp/models/ggml-base.en.bin"
