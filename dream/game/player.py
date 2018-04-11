class Player(object):
    def __init__(self, player_name=None, seat_id=None, chips=None):
        self.player_name = player_name
        self.seat_id = seat_id
        self.chips = chips

    def __repr__(self):
        return f'<Player {self.player_name} at seat {self.seat_id}>'

    def __eq__(self, other):
        return self.player_name == other.player_name and self.seat_id == other.seat_id and self.chips == other.chips
