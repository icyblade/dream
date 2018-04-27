from itertools import product

import os
import requests

if 'TRAVIS' not in os.environ:
    def test_server(host='http://127.0.0.1:10000'):
        AGENTS = []  # agents to be created
        for table_id, position, ai_type in product(range(2), range(6), ['entangled_endive']):
            AGENTS.append({
                'tableid': str(table_id), 'position': str(position), 'AIType': ai_type
            })

        # base
        assert requests.get(f'{host}/api').json() == {
            'errcode': 1, 'error_message': 'Invalid parameter action: '
        }

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
            'AITypeList': {'entangled_endive': {'numbers': 12, 'EVRange': 0.0}},
        }

        # get quota
        assert requests.get(f'{host}/api?action=GetQuotaList').json() == {
            'errcode': 0,
            'AITypeList': {'entangled_endive': {'numbers': 500, 'EVRange': 0.0}},
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
