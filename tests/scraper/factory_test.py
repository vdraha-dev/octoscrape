import pytest

def test_factory_item_not_exist(factory):
    with pytest.raises(KeyError, match="Scraper"):
        factory("not_exist_label")


def test_create_new_scraper(factory, scraper_config):
    factory("label1", scraper_config)


def test_is_not_the_same(factory, scraper_config, factory_dict):
    scr1 = factory("label1", scraper_config)
    scr2 = factory("label2", scraper_config)
    scr3 = factory("label3", scraper_config)

    assert type(scr1) is factory_dict["label1"]
    assert not type(scr1) is factory_dict["label2"]
    assert not type(scr1) is factory_dict["label3"]

    assert not type(scr2) is factory_dict["label1"]
    assert type(scr2) is factory_dict["label2"]
    assert not type(scr2) is factory_dict["label3"]

    assert not type(scr3) is factory_dict["label1"]
    assert not type(scr3) is factory_dict["label2"]
    assert type(scr3) is factory_dict["label3"]