import os


pokerstars_test_log = """PokerStars Hand #124959928530:  Hold'em No Limit ($10.00/$20.00 USD) - 2014/11/12 8:26:34 ET
Table 'Grus II' 6-max Seat #3 is the button
Seat 1: zazano ($2391 in chips)
Seat 2: jinmay ($7997.07 in chips)
Seat 3: davidtan23 ($2053.60 in chips)
Seat 4: Rednaxela747 ($1007.45 in chips)
Seat 5: bmlm ($2308.30 in chips)
Seat 6: heffalump75 ($2433.40 in chips)
Rednaxela747: posts small blind $10
bmlm: posts big blind $20
*** HOLE CARDS ***
Dealt to bmlm [Kh 4h]
heffalump75: folds
zazano: folds
jinmay: folds
davidtan23: folds
davidtan23 said, "haha yea thats true, anyway i cant either, since sg going to ban online gambling soon"
davidtan23 said, "unittest: test for colon bypass"
Rednaxela747: raises $40.80 to $60.80
bmlm: calls $40.80
*** FLOP *** [Jh 2h 3s]
Rednaxela747 said, "yeah heard"
Rednaxela747: checks
davidtan23 said, "unless i really take it serious n move to other country which is possible"
bmlm: bets $79.06
Rednaxela747 said, "or get a vpn"
Rednaxela747: calls $79.06
*** TURN *** [Jh 2h 3s] [Qd]
Rednaxela747: checks
davidtan23 said, "yea vpn a possibility"
bmlm: bets $184.47
Rednaxela747: calls $184.47
*** RIVER *** [Jh 2h 3s Qd] [5h]
Rednaxela747: checks
bmlm: bets $1983.97 and is all-in
Rednaxela747: calls $683.12 and is all-in
Uncalled bet ($1300.85) returned to bmlm
*** SHOW DOWN ***
bmlm: shows [Kh 4h] (a flush, King high)
Rednaxela747: shows [Ah Qc] (a pair of Queens)
bmlm collected $2011.90 from pot
*** SUMMARY ***
Total pot $2014.90 | Rake $3
Board [Jh 2h 3s Qd 5h]
Seat 1: zazano folded before Flop (didn't bet)
Seat 2: jinmay folded before Flop (didn't bet)
Seat 3: davidtan23 (button) folded before Flop (didn't bet)
Seat 4: Rednaxela747 (small blind) showed [Ah Qc] and lost with a pair of Queens
Seat 5: bmlm (big blind) showed [Kh 4h] and won ($2011.90) with a flush, King high
Seat 6: heffalump75 folded before Flop (didn't bet)"""


def test_pokerstars():
    from datetime import datetime
    from dream.game.log_parser import PokerStars
    from dream.game.card import Card

    game = PokerStars(log=pokerstars_test_log)

    assert game.log_id == 124959928530
    assert game.small_blind == 10
    assert game.big_blind == 20
    assert game.currency == 'USD'
    assert game.time == datetime(2014, 11, 12, 8, 26, 34)
    assert game.table_name == 'Grus II'
    assert game.max_players == 6
    assert game.button == 3
    assert sorted([
        (player.player_name, player.seat_id, player.chips)
        for player in game.players
    ], key=lambda x: x[1]) == ([
        ('zazano', 1, 2391), ('jinmay', 2, 7997.07), ('davidtan23', 3, 2053.60),
        ('Rednaxela747', 4, 1007.45), ('bmlm', 5, 2308.30), ('heffalump75', 6, 2433.40)
    ])

    assert game.get_player(seat_id=4).player_name == 'Rednaxela747'
    assert game.get_player(player_name='bmlm').seat_id == 5
    assert set(game._game_rounds.keys()).issubset({
        'preflop', 'flop', 'turn', 'river', 'show down', 'summary'
    })

    assert game.current_player.player_name == 'bmlm'
    assert game.current_handcard == [Card('Kh'), Card('4h')]

    assert game.community_cards == [Card('Jh'), Card('2h'), Card('3s'), Card('Qd'), Card('5h')]

    assert repr(game.get_actions(player_name='Rednaxela747', game_round='river')) == (
        '['
        '(<Player Rednaxela747 at seat 4>, CHECK), '
        '(<Player Rednaxela747 at seat 4>, ALLIN)'
        ']'
    )
    assert len(game.get_actions(player_name='Rednaxela747')) == 7

    assert game.winner.player_name == 'bmlm'


if 'TRAVIS' not in os.environ and 'FULLTEST' in os.environ:  # disable general tests
    def mini_batch(batch):
        from dream.game.log_parser import PokerStars
        for log in batch:
            PokerStars(log)

    def test_pokerstars_full():
        """Full PokerStars log simulation.

        This test will costs about 2 minutes at a 8-core machine.
        """
        import pickle
        import multiprocessing
        from multiprocessing import Process

        jobs = 8
        multiprocessing.set_start_method('forkserver', force=True)

        with open('/data/datasets/texas_holdem/data.pickle', 'rb') as f:
            data = pickle.load(f)

        full_batch_size = len(data)
        batch_size = full_batch_size // jobs

        processes = []
        for job_id in range(jobs):
            if job_id != jobs - 1:
                process = Process(target=mini_batch, args=(data[job_id*batch_size:(job_id+1)*batch_size],))
            else:
                process = Process(target=mini_batch, args=(data[job_id*batch_size:],))
            process.daemon = True
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
