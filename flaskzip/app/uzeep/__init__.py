import os
from uzeep.ytapi import YTAPI
from uzeep.zip import Zipper
from flask import (
        Flask,
        request,
        Response
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='faodfbpewjpoij',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello'

    @app.route('/download', methods=['GET'])
    def download():
        args = request.args
        channel = args.get('channel')

        if channel is None:
            return "Channel not provided."

        def gen():
            ytapi = YTAPI()
            channel_id = ytapi.get_channel_id(channel)

            zipper = Zipper()
            zip_buf, title = zipper.zip_mp3s_from_channelid(channel_id)
            if zip_buf is not None:
                with open(f'{title}.zip', 'wb') as f:
                    f.write(zip_buf.getvalue())
                    yield f

        return Response(gen(), mimetype='application/octet-stream')

    return app
