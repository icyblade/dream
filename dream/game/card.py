from aenum import MultiValueEnum


class Rank(MultiValueEnum):
    DEUCE = '2', 2
    THREE = '3', 3
    FOUR = '4', 4
    FIVE = '5', 5
    SIX = '6', 6
    SEVEN = '7', 7
    EIGHT = '8', 8
    NINE = '9', 9
    TEN = 'T', 10
    JACK = 'J',
    QUEEN = 'Q',
    KING = 'K',
    ACE = 'A', 1

    def __repr__(self):
        return f'Rank({self.value})'

    def __str__(self):
        return str(self.value)


class Suit(MultiValueEnum):
    CLUBS = '♣', 'c', 'C', 'clubs'
    DIAMONDS = '♦', 'd', 'D', 'diamonds'
    HEARTS = '♥', 'h', 'H', 'hearts'
    SPADES = '♠', 's', 'S', 'spades'

    def __repr__(self):
        return f'Suit({self.value})'

    def __str__(self):
        return self.values[1]


class Card(object):
    """Abstract class of card of Texas Hold'em.

    Parameters
    --------
    raw: str
        Raw card string. For example: As
    """

    def __init__(self, raw):
        assert len(raw) == 2

        self.rank, self.suit = Rank(raw[0]), Suit(raw[1])

    def __repr__(self):
        return f'Card({self.rank.value}{self.suit.value})'

    def __str__(self):
        return f'{str(self.rank)}{str(self.suit)}'

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
