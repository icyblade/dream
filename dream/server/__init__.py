import json
import os

from flask import Flask

from .models import Agent, Config, db

app = Flask('dream')

# parse $CONFIG_FILE
if os.path.exists(os.path.abspath(os.environ['CONFIG_FILE'])):
    with open(os.environ['CONFIG_FILE'], 'r') as fp:
        for k, v in json.load(fp).items():
            app.config[k] = v
else:
    raise Exception('Please specify $CONFIG_FILE.')


db.init_app(app)


@app.route('/list', defaults={'page': 0})
@app.route('/list/<page>')
def list(page, page_size=20):
    try:
        page = int(page)

        status = 'SUCCESS'
        errCode = 0
        message = ''
        maximum_agent = int(Config.query.filter_by(key='maximum_agent').first().value)
        n_current_agent = int(Agent.query.count())
        n_pages = n_current_agent // page_size + 1
        current_agents = Agent.query.offset(page * page_size).limit(page_size).all()
        current_agents = [row.as_dict() for row in current_agents]
        has_next_page = n_pages > page + 1
    except Exception as e:
        status = 'FAIL'
        errCode = -1
        message = str(e)
        maximum_agent = 0
        n_current_agent = 0
        n_pages = 1
        current_agents = []
        has_next_page = False

    return json.dumps({
        'status': status,
        'errCode': errCode,
        'message': message,
        'datas': {
            'maximum_agents': maximum_agent,
            'current_agents': current_agents,
        },
        'hasNextPage': has_next_page,
        'totalPages': n_pages,
        'totalCount': n_current_agent,
    })+'\n'


@app.route('/get/<name>')
def get(name):
    raise NotImplementedError


@app.route('/create/<name>')
def create(name):
    raise NotImplementedError


@app.route('/get_or_create/<name>')
def get_or_create(name):
    raise NotImplementedError


@app.route('/kill/<name>')
def kill(name):
    raise NotImplementedError
