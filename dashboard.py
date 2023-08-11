from threading import Thread
from flask import Flask, render_template, request, session, redirect, jsonify, url_for, abort
from settingsClass import settings
import os
import dashboard_settings
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "this_is_a_secret"

BOT_TOKEN: str | None = None


@app.route('/')
def home():
    return render_template('index.html', oauth_url=dashboard_settings.OAUTH_URL)


@app.route('/oauth/callback')
def oauth_discord():
    token = dashboard_settings.get_token(request.args.get('code'))
    session['token'] = token
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect(dashboard_settings.OAUTH_URL)
    user_guilds = dashboard_settings.get_user_guilds(session.get('token'))
    bot_guilds = dashboard_settings.get_bot_guilds(BOT_TOKEN)
    mutuals = dashboard_settings.get_mutual_guilds(user_guilds, bot_guilds)
    if len(mutuals) == 0 or mutuals is None:
        return render_template('no_guilds.html')
    return render_template('dashboard.html', guilds=mutuals)


@app.route('/guild/<guild_id>', methods=['GET', 'POST'])
def guild(guild_id):
    guild_info = dashboard_settings.get_guild_data(guild_id, BOT_TOKEN)  # Replace with actual guild data retrieval
    if not guild_info:
        return redirect(url_for('dashboard'))

    sorted_settings = sorted(dashboard_settings.settings_types.items(),
                             key=lambda item: dashboard_settings.settings_type_names.index(item[1]))

    return render_template('guild.html', guild=guild_info, settings=sorted_settings,
                           categories=dashboard_settings.settings_type_names, category_data=settings.__dict__)


@app.route('/api/settings/update/<code>', methods=['POST'])
def update_settings(code):
    if code != '87350819':
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        data = request.json  # Get the JSON data from the request

        settings.update_settings(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'title': 'success'}), 200


@app.route('/api/settings/set/<code>/<setting>/<value>', methods=["POST"])
def set_setting(code, setting, value):
    if value == "style.css":
        return "success", 200

    if int(code) != 87350819:
        return abort(403)
    elif setting not in settings.__dict__:
        return abort(400)
    else:
        new = settings.__dict__
        if isinstance(new[setting], str):
            new[setting] = value
        elif isinstance(new[setting], int):
            try:
                new[setting] = int(value)
            except ValueError:
                return abort(400)
        elif isinstance(new[setting], bool):
            try:
                new[setting] = bool(value)
            except ValueError:
                return abort(400)
        else:
            split = setting.split(':')
            if len(split) <= 1:
                return abort(400)

            if split[0] in new:
                if split[1] in new[split[0]]:
                    new[split[0]][split[1]] = value
                else:
                    return abort(400)
            else:
                return abort(400)

        settings.update_settings(new)
        return "success", 200


@app.route('/api/settings/add/list/<code>/<list_name>/<value>', methods=['POST'])
def add_to_list(code, list_name, value):
    if code != '87350819':
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        value = json.loads(value)  # Assuming the value is JSON formatted, you can modify this based on your data type
        settings[list_name].append(value)
        settings.save_to_json()  # Save the updated settings
        return jsonify({'success': True})
    except KeyError:
        return jsonify({'error': 'List not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400


@app.route('/api/settings/remove/list/<code>/<list_name>/<value>', methods=['POST'])
def remove_from_list(code, list_name, value):
    if code != '87350819':
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        value = json.loads(value)  # Assuming the value is JSON formatted, you can modify this based on your data type
        if value in settings[list_name]:
            settings[list_name].remove(value)
            settings.save_to_json()  # Save the updated settings
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Value not found in list'}), 404
    except KeyError:
        return jsonify({'error': 'List not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400


@app.route('/api/settings/add/dict/<code>/<dict_name>/<value_name>/<value>', methods=['POST'])
def add_to_dict(code, dict_name, value_name, value):
    if code != '87350819':
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        value = json.loads(value)  # Assuming the value is JSON formatted, you can modify this based on your data type
        settings[dict_name][value_name] = value
        settings.save_to_json()  # Save the updated settings
        return jsonify({'success': True})
    except KeyError:
        return jsonify({'error': 'Dictionary not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400


@app.route('/api/settings/remove/dict/<code>/<dict_name>/<value>', methods=['POST'])
def remove_from_dict(code, dict_name, value):
    if code != '87350819':
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        if value in settings[dict_name]:
            del settings[dict_name][value]
            settings.save_to_json()  # Save the updated settings
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Key not found in dictionary'}), 404
    except KeyError:
        return jsonify({'error': 'Dictionary not found'}), 404


def run(debug):
    global BOT_TOKEN
    if os.path.exists("./token.txt"):
        with open("./token.txt", "r") as f:
            lines = f.readlines()
            BOT_TOKEN = lines[0]
            print("loaded token from token.txt")
    else:
        BOT_TOKEN = os.environ['TOKEN']

    if BOT_TOKEN is None:
        print("no token!")
        return
    else:
        app.run(
            host='0.0.0.0',
            port=2710,
            debug=debug
        )


def start():
    """
        Creates and starts new thread that runs the function run.
    """
    t = Thread(target=run, args=(False,))
    t.start()
