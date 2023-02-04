import os
import shutil
import asyncio
import tempfile

import aiofiles
from quart import Quart, request, send_file, render_template

import settings
from whisperapi.factory import app


@app.route("/", methods=["GET"])
async def root():
    return await render_template('index.html')


@app.route("/upload", methods=["POST"])
async def upload():
    files = await request.files
    audio_file = files.get('audio_file')
    if not audio_file:
        return "No file selected."

    if audio_file.filename == "":
        return "No file selected."

    if not audio_file.filename.endswith((".mp3", ".wav")):
        return "File must be an MP3 or WAV audio file."

    if audio_file.content_type not in [
        'audio/x-wav',
        'audio/mpeg3',
        'audio/mpeg',
        'audio/mp3',
        'audio/mpeg'
    ]:
        return "File must be an MP3 or WAV audio file."

    with tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None) as temp_dir:
        path_upload = os.path.join(temp_dir, 'upload')
        path_processed = os.path.join(temp_dir, 'processed.wav')
        path_srt = os.path.join(temp_dir, 'processed.wav.srt')

        await audio_file.save(path_upload)

        process = await asyncio.create_subprocess_exec(
            'timeout', '30',
            'ffmpeg', '-i', path_upload, '-ar', '16000', '-nostdin', path_processed,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.wait()
        data, _ = await process.communicate()

        process = await asyncio.create_subprocess_exec(
            'timeout', '30',
            settings.WHISPER_BINARY,
            '-m', settings.WHISPER_MODEL,
            '-f', path_processed,
            '-osrt',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.wait()
        data, _ = await process.communicate()

        data = None
        async with aiofiles.open(path_srt, mode='rb') as f:
            data = await f.read()

        return data
