def test_observation():
    from dream.game.observation import Observation
    from dream.game.card import Card

    ob = Observation('')

    ob.seat = 0
    assert ob.seat == 0

    ob.combo = ['Ac', 'Ks']
    assert ob.combo == [Card('Ac'), Card('Ks')]

    ob.board = ['9s', '7s', '6h']
    assert ob.board == [Card('9s'), Card('7s'), Card('6h')]
