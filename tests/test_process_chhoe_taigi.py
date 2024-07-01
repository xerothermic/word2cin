
from word2cin.cin_entry import CinEntry
from word2cin.processors.process_chhoe_taigi import dedup_cin_list


def test_dedup_cin_list():
    # identical entries should collapse
    cin_list = [
        CinEntry(
            "key",
            "value",
            "src_name",
            "src_col",
            "parse_method",
            0.0,
            "comment"
        ),
        CinEntry(
            "key",
            "value",
            "src_name",
            "src_col",
            "parse_method",
            0.0,
            "comment"
        ),
    ]
    new_cin_list = dedup_cin_list(cin_list)
    assert len(new_cin_list) == 1
    assert new_cin_list[0] == cin_list[0]
    # same key and value should collapse, but the metadata should concat with
    # ";", weight should be sum'ed
    cin_list = [
        CinEntry(
            "key",
            "value",
            "src_name1",
            "src_col1",
            "parse_method1",
            4.0,
            "comment1"
        ),
        CinEntry(
            "key",
            "value",
            "src_name2",
            "src_col2",
            "parse_method2",
            7.0,
            "comment2"
        ),
    ]
    expected_cin = CinEntry(
        "key",
        "value",
        "src_name1;src_name2",
        "src_col1;src_col2",
        "parse_method1;parse_method2",
        11.0,
        "comment1;comment2"
    )
    new_cin_list = dedup_cin_list(cin_list)
    assert len(new_cin_list) == 1
    assert new_cin_list[0] != cin_list[0]
    assert new_cin_list[0] == expected_cin
