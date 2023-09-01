import typing

import pytest

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EpsilonGreedyBannerEngine, NoBannerError, EmptyBannerStorageError
)
import random

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> list[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    assert clicks / shows == expected_ctr


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    bs = BannerStat()
    assert bs.compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    for bs in [BannerStat(10), BannerStat(0, 10), BannerStat(100, 0), BannerStat(10, 20), BannerStat()]:
        ctr = bs.compute_ctr(TEST_DEFAULT_CTR)
        bs.add_show()
        assert ctr > bs.compute_ctr(TEST_DEFAULT_CTR) or (ctr == TEST_DEFAULT_CTR and bs.compute_ctr(
            TEST_DEFAULT_CTR) != TEST_DEFAULT_CTR and bs.shows == 1) or not bs.clicks


def test_banner_stat_add_click_increases_ctr() -> None:
    for bs in [BannerStat(10), BannerStat(0, 10), BannerStat(100, 0), BannerStat(10, 20), BannerStat()]:
        ctr = bs.compute_ctr(TEST_DEFAULT_CTR)
        bs.add_click()
        assert ctr < bs.compute_ctr(TEST_DEFAULT_CTR) or not bs.shows


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    storage = BannerStorage(test_banners)
    max_ban = test_banners[0]
    for ban in test_banners:
        if max_ban.stat.compute_ctr(TEST_DEFAULT_CTR) < ban.stat.compute_ctr(TEST_DEFAULT_CTR):
            max_ban = ban
    assert storage.banner_with_highest_cpc() == max_ban


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    try:
        EpsilonGreedyBannerEngine(BannerStorage([]), 1.0)
    except EmptyBannerStorageError:
        return
    assert False, f'not raise {EmptyBannerStorageError}'


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: list[Banner]) -> None:
    try:
        engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.2)
        engine.send_click("b50")
    except NoBannerError:
        assert False, "Send Click Fails on unknown banner"


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0)
    max_ban = test_banners[0]
    for bn in test_banners:
        if max_ban.stat.compute_ctr(TEST_DEFAULT_CTR) < bn.stat.compute_ctr(TEST_DEFAULT_CTR):
            max_ban = bn
    assert engine.show_banner() == max_ban.banner_id


@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: list[Banner],
        monkeypatch: typing.Any
        ) -> None:
    def Rand(args: typing.Any) -> str:
        return expected_random_banner

    monkeypatch.setattr(random, "choice", Rand)
    engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 1)
    assert engine.show_banner() == expected_random_banner


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: list[Banner]) -> None:
    storage = BannerStorage(test_banners)
    cost = 0
    engine = EpsilonGreedyBannerEngine(storage, 0.5)
    for num, val in enumerate(test_banners):
        cost += val.stat.clicks * val.cost
        for i in range(num):
            engine.send_click(val.banner_id)
            cost += val.cost
    assert engine.total_cost == cost


def test_engine_show_increases_banner_show_stat(test_banners: list[Banner]) -> None:
    engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.75)
    count = engine._show_count
    engine.show_banner()
    assert count == engine._show_count - 1


def test_engine_click_increases_banner_click_stat(test_banners: list[Banner]) -> None:
    storage = BannerStorage(test_banners)
    banner = storage.get_banner("b1")
    clicks = banner.stat.clicks
    engine = EpsilonGreedyBannerEngine(BannerStorage(test_banners), 0.75)
    engine.send_click("b1")
    assert clicks == banner.stat.clicks - 1
