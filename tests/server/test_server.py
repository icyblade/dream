from itertools import product

import requests

AGENTS = []  # agents to be created
for table_id, position, ai_type in product(range(5), range(9), ['bitter_banana']):
    AGENTS.append({
        'tableid': str(table_id), 'position': str(position), 'AIType': ai_type
    })


# not designed for integration test
def basic_operations(host='http://127.0.0.1:10000'):
    # base
    assert requests.get(f'{host}/api').json() == {
    }

    # empty agent list
    assert requests.post(f'{host}/api?action=EMPTY').json() == {
        'errcode': 0
    }

    # get all agents
    assert requests.get(f'{host}/api?action=GETALLLIST').json() == {
        'errcode': 0,
        'AITypeList': {},
    }

    # get quota
    result = requests.get(f'{host}/api?action=GETQUOTALIST').json()
    assert result == {
        'errcode': 0,
        'AITypeList': {'bitter_banana': {'numbers': 255, 'EVRange': 0.0}},
    }, result

    # create agents
    for index, agent in enumerate(AGENTS):
        result = requests.post(f'{host}/api?action=CREATE', json=agent).json()

        assert set(result.keys()) == {'errcode', 'tableid', 'position', 'port', 'address', 'AIType', 'AIID'}, result
        assert result['errcode'] == 0
        assert result['tableid'] == agent['tableid']
        assert result['position'] == agent['position']
        assert result['AIType'] == agent['AIType']
        AGENTS[index]['AIID'] = result['AIID']

    # get all agents
    assert requests.get(f'{host}/api?action=GETALLLIST').json() == {
        'errcode': 0,
        'AITypeList': {'bitter_banana': {'numbers': 45, 'EVRange': 0.0}},
    }

    # get quota
    assert requests.get(f'{host}/api?action=GETQUOTALIST').json() == {
        'errcode': 0,
        'AITypeList': {'bitter_banana': {'numbers': 210, 'EVRange': 0.0}},
    }

    # delete this agent
    for agent in AGENTS:
        assert requests.post(f'{host}/api?action=DELETE', json={
            'AIID': agent['AIID']
        }).json() == {'errcode': 0}

    # get all agents
    result = requests.get(f'{host}/api?action=GETALLLIST').json()
    assert result == {
        'errcode': 0,
        'AITypeList': {},
    }, result

    # get quota
    result = requests.get(f'{host}/api?action=GETQUOTALIST').json()
    assert result == {
        'errcode': 0,
        'AITypeList': {'bitter_banana': {'numbers': 255, 'EVRange': 0.0}},
    }, result


if __name__ == '__main__':
    basic_operations()
