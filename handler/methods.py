from flask import jsonify, request, make_response

from loader import app
from data.config import DB_URI, DB_NAME, EMAIL, API_KEY
from utils.smtp import send_email
from utils.db_connector import MongodbAPI


@app.route('/api/v1.0/create', methods=['POST'])
def handler_keys():
    param_data = request.args
    api_key = param_data.get('api_key')
    if API_KEY != api_key:
        return make_response(jsonify({'error': 'Not api key'}), 401)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not json'}), 415)
    if len(request.data) == 0:
        return make_response(jsonify({'error': 'No content'}), 204)

    post_data = request.get_json()
    user_id = post_data.get('user_id')
    target_id = post_data.get('target_id')
    key = post_data.get('key')
    data = post_data.get('data')

    if user_id is None:
        return make_response(jsonify({'success': False, 'error': 'not value user_id'}), 400)
    elif len(user_id) != 24:
        return make_response(jsonify({'success': False, 'error': 'length user_id not is eval 24 symbols'}), 400)
    if key is None:
        return make_response(jsonify({'success': False, 'error': 'not value key'}), 400)
    elif not any(element in key for element in ['registration', 'new_message', 'new_post', 'new_login']):
        return make_response(jsonify({'success': False, 'error': 'not current key'}), 400)

    db = MongodbAPI(DB_URI, DB_NAME)

    if not db.check_user(user_id):
        db.create_user(EMAIL, user_id)

    db.new_notification(user_id,
        {
            "key": key,
            "target_id": target_id,
            "data": data if data is not None else [],
        }
    )

    user = db.get_user(user_id)
    send_email(user.get('email'), key)
    return make_response(jsonify({'success': True}), 201)


@app.route('/api/v1.0/list', methods=['GET'])
def get_list():
    param_data = request.args

    api_key = param_data.get('api_key')
    if API_KEY != api_key:
        return make_response(jsonify({'error': 'Not api key'}), 401)

    user_id = param_data.get('user_id')
    skip = param_data.get('skip')
    limit = param_data.get('limit')

    if not skip.isdigit():
        make_response(jsonify({'success': False, 'error': 'skip not is number'}), 400)
    if not limit.isdigit():
        make_response(jsonify({'success': False, 'error': 'limit not is number'}), 400)
    if user_id is None:
        return make_response(jsonify({'success': False, 'error': 'not value user_id'}), 400)

    db = MongodbAPI(DB_URI, DB_NAME)
    data = db.get_slice_user_notifications(user_id, int(skip), int(limit))
    return make_response(jsonify({'success': True, 'data': data}), 200)


@app.route('/api/v1.0/read', methods=['POST'])
def update_read():
    param_data = request.args
    api_key = param_data.get('api_key')
    if API_KEY != api_key:
        return make_response(jsonify({'error': 'Not api key'}), 401)

    if not request.is_json:
        return make_response(jsonify({'error': 'Not json'}), 415)
    if len(request.data) == 0:
        return make_response(jsonify({'error': 'No content'}), 204)
    post_data = request.get_json()
    user_id = post_data.get('user_id')
    notification_id = post_data.get('notification_id')

    if user_id is None:
        return make_response(jsonify({'success': False, 'error': 'not value user_id'}), 400)
    if notification_id is None:
        return make_response(jsonify({'success': False, 'error': 'not value notification_id'}), 400)

    db = MongodbAPI(DB_URI, DB_NAME)
    status = db.read_notification(user_id, notification_id)
    if status is None:
        return make_response(jsonify({'success': False, 'error': 'notification_id not funded'}), 400)
    elif status is False:
        return make_response(jsonify({'success': False, 'error': 'user_id not funded'}), 400)
    elif True:
        return make_response(jsonify({'success': True}), 200)

