import pytest


def test_factory_item_not_exist(factory, not_exist_config):
    with pytest.raises(KeyError, match="Scraper"):
        factory(not_exist_config)


def test_create_new_scraper(factory, exist_config_1, exist_config_2, exist_config_3):
    factory(exist_config_1)
    factory(exist_config_2)
    factory(exist_config_3)


def test_is_not_the_same(
    factory, exist_config_1, exist_config_2, exist_config_3, factory_list
):
    scr1 = factory(exist_config_1)
    scr2 = factory(exist_config_2)
    scr3 = factory(exist_config_3)

    assert type(scr1) is factory_list[0]
    assert not type(scr1) is factory_list[1]
    assert not type(scr1) is factory_list[2]

    assert not type(scr2) is factory_list[0]
    assert type(scr2) is factory_list[1]
    assert not type(scr2) is factory_list[2]

    assert not type(scr3) is factory_list[0]
    assert not type(scr3) is factory_list[1]
    assert type(scr3) is factory_list[2]
