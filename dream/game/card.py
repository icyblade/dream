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
    TEN = 'T', '10', 10
    JACK = 'J', 'j', 11
    QUEEN = 'Q', 'q', 12
    KING = 'K', 'k', 13
    ACE = 'A', 'a', 1

    def __repr__(self):
        """repr.

        For example: Rank(T).
        """
        return f'Rank({self.value})'

    def __str__(self):
        """str.

        For example: T.
        """
        return str(self.value)

    def to_numeric(self):
        """Convert Rank to numeric values.

        Used for label binarization.
        """
        if self.values[-1] == 1:
            return 12
        else:
            return self.values[-1] - 2


class Suit(MultiValueEnum):
    CLUBS = '♣', 'c', 'C', 'clubs'
    DIAMONDS = '♦', 'd', 'D', 'diamonds'
    HEARTS = '♥', 'h', 'H', 'hearts'
    SPADES = '♠', 's', 'S', 'spades'

    def __repr__(self):
        """repr.

        For example: Suit(♣).
        """
        return f'Suit({self.value})'

    def __str__(self):
        """str.

        For example: c.
        """
        return self.values[1]

    def to_numeric(self):
        """Convert Suit to numeric values.

        Used for label binarization.
        """
        return ['♣', '♦', '♥', '♠'].index(self.value)


class Card(object):
    """Abstract class of card of Texas Hold'em.

    Parameters
    --------
    raw: str or list of Card
        Raw card string, for example: As. Or list of Card.
    """

    def __init__(self, raw):
        if isinstance(raw, Card):
            self.rank, self.suit = raw.rank, raw.suit
        else:
            assert len(raw) == 2 or (len(raw) == 3 and raw[0] == '1')

            self.rank, self.suit = Rank(raw[:-1]), Suit(raw[-1])

    def __repr__(self):
        """repr.

        For example: Card(T♣).
        """
        return f'Card({self.rank.value}{self.suit.value})'

    def __str__(self):
        """str.

        For example: Tc
        """
        return f'{str(self.rank)}{str(self.suit)}'

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def to_numeric(self):
        """Convert Card to numeric values.

        Used for label binarization.
        """
        return [self.rank.to_numeric(), self.suit.to_numeric()]
