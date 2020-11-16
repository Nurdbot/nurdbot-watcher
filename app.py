#test
import os
from flask import Flask, jsonify, request
import docker
from config import *
from models import *

app = Flask(__name__)

debug = True
client = docker.from_env()
if debug == True:
    creators = session.query(Creator).filter_by(twitch_channel = 'pronerd_jay').all()
else:
    creators = session.query(Creator).all()

app.config.from_pyfile('config.py')


@app.route('/', methods=['GET'])
def index():
    return 'flask ok'

@app.route('/reboot', methods=['POST'])
def reboot_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = request.json['channel_name']
    if api_key in valid_keys:
        try:
            container = client.containers.get(channel)
            container.restart()
            return jsonify(message='nailed it'),200
        except:
            return jsonify(message=f'no conatiner found for {channel}'), 404
    return jsonify(message=f'whomstve do you think you are> bad api key'), 403

@app.route('/status', methods=['POST'])
def status_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = request.json['channel_name']
    if api_key in valid_keys:
        try:
            container = client.containers.get(channel)
            return jsonify(status=container.status),200
        except:
            return jsonify(message=f'no conatiner found for {channel}'), 404
    return jsonify(message="whomstve do you think you are? bad api key."),403

@app.route('/kill', methods=['POST'])
def kill_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = request.json['channel_name']
    if api_key in valid_keys:
        try:
            container = client.containers.get(channel)
            if container.status != 'exited':
                container.kill()
                return jsonify(message='success'),200
            else:
                return jsonify(message="container is likely already in the exited status"), 400
        except:
            return jsonify(message=f'no conatiner found for {channel}'), 404
    return jsonify(message="whomstve do you think you are? bad api key."),403

@app.route('/spawn', methods=['POST'])
def spawn_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = request.json['channel_name']
    creator_id = request.json['creator_id']
    if api_key in valid_keys:
        exists =[]
        all_containers = client.containers.list(all=True)
        for a_container in all_containers:
            exists.append(a_container.name)

        if channel not in exists:
            container = client.containers.run(
                'nurdbot',
                name = channel,
                labels = [channel],
                detach = True,
                environment = [f'creator_id={creator_id}', f'twitch_username={channel}']
            )
            return jsonify(message='container spawned successfully. Happy birthday nurdbot.'), 200
        else:
            container = client.containers.get(channel)
            container.restart()
            return jsonify(message='container exists, rebooting it.'), 200
    return jsonify(message="whomstve do you think you are? bad api key."),403

@app.route('/remove', methods=['POST'])
def remove_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = request.json['channel_name']
    if api_key in valid_keys:
        container = client.containers.get(channel)
        if container.status != 'exited':
            container.kill()
        container.remove()
        return jsonify(message="he's dead jim."), 200
    return jsonify(message="whomstve do you think you are? bad api key."),403

def init_watcher():
    for creator in creators:
        if creator.twitch_channel !='pronerd_jay':
            print(creator.id)
            print('<o_o> Watching... ')
            print(creator.twitch_channel)
            exists =[]
            all_containers = client.containers.list(all=True)
            for a_container in all_containers:
                exists.append(a_container.name)

            if creator.twitch_channel not in exists:
                container = client.containers.run(
                    'nurdbot',
                    name = creator.twitch_channel,
                    labels = [creator.twitch_channel],
                    detach = True,
                    environment = [f'creator_id={creator.id}', f'twitch_username={creator.twitch_channel}']
                )
            else:
                print('found container, i guess')
                container = client.containers.get(creator.twitch_channel)
                container.restart()
    return print('all set.')

if __name__ == "__main__":
    init_watcher()
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
