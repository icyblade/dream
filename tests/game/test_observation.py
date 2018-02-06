def test_observation():
    from dream.game.observation import Observation
    from dream.game.card import Card

    ob = Observation()
    ob.update_json({
        'playerAction': {
            'boardCards': '',
            'log': [],
            'newCards': '',
            'player': {
                'AIID': '2156',
                'card': '4h Qd',
                'chips': '2008',
                'position': '4',
                'userID': '2400'
            },
            'pots': [{
                'pot': '0'
            }],
            'round': 'PREFLOP'
        }
    })

    assert ob.seat == 4

    assert ob.combo == [Card('4h'), Card('Qd')]

    ob.board = ['9s', '7s', '6h']
    assert ob.board == [Card('9s'), Card('7s'), Card('6h')]

    assert ob.to_numeric() == [4, 2, 2, 10, 1]

    ob.update_json({
        'playerAction': {
            'boardCards': 'As Kh Kc',
            'log': [],
            'newCards': '',
            'player': {
                'AIID': '2156',
                'card': '4h Qd',
                'chips': '2008',
                'position': '4',
                'userID': '2400'
            },
            'pots': [{
                'pot': '0'
            }],
            'round': 'FLOP'
        }
    })
