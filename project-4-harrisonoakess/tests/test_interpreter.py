# type: ignore
"""Tests for the Datalog interpreter."""

from project4.relation import Relation
from project4.datalogprogram import Parameter, Predicate, DatalogProgram, Rule
from project4.interpreter import Interpreter


def test_eval_schemes():
    # given
    schemeslist = [
        Predicate(
            "snap",
            [
                Parameter("S", "ID"),
                Parameter("N", "ID"),
                Parameter("A", "ID"),
                Parameter("P", "ID"),
            ],
        ),
        Predicate(
            "csg", [Parameter("C", "ID"), Parameter("S", "ID"), Parameter("G", "ID")]
        ),
        Predicate("cn", [Parameter("C", "ID"), Parameter("N", "ID")]),
        Predicate(
            "ncg", [Parameter("N", "ID"), Parameter("C", "ID"), Parameter("G", "ID")]
        ),
    ]
    expected = {
        "snap": Relation(["S", "N", "A", "P"], set()),
        "csg": Relation(["C", "S", "G"], set()),
        "cn": Relation(["C", "N"], set()),
        "ncg": Relation(["N", "C", "G"], set()),
    }

    datalog_program = DatalogProgram(schemes=schemeslist)

    interpreter = Interpreter(datalog_program)

    # when
    interpreter.eval_schemes()

    # then
    assert interpreter.table_list == expected


