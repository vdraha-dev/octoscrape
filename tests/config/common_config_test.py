def test_default_path_to_csv(default_common_config):
    assert str(default_common_config.path_to_csv_dir) == "."


def test_default_max_window_width(default_common_config):
    assert default_common_config.max_window_width == 1920


def test_default_max_window_heigh(default_common_config):
    assert default_common_config.max_window_height == 1080


def test_default_pool_size(default_common_config):
    assert default_common_config.pool_size == 1


def test_default_headless(default_common_config):
    assert default_common_config.headless == False


def test_path_to_csv(common_config, common_config_dict):
    assert str(common_config.path_to_csv_dir) == common_config_dict["path_to_csv"]


def test_max_window_width(common_config, common_config_dict):
    assert common_config.max_window_width == common_config_dict["max_width"]


def test_max_window_heigh(common_config, common_config_dict):
    assert common_config.max_window_height == common_config_dict["max_height"]


def test_pool_size(common_config, common_config_dict):
    assert common_config.pool_size == common_config_dict["pool_size"]


def test_headless(common_config, common_config_dict):
    assert common_config.headless == common_config_dict["headless"]
