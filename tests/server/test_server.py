from itertools import product

import os
import requests


TEST_PORT = 10000


def func_server_thread(return_value: list):
    try:
        host = f'http://127.0.0.1:{TEST_PORT}'
        AGENTS = []  # agents to be created
        for table_id, position, ai_type in product(range(2), range(1, 4), ['entangled_endive']):
            AGENTS.append({
                'tableid': str(table_id), 'position': str(position), 'AIType': ai_type
            })

        # empty agent list
        assert requests.post(f'{host}/api?action=Empty').json() == {
            'errcode': 0
        }

        # get all agents
        assert requests.get(f'{host}/api?action=GetAIList').json() == {
            'errcode': 0,
            'AITypeList': {},
        }

        # get quota
        result = requests.get(f'{host}/api?action=GetQuotaList').json()
        assert result == {
            'errcode': 0,
            'AITypeList': {'entangled_endive': {'numbers': 512, 'EVRange': 0.0}},
        }, result

        # create agents
        for index, agent in enumerate(AGENTS):
            result = requests.post(f'{host}/api?action=Create', json=agent).json()

            assert set(result.keys()) == {'errcode', 'tableid', 'position', 'port', 'address', 'AIType', 'AIID'}, result
            assert result['errcode'] == 0
            assert result['tableid'] == agent['tableid']
            assert result['position'] == agent['position']
            assert result['AIType'] == agent['AIType']
            AGENTS[index]['AIID'] = result['AIID']

        # get all agents
        assert requests.get(f'{host}/api?action=GetAIList').json() == {
            'errcode': 0,
            'AITypeList': {'entangled_endive': {'numbers': 6, 'EVRange': 0.0}},
        }

        # get quota
        assert requests.get(f'{host}/api?action=GetQuotaList').json() == {
            'errcode': 0,
            'AITypeList': {'entangled_endive': {'numbers': 506, 'EVRange': 0.0}},
        }

        # delete this agent
        for agent in AGENTS:
            assert requests.post(f'{host}/api?action=Delete', json={
                'AIID': agent['AIID']
            }).json() == {'errcode': 0}

        # get all agents
        result = requests.get(f'{host}/api?action=GetAIList').json()
        assert result == {
            'errcode': 0,
            'AITypeList': {},
        }, result

        # get quota
        result = requests.get(f'{host}/api?action=GetQuotaList').json()
        assert result == {
            'errcode': 0,
            'AITypeList': {'entangled_endive': {'numbers': 512, 'EVRange': 0.0}},
        }, result
    except Exception as e:
        return_value.append(e)


def server_thread_func(return_value: list):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        os.system((
            f'CONFIG_FILE={path}/../../config_travis.json '
            f'FLASK_APP={path}/../../dream/server/__init__.py '
            f'python3.6 -m flask run -h 0.0.0.0 -p {TEST_PORT}'
        ))
    except Exception as e:
        return_value.append(e)


def test_server():
    from time import sleep
    from threading import Thread

    server_test_exceptions, server_exceptions = [], []

    server_thread = Thread(target=server_thread_func, args=(server_exceptions,))
    test_thread = Thread(target=func_server_thread, args=(server_test_exceptions,))

    for i in [server_thread, test_thread]:
        i.daemon = True
        i.start()
        sleep(2)  # wait for server start

    test_thread.join()

    for e in server_exceptions:
        raise e

    for e in server_test_exceptions:
        raise e
