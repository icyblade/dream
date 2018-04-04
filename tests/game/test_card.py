def test_rank():
    from dream.game.card import Rank

    assert repr(Rank(10)) == 'Rank(T)'
    assert str(Rank(10)) == 'T'


def test_suit():
    from dream.game.card import Suit

    assert repr(Suit('c')) == 'Suit(c)'
    assert str(Suit('♣')) == 'c'


def test_card():
    from dream.game.card import Card

    card = Card('Ac')

    assert repr(card) == 'Card(Ac)'
    assert str(card) == 'Ac'

    assert card == Card('AC')
    assert card != Card('As')
    assert card != Card('Tc')
    assert card != Card('10c')

    assert card.to_numeric() == 156