def test_eval_facts():
    pass
    # given
    schemeslist = [
        Predicate(
            "snap",
            [
                Parameter("S", "ID"),
                Parameter("N", "ID"),
                Parameter("A", "ID"),
                Parameter("P", "ID"),
            ],
        ),
        Predicate(
            "csg", [Parameter("C", "ID"), Parameter("S", "ID"), Parameter("G", "ID")]
        ),
    ]

    factslist = [
        Predicate(
            "snap",
            [
                Parameter("12345", "STRING"),
                Parameter("C. Brown", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("22222", "STRING"),
                Parameter("P. Patty", "STRING"),
                Parameter("56 Grape Blvd", "STRING"),
                Parameter("555-9999", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("33333", "STRING"),
                Parameter("Snoopy", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("A", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("33333", "STRING"),
                Parameter("C", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("B+", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
    ]

    expected = {
        "snap": Relation(
            ["S", "N", "A", "P"],
            {
                ("12345", "C. Brown", "12 Apple St.", "555-1234"),
                ("22222", "P. Patty", "56 Grape Blvd", "555-9999"),
                ("33333", "Snoopy", "12 Apple St.", "555-1234"),
            },
        ),
        "csg": Relation(
            ["C", "S", "G"],
            {
                ("CS101", "12345", "A"),
                ("CS101", "22222", "B"),
                ("CS101", "33333", "C"),
                ("EE200", "12345", "B+"),
                ("EE200", "22222", "B"),
            },
        ),
    }

    datalog_program = DatalogProgram(schemes=schemeslist, facts=factslist)

    interpreter = Interpreter(datalog_program)

    # when
    interpreter.eval_schemes()
    interpreter.eval_facts()
    # then
    assert interpreter.table_list == expected


def test_eval_rules():
    # given
    schemeslist = [
        Predicate(
            "snap",
            [
                Parameter("S", "ID"),
                Parameter("N", "ID"),
                Parameter("A", "ID"),
                Parameter("P", "ID"),
            ],
        ),
        Predicate(
            "csg", [Parameter("C", "ID"), Parameter("S", "ID"), Parameter("G", "ID")]
        ),
        Predicate("cn", [Parameter("C", "ID"), Parameter("N", "ID")]),
        Predicate(
            "ncg", [Parameter("N", "ID"), Parameter("C", "ID"), Parameter("G", "ID")]
        ),
    ]

    factslist = [
        Predicate(
            "snap",
            [
                Parameter("12345", "STRING"),
                Parameter("C. Brown", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("22222", "STRING"),
                Parameter("P. Patty", "STRING"),
                Parameter("56 Grape Blvd", "STRING"),
                Parameter("555-9999", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("33333", "STRING"),
                Parameter("Snoopy", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("A", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("33333", "STRING"),
                Parameter("C", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("B+", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
    ]

    ruleslist = [
        Rule(
            Predicate("cn", [Parameter("c", "ID"), Parameter("n", "ID")]),
            [
                Predicate(
                    "snap",
                    [
                        Parameter("S", "ID"),
                        Parameter("n", "ID"),
                        Parameter("A", "ID"),
                        Parameter("P", "ID"),
                    ],
                ),
                Predicate(
                    "csg",
                    [Parameter("c", "ID"), Parameter("S", "ID"), Parameter("G", "ID")],
                ),
            ],
        ),
        # Rule(
        #     Predicate(
        #         "ncg",
        #         [Parameter("n", "ID"), Parameter("c", "ID"), Parameter("g", "ID")],
        #     ),
        #     [
        #         Predicate(
        #             "snap",
        #             [
        #                 Parameter("S", "ID"),
        #                 Parameter("n", "ID"),
        #                 Parameter("A", "ID"),
        #                 Parameter("P", "ID"),
        #             ],
        #         ),
        #         Predicate(
        #             "csg",
        #             [Parameter("c", "ID"), Parameter("S", "ID"), Parameter("G", "ID")],
        #         ),
        #     ],
        # ),
    ]

    expected = [
        Relation(
            [
                "C",
                "N",
            ],
            set(
                [
                    ("CS101", "C. Brown"),
                    ("CS101", "Snoopy"),
                    ("EE200", "P. Patty"),
                    ("CS101", "P. Patty"),
                    ("EE200", "C. Brown"),
                ]
            ),
        )
    ]

    datalog_program = DatalogProgram(
        schemes=schemeslist, facts=factslist, rules=ruleslist
    )
    interpreter = Interpreter(datalog_program)

    # when
    interpreter.eval_schemes()
    interpreter.eval_facts()
    final_list = interpreter.eval_rules()

    # then
    for i, expect in zip(final_list, expected):
        assert i[2] == expect
    # assert final_list[0][2] == expected[0] # this probably has a problem


def test_eval_queries():
    # given
    schemeslist = [
        Predicate(
            "snap",
            [
                Parameter("S", "ID"),
                Parameter("N", "ID"),
                Parameter("A", "ID"),
                Parameter("P", "ID"),
            ],
        ),
        Predicate(
            "csg", [Parameter("C", "ID"), Parameter("S", "ID"), Parameter("G", "ID")]
        ),
        Predicate("cn", [Parameter("C", "ID"), Parameter("N", "ID")]),
        Predicate(
            "ncg", [Parameter("N", "ID"), Parameter("C", "ID"), Parameter("G", "ID")]
        ),
    ]

    factslist = [
        Predicate(
            "snap",
            [
                Parameter("12345", "STRING"),
                Parameter("C. Brown", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("22222", "STRING"),
                Parameter("P. Patty", "STRING"),
                Parameter("56 Grape Blvd", "STRING"),
                Parameter("555-9999", "STRING"),
            ],
        ),
        Predicate(
            "snap",
            [
                Parameter("33333", "STRING"),
                Parameter("Snoopy", "STRING"),
                Parameter("12 Apple St.", "STRING"),
                Parameter("555-1234", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("A", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("CS101", "STRING"),
                Parameter("33333", "STRING"),
                Parameter("C", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("12345", "STRING"),
                Parameter("B+", "STRING"),
            ],
        ),
        Predicate(
            "csg",
            [
                Parameter("EE200", "STRING"),
                Parameter("22222", "STRING"),
                Parameter("B", "STRING"),
            ],
        ),
    ]

    querieslist = [
        Predicate("cn", [Parameter("CS101", "STRING"), Parameter("Name", "ID")]),
        Predicate(
            "ncg",
            [
                Parameter("Snoopy", "STRING"),
                Parameter("Course", "ID"),
                Parameter("Grade", "ID"),
            ],
        ),
    ]

    expected = [
        (
            querieslist[0],
            Relation(
                ["Name"],
                {},
            ),
        ),
        (querieslist[1], Relation(["Course", "Grade"], {})),
    ]

    datalog_program = DatalogProgram(
        schemes=schemeslist, facts=factslist, queries=querieslist
    )
    interpreter = Interpreter(datalog_program)

    # when
    interpreter.eval_schemes()
    interpreter.eval_facts()
    interpreter.eval_rules()
    actual = list(interpreter.eval_queries())

    # then
    assert actual == expected
