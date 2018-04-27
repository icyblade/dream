import json
from importlib import import_module

import os
from flask import Flask
from flask import request

from .helpers import flask_method, helper
from .models import Agent, Quota, db
from ..logger import build_logger

app = Flask('dream')
logger = build_logger('dream_server')

# parse $CONFIG_FILE
config_file_path = os.path.abspath(os.environ['CONFIG_FILE'])
if os.path.exists(config_file_path):
    with open(config_file_path, 'r') as f:
        for k, v in json.load(f).items():
            app.config[k] = v
else:
    raise Exception('Please specify $CONFIG_FILE.')

db.init_app(app)


@app.route('/api', methods=['GET', 'POST'])
@flask_method
def api():
    """API Entry point."""
    action = request.args.get('action', '')
    http_method = request.method

    def action_eq(*args):
        assert args

        for i in args:
            if i.lower().strip() != args[0].lower().strip():
                return False

        return True

    if http_method == 'GET':
        if action_eq(action, 'GetAllList'):
            logger.warning('GetAllList is deprecated, use GetAIList instead.')
            return get_running_agents(request)
        elif action_eq(action, 'GetAIList'):
            return get_running_agents(request)
        elif action_eq(action, 'GetQuotaList'):
            return get_available_agents(request)
        else:
            raise ValueError(f'Invalid parameter action: {action}')
    elif http_method == 'POST':
        if action_eq(action, 'Create'):
            return create(request)
        elif action_eq(action, 'Delete'):
            return delete(request)
        elif action_eq(action, 'Empty'):
            return empty(request)
        else:
            raise ValueError(f'Invalid parameter action: {action}')
    else:
        raise ValueError(f'Invalid HTTP method: {http_method}')


@helper
def get_nb_running_agents():
    """Get numbers of running agents.

    Returns
    --------
    dict
        Mapping between agent type and numbers of running agents of this agent type.
    """
    return dict(db.session.query(
        Agent.type, db.func.count(Agent.id)
    ).group_by(Agent.type).all())


@helper
def get_nb_all_agents():
    """Get quota of all available agents.

    Returns
    --------
    dict
        Mapping between agent type and quota of this agent type.
    """
    return dict(db.session.query(
        Quota.type, Quota.maximum_quota
    ).all())


@helper
def get_nb_available_agents():
    """Get numbers of remaining agents.

    Equals to quota of all agents minus numbers of running agents.

    Returns
    --------
    dict
        Mapping between agent type and numbers of remaining agents of this agent type.
    """
    nb_running_agents = get_nb_running_agents()
    agent_quota = get_nb_all_agents()

    result = {}
    for agent_type, value in agent_quota.items():
        if agent_type in nb_running_agents:
            result[agent_type] = value - nb_running_agents[agent_type]
        else:
            result[agent_type] = value

    return result


@flask_method
def get_running_agents(request):
    """Get numbers of running agents."""
    result = {}
    for agent_type, value in get_nb_running_agents().items():
        agent = getattr(import_module(f'dream.agent.{agent_type}'), 'Agent')
        result[agent_type] = {
            'numbers': value,
            'EVRange': agent.ev_range,
        }
    return json.dumps({
        'errcode': 0,
        'AITypeList': result,
    })


@flask_method
def get_available_agents(request):
    """Get numbers of remaining agents."""
    result = {}
    for agent_type, value in get_nb_available_agents().items():
        agent = getattr(import_module(f'dream.agent.{agent_type}'), 'Agent')
        result[agent_type] = {
            'numbers': value,
            'EVRange': agent.ev_range
        }

    return json.dumps({
        'errcode': 0,
        'AITypeList': result,
    })


@flask_method
def create(request):
    table_id = request.get_json()['tableid']
    position = request.get_json()['position']
    ai_type = request.get_json()['AIType']

    assert position.isdigit()
    seat_id = int(position) - 1  # convert 1-9 to 0-8

    assert 0 <= seat_id <= 8

    quota = get_nb_available_agents()
    assert str(ai_type) in quota
    assert quota[str(ai_type)] >= 0

    agent = Agent(type=ai_type, name=ai_type, port=41488)  # TODO
    db.session.add(agent)
    db.session.commit()

    return json.dumps({
        'errcode': 0,
        'tableid': table_id, 'position': position,
        'port': agent.port, 'address': f'tcp://{app.config["SERVER_ADDRESS"]}:{agent.port}',
        'AIType': ai_type, 'AIID': agent.id,
    })


@flask_method
def delete(request):
    ai_id = request.get_json()['AIID']
    for i in Agent.query.filter_by(id=ai_id):
        db.session.delete(i)
    db.session.commit()
    return json.dumps({'errcode': 0})


@flask_method
def empty(request):
    db.session.query(Agent).delete()
    db.session.commit()
    return json.dumps({'errcode': 0})
