from src.pyfs import copy, remove, move
from src.pyfs import load_yaml_full, load_yaml_safe, dump_yaml
from src.pyfs import load_json, dump_json
from src.pyfs import (
    logger_file_info,
    logger_section,
    logger_table_begin,
    logger_table_end,
)

import os


def test_clear():
    logger_section("start test_clear")
    # clear
    remove("./build")
    assert not os.path.exists("./build")


def test_copy_remove():
    logger_section("start test_copy_remove")
    # test copytree ignore
    copy(
        "./test/data_1",
        "./build/data_1_copytree_ignore",
        mode="ignore",
        patterns=["*.txt"],
        dirs_exist_ok=True,
    )
    assert os.path.exists("./build/data_1_copytree_ignore")
    assert os.path.exists("./build/data_1_copytree_ignore/test.md")
    assert not os.path.exists("./build/data_1_copytree_ignore/test.txt")

    # test copytree include
    copy(
        "./test/data_1",
        "./build/data_1_copytree_include",
        mode="include",
        patterns=["*.txt"],
        dirs_exist_ok=True,
    )
    assert os.path.exists("./build/data_1_copytree_include")
    assert not os.path.exists("./build/data_1_copytree_include/test.md")
    assert os.path.exists("./build/data_1_copytree_include/test.txt")

    # test remove
    remove("./build/data_1_copytree_to_be_remove")
    assert not os.path.exists("./build/data_1_copytree_to_be_remove/test.md")

    copy("./test/data_1", "./build/data_1_copytree_to_be_remove", dirs_exist_ok=False)
    remove("./build/data_1_copytree_to_be_remove/test.md")
    assert not os.path.exists("./build/data_1_copytree_to_be_remove/test.md")
    assert os.path.exists("./build/data_1_copytree_to_be_remove/test.txt")

    # test remove with incldue mode
    copy("./test/data_1", "./build/data_1_copytree_to_be_remove_2", dirs_exist_ok=False)
    remove("./build/data_1_copytree_to_be_remove_2", mode="include", patterns=["*.md"])
    assert not os.path.exists("./build/data_1_copytree_to_be_remove_2/test.md")
    assert os.path.exists("./build/data_1_copytree_to_be_remove_2/test.txt")

    # test remove with ignore mode
    remove("./build/data_1_copytree_to_be_remove_2", mode="ignore", patterns=["*.md"])
    assert not os.path.exists("./build/data_1_copytree_to_be_remove_2/test.txt")


def test_move():
    logger_section("start test_move")
    # test copytree
    copy("./test/data_1", "./build/data_1_move_source_0")
    copy("./test/data_1", "./build/data_1_move_source_1")
    copy("./test/data_1", "./build/data_1_move_source_2")

    # test move file and dir
    # remove("./build/data_1_move")

    move(
        "./build/data_1_move_source_0/sub_1/test.md",
        "./build/data_1_move/sub_1/test.md",
    )
    assert os.path.exists("./build/data_1_move/sub_1/test.md")
    assert not os.path.exists("./build/data_1_move_source_0/sub_1/test.md")

    move("./build/data_1_move_source_0/sub_2", "./build/data_1_move/sub_2")
    assert os.path.exists("./build/data_1_move/sub_2")
    assert os.path.exists("./build/data_1_move/sub_2/test.txt")
    assert os.path.exists("./build/data_1_move/sub_2/test.md")

    assert not os.path.exists("./build/data_1_move_source_0/sub_2")
    assert not os.path.exists("./build/data_1_move_source_0/sub_2/test.txt")
    assert not os.path.exists("./build/data_1_move_source_0/sub_2/test.md")

    # test move tree ignore
    # remove("./build/data_1_move_ignore")
    move(
        "./build/data_1_move_source_1",
        "./build/data_1_move_ignore",
        mode="ignore",
        patterns=["*.txt"],
    )
    assert os.path.exists("./build/data_1_move_ignore")

    assert os.path.exists("./build/data_1_move_ignore/test.md")
    assert not os.path.exists("./build/data_1_move_source_1/test.md")

    assert not os.path.exists("./build/data_1_move_ignore/test.txt")
    assert os.path.exists("./build/data_1_move_source_1/test.txt")

    assert os.path.exists("./build/data_1_move_ignore/sub_1/test.md")
    assert not os.path.exists("./build/data_1_move_source_1/sub_1/test.md")

    assert not os.path.exists("./build/data_1_move_ignore/sub_1/test.txt")
    assert os.path.exists("./build/data_1_move_source_1/sub_1/test.txt")

    # test move tree include
    # remove("./build/data_1_move_include")
    move(
        "./build/data_1_move_source_2",
        "./build/data_1_move_include",
        mode="include",
        patterns=["*.txt"],
    )

    assert os.path.exists("./build/data_1_move_include/test.txt")
    assert not os.path.exists("./build/data_1_move_source_2/test.txt")

    assert not os.path.exists("./build/data_1_move_include/test.md")
    assert os.path.exists("./build/data_1_move_source_2/test.md")

    assert os.path.exists("./build/data_1_move_include/sub_1/test.txt")
    assert not os.path.exists("./build/data_1_move_source_2/sub_1/test.txt")

    assert not os.path.exists("./build/data_1_move_include/sub_1/test.md")
    assert os.path.exists("./build/data_1_move_source_2/sub_1/test.md")


def test_yaml():
    logger_section("start test_yaml")

    y = load_yaml_full("./test/data_2/yaml/0.yml", "./test/data_2/yaml")
    assert y["name"] == "0"
    assert y["file1"]["name"] == "1"
    assert y["file2"]["name"] == "2"

    dump_yaml(y, "./build/0.full.yml")
    y_full = load_yaml_safe("./build/0.full.yml")
    assert y_full["name"] == "0"
    assert y_full["file1"]["name"] == "1"
    assert y_full["file2"]["name"] == "2"

    y = load_yaml_safe("./test/data_2/yaml/0.yml")
    assert y["name"] == "0"
    assert y["file1"] == None
    assert y["file2"] == None


def test_json():
    logger_section("start test_json")

    j1 = load_json("./test/data_2/json/1.json")
    dump_json(j1, "./build/1.json")

    j2 = load_json("./build/1.json")

    assert j1["key"] == j2["key"]


def test_logger():
    logger_section("start test_logger")

    logger_table_begin("test logger_file_info")
    logger_file_info("./build/1.json")
    logger_table_end()


if __name__ == "__main__":
    test_clear()
    test_copy_remove()
    test_move()
    test_yaml()
    test_json()
    test_logger()
