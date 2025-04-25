from core.stats_merger import StatsMerger


def test_merge_stats():
    stats1 = {
        "/api/v1/items/": {"INFO": 2, "ERROR": 1},
        "/api/v1/users/": {"INFO": 1}
    }
    stats2 = {
        "/api/v1/items/": {"INFO": 1, "WARNING": 1},
        "/api/v1/orders/": {"ERROR": 1}
    }

    merged = StatsMerger.merge([stats1, stats2])
    assert merged["/api/v1/items/"]["INFO"] == 3
    assert merged["/api/v1/items/"]["ERROR"] == 1
    assert merged["/api/v1/items/"]["WARNING"] == 1
    assert merged["/api/v1/users/"]["INFO"] == 1
    assert merged["/api/v1/orders/"]["ERROR"] == 1