import asyncio
from quart import Quart, request, send_file

app = Quart(__name__)


def create_app():
    global app
    app = Quart(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1024

    @app.before_serving
    async def startup():
        import whisperapi.routes

    return app
