def test_rank():
    from dream.game.card import Rank

    assert repr(Rank(10)) == 'Rank(T)'
    assert str(Rank(10)) == 'T'


def test_suit():
    from dream.game.card import Suit

    assert repr(Suit('c')) == 'Suit(♣)'
    assert str(Suit('♣')) == 'c'


def test_card():
    from dream.game.card import Card

    card = Card('Tc')

    assert repr(card) == 'Card(T♣)'
    assert str(card) == 'Tc'

    assert card == Card('TC')
    assert card != Card('Ts')
    assert card != Card('Ac')
