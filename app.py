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

def validate_channel_name(channel):
    pass

    #!TODO
    #Really maybe just do a try/except
def init_watcher():
    for creator in creators:
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

init_watcher()

@app.route('/', methods=['GET'])
def index():
    return 'flask ok'

@app.route('/reboot', methods=['POST'])
def reboot_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = headers.get('X-Channel-Name')
    if api_key in valid_keys:
       container = client.containers.get(channel)
       container.restart()
       return jsonify({"message":"yayayaya"})
    return jsonify({"message":"nahanahnahnah"})

@app.route('/status', methods=['GET'])
def status_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = headers.get('X-Channel-Name')
    if api_key in valid_keys:
        container = client.containers.get(channel)
        return jsonify({"status":container.status})
    return jsonify({"message":"Nahanahnahnah"})

@app.route('/kill', methods=['POST'])
def kill_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = headers.get('X-Channel-Name')
    if api_key in valid_keys:
        container = client.containers.get(channel)
        if container.status != 'exited':
            container.kill()
        return jsonify({"message":"yayayaya"})
    return jsonify({"message":"nahanahnahnah"})

@app.route('/spawn', methods=['POST'])
def spawn_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = headers.get('X-Channel-Name')
    creator_id = headers.get('X-Creator-Id')
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
        else:
            print('found container, i guess')
            container = client.containers.get(channel)
            container.restart()

        return jsonify({"message":"yayayaya"})
   
    return jsonify({"message":"nahanahnahnah"})

@app.route('/remove', methods=['POST'])
def remove_route():
    headers = request.headers
    api_key = headers.get('X-Api-Key')
    channel = headers.get('X-Channel-Name')
    if api_key in valid_keys:
        container = client.containers.get(channel)
        if container.status != 'exited':
            container.kill()
        container.remove()
        return jsonify({"message":"yayayaya"})
    return jsonify({"message":"nahanahnahnah"})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
