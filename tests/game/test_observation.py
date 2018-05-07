def test_observation():
    from dream.game.observation import Observation
    from dream.game.card import Card

    ob = Observation()
    ob.update_json({
        'playerAction': {
            'boardCards': '',
            'log': [
                'ONE',
                'TWO',
                'THREE'
            ],
            'newCards': '',
            'player': {
                'AIID': '2156',
                'card': '4h Qd',
                'chips': '2008',
                'position': '4',
                'userID': '2400'
            },
            'pots': {
                'pot': '0'
            },
            'round': 'PREFLOP'
        }
    })

    assert ob.seat == 4

    assert ob.combo == [Card('4h'), Card('Qd')]

    assert ob.board is None

    assert ob.to_numeric() == [4, 28, 131]

    assert ob.pots == {'pot': 0}

    assert ob.chips == 2008

    ob.update_json({
        'playerAction': {
            'boardCards': 'As Kh Kc',
            'log': [
                'ONE',
                'TWO',
                'THREE'
            ],
            'newCards': '',
            'player': {
                'AIID': '2156',
                'card': '4h Qd',
                'chips': '2008',
                'position': '4',
                'userID': '2400'
            },
            'pots': {
                'pot': '0'
            },
            'round': 'FLOP'
        }
    })

    assert ob.json == {
        'playerAction': {
            'boardCards': 'As Kh Kc',
            'log': [
                'ONE',
                'TWO',
                'THREE'
            ],
            'newCards': '',
            'player': {
                'AIID': '2156',
                'card': '4h Qd',
                'chips': '2008',
                'position': '4',
                'userID': '2400'
            },
            'pots': {
                'pot': '0'
            },
            'round': 'FLOP'
        }
    }

    assert ob.board == [Card('As'), Card('Kh'), Card('Kc')]
    assert ob.log == 'ONE\nTWO\nTHREE'
