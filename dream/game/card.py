from aenum import MultiValueEnum, OrderedEnum, unique


@unique
class Rank(MultiValueEnum, OrderedEnum):
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

        Todo
        --------
         - Use native members instead of hard-coded list.
        """
        return ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'].index(self.value)


@unique
class Suit(MultiValueEnum, OrderedEnum):
    CLUBS = 'c', '♣', 'C', 'clubs', 1
    DIAMONDS = 'd', '♦', 'D', 'diamonds', 2
    HEARTS = 'h', '♥', 'H', 'hearts', 3
    SPADES = 's', '♠', 'S', 'spades', 4

    def __repr__(self):
        """repr.

        For example: Suit(c).
        """
        return f'Suit({self.value})'

    def __str__(self):
        """str.

        For example: c.
        """
        return self.value

    def to_numeric(self):
        """Convert Suit to numeric values.

        Used for label binarization.

        Todo
        --------
         - Use native members instead of hard-coded list.
        """
        return ['c', 'd', 'h', 's'].index(self.value)


class Card(object):
    """Abstract class of Texas Hold'em card.

    Parameters
    --------
    raw: str or list of Card
        Raw card string, for example: As. Or list of Card.
    """

    def __init__(self, raw):
        if isinstance(raw, Card):
            self.rank, self.suit = raw.rank, raw.suit
        else:
            assert len(raw) == 2 or (len(raw) == 3 and raw[0] == '1')  # fix for something like 10c

            self.rank, self.suit = Rank(raw[:-1]), Suit(raw[-1])

    def __repr__(self):
        """repr.

        For example: Card(Tc).
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
        return len(Rank) * self.rank.to_numeric() + self.suit.to_numeric()
