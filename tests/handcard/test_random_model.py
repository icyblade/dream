def test_random_model():
    import numpy as np
    from dream.handcard.random_model import RandomModel

    handcard = RandomModel()

    proba = handcard.predict_proba(None, None)

    assert len(proba) == handcard.sample_size
    assert np.isclose(sum((value for key, value in proba)), 1)
