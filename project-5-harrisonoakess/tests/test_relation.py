# type: ignore
import pytest
from project5.relation import IncompatibleOperandError, Relation


def test_relation_intersection():
    # given
    header1 = ("a", "b", "c")
    set1 = set([("1", "2", "3"), ("1", "3", "5")])
    relation1 = Relation(header1, set1)
    set2 = set([("1", "2", "4"), ("1", "3", "5")])
    relation2 = Relation(header1, set2)

    # when
    relation1 = relation1.intersection(relation2)

    # then
    relation3 = Relation(header1, set([("1", "3", "5")]))
    assert relation1 == relation3


def test_relation_project():
    # given
    header1 = ("a", "b", "c")
    set1 = set([("1", "2", "3"), ("1", "3", "5")])
    relation1 = Relation(header1, set1)
    to = ["b", "a"]
    # when
    relation1 = relation1.project(to)

    # then
    answer_relation = Relation(("b", "a"), set([("2", "1"), ("3", "1")]))
    assert relation1 == answer_relation


def test_relation_rename():
    # given
    header = ["header1", "header2"]
    relation = Relation(header, set())
    header2 = ["head1", "head2"]

    # when
    relation = relation.rename(header2)

    # then
    assert relation.header == header2


def test_relation_select_eq_col():
    # given
    header1 = ("a", "b", "c")
    src = "a"
    col = "b"
    set1 = set([("1", "1", "3"), ("1", "3", "5")])

    relation1 = Relation(header1, set1)

    # when
    relation1 = relation1.select_eq_col(src, col)

    # then
    new_tuples = set([("1", "1", "3")])
    assert relation1 == Relation(header1, new_tuples)


def test_relation_select_eq_lit():
    # given
    header1 = ("a", "b", "c")
    src = "a"
    lit = "1"
    set1 = set([("1", "1", "3"), ("2", "3", "5")])

    relation1 = Relation(header1, set1)

    # when
    relation1 = relation1.select_eq_lit(src, lit)

    # then
    new_tuples = set([("1", "1", "3")])
    assert relation1 == Relation(header1, new_tuples)


def test_relation_union():
    # given
    header1 = ("a", "b", "c")
    set1 = set([("1", "2", "3"), ("1", "3", "5")])
    relation1 = Relation(header1, set1)
    set2 = set([("1", "2", "4"), ("1", "3", "5")])
    relation2 = Relation(header1, set2)

    # when
    relation1 = relation1.union(relation2)

    # then
    relation3 = Relation(
        header1, set([("1", "2", "3"), ("1", "3", "5"), ("1", "2", "4")])
    )
    assert relation1 == relation3


def test_relation_join_natural_join_one():
    # given
    join_pos_header1 = ("a", "b", "c")
    join_pos_set1 = set([("1", "2", "3"), ("1", "3", "5")])
    join_pos_relation1 = Relation(join_pos_header1, join_pos_set1)

    join_pos_header2 = ("c", "d")
    join_pos_set2 = set([("3", "4"), ("1", "3")])
    join_pos_relation2 = Relation(join_pos_header2, join_pos_set2)

    join_pos_all_headers = ("a", "b", "c", "d")
    join_pos_all_tuples = set([("1", "2", "3", "4")])
    join_pos_true_relation = Relation(join_pos_all_headers, join_pos_all_tuples)

    # when
    join_pos_relation1 = join_pos_relation1.join(join_pos_relation2)

    # then
    assert join_pos_true_relation == join_pos_relation1


def test_relation_join_natural_join_equal_headers():
    # given
    join_pos_header1 = ("a", "b")
    join_pos_set1 = set([("a", "1"), ("b", "2")])
    join_pos_relation1 = Relation(join_pos_header1, join_pos_set1)

    join_pos_header2 = ("a", "b")
    join_pos_set2 = set([("a", "1"), ("c", "5"), ("c", "6")])
    join_pos_relation2 = Relation(join_pos_header2, join_pos_set2)

    join_pos_all_headers = ("a", "b")
    join_pos_all_tuples = set([("a", "1")])
    join_pos_true_relation = Relation(join_pos_all_headers, join_pos_all_tuples)

    # when
    join_pos_relation1 = join_pos_relation1.join(join_pos_relation2)

    # then
    assert join_pos_true_relation == join_pos_relation1


def test_relation_join_natural_join_no_headers():
    # given
    join_pos_header1 = ("a", "b")
    join_pos_set1 = set([("a", "1"), ("b", "2")])
    join_pos_relation1 = Relation(join_pos_header1, join_pos_set1)

    join_pos_header2 = ("c", "d")
    join_pos_set2 = set([("a", "1"), ("c", "5"), ("c", "6")])
    join_pos_relation2 = Relation(join_pos_header2, join_pos_set2)

    join_pos_all_headers = ("a", "b", "c", "d")
    join_pos_all_tuples = set(
        [
            ("a", "1", "a", "1"),
            ("a", "1", "c", "5"),
            ("a", "1", "c", "6"),
            ("b", "2", "a", "1"),
            ("b", "2", "c", "5"),
            ("b", "2", "c", "6"),
        ]
    )
    join_pos_true_relation = Relation(join_pos_all_headers, join_pos_all_tuples)

    # when
    join_pos_relation1 = join_pos_relation1.join(join_pos_relation2)

    # then
    assert join_pos_true_relation == join_pos_relation1


def test_relation_join_natural_join_empty():
    # given
    join_pos_header1 = ("a", "b")
    join_pos_set1 = set([("a", "1"), ("b", "2")])
    join_pos_relation1 = Relation(join_pos_header1, join_pos_set1)

    join_pos_header2 = ()
    join_pos_set2 = set([])
    join_pos_relation2 = Relation(join_pos_header2, join_pos_set2)

    join_pos_all_headers = ()
    join_pos_all_tuples = set([])
    join_pos_true_relation = Relation(join_pos_all_headers, join_pos_all_tuples)

    # when
    join_pos_relation1 = join_pos_relation1.join(join_pos_relation2)

    # then
    assert join_pos_true_relation == join_pos_relation1


def test_given_empty_relation_when_add_tuple_then_tuple_in_relation():
    # given
    header = ("a", "b", "c")
    relation = Relation(header, set())
    input = ("'1'", "'2'", "'3'")

    # when
    relation.add_tuple(input)

    # then
    assert 1 == len(relation.set_of_tuples)
    assert input in relation.set_of_tuples


def test_given_relation_when_str_then_match_expected():
    # given
    header = ("a", "b", "c")
    set_of_tuples = set([("'1'", "'2'", "'3'"), ("'1'", "'3'", "'5'")])
    relation = Relation(header, set_of_tuples)

    expected = """+-----+-----+-----+
|  a  |  b  |  c  |
+-----+-----+-----+
| '1' | '2' | '3' |
| '1' | '3' | '5' |
+-----+-----+-----+"""

    # when
    answer = str(relation)

    # then
    assert expected == answer


def test_given_relation_and_wrong_size_when_add_tuple_then_exception():
    # given
    relation = Relation(("a", "b", "c"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        relation.add_tuple(("1", "2"))

    # then
    assert (
        "Error: ('1', '2') is not compatible with header ['a', 'b', 'c'] in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_relation_when_add_tuple_then_added():
    # given
    relation = Relation(("a", "b", "c"), set())

    # when
    relation.add_tuple(("1", "2", "3"))

    # then
    assert ("1", "2", "3") in relation.set_of_tuples


def test_given_mismatched_header_and_tuple_when_construct_then_exception():
    # given
    header = ("a", "b", "c")
    set_of_tuples = set([("1", "2")])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: ('1', '2') is not compatible with header ['a', 'b', 'c'] in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_set_that_is_not_over_tuples_when_construct_then_exception():
    # given
    header = "a"
    set_of_tuples = set(["1"])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: 1 is not type compatible with Relation.RelationTuple in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_set_that_is_tuples_but_not_str_when_construct_then_exception():
    # given
    header = ("a", "b")
    set_of_tuples = set([("1", 2)])

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        _ = Relation(header, set_of_tuples)

    # then
    assert (
        "Error: ('1', 2) is not type compatible with Relation.RelationTuple in Relation.add_tuple"
        == str(exception.value)
    )


def test_given_mismatched_relations_when_difference_then_exception():
    # given
    left = Relation(("a", "b", "c"), set())
    right = Relation(("a", "b"), set())

    # when
    with pytest.raises(IncompatibleOperandError) as exception:
        left.difference(right)

    # then
    assert (
        "Error: headers ['a', 'b', 'c'] and ['a', 'b'] are not compatible in Relation.difference"
        == str(exception.value)
    )


def test_given_matched_relations_when_difference_then_difference():
    # given
    left = Relation(("a", "b", "c"), set([("1", "2", "3"), ("2", "4", "6")]))
    right = Relation(("a", "b", "c"), set([("2", "4", "6")]))
    expected = Relation(("a", "b", "c"), set([("1", "2", "3")]))

    # when
    answer = left.difference(right)

    # then
    assert expected == answer
