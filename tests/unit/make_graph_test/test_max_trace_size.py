import pytest

from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph

def pack_graph():
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B9",
        label="{Sheet1!B9|=AVERAGE(C1:C10)}"
    )
    expected_graph.node(
        name="Sheet1!C1C10",
        label="{Sheet1!C1:C10|}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B9",
        head_name="Sheet1!C1C10"
    )

    return expected_graph

def unpack_graph():
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B9",
        label="{Sheet1!B9|=AVERAGE(C1:C10)}"
    )
    expected_graph.node(
        name="Sheet1!C1C10",
        label="{Sheet1!C1:C10|}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B9",
        head_name="Sheet1!C1C10"
    )
    expected_graph.node(
        name="Sheet1!C1",
        label="{Sheet1!C1|1}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C1"
    )
    expected_graph.node(
        name="Sheet1!C2",
        label="{Sheet1!C2|2}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C2"
    )
    expected_graph.node(
        name="Sheet1!C3",
        label="{Sheet1!C3|3}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C3"
    )
    expected_graph.node(
        name="Sheet1!C4",
        label="{Sheet1!C4|4}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C4"
    )
    expected_graph.node(
        name="Sheet1!C5",
        label="{Sheet1!C5|5}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C5"
    )
    expected_graph.node(
        name="Sheet1!C6",
        label="{Sheet1!C6|6}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C6"
    )
    expected_graph.node(
        name="Sheet1!C7",
        label="{Sheet1!C7|7}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C7"
    )
    expected_graph.node(
        name="Sheet1!C8",
        label="{Sheet1!C8|8}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C8"
    )
    expected_graph.node(
        name="Sheet1!C9",
        label="{Sheet1!C9|9}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C9"
    )
    expected_graph.node(
        name="Sheet1!C10",
        label="{Sheet1!C10|10}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C10",
        head_name="Sheet1!C10"
    )

    return expected_graph


@pytest.mark.parametrize(
        "max_trace_size, expected_graph",
        [
            (9, pack_graph()),
            (10, unpack_graph())
        ]
)
def test_max_trace_size(max_trace_size, expected_graph):
    """
    max_trace_size以下の場合、範囲セルを展開することのテスト
    max_trace_sizeより大きい場合、範囲セルを展開しないことのテスト
    """

    # Arrenge
    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=9,
        clm=2,
        graph_format="svg",
        max_trace_size=max_trace_size
    )

    # bodyの順序が変わってもグラフの構造は変わらない
    actual_graph.body = sorted(actual_graph.body)
    expected_graph.body = sorted(expected_graph.body)

    # Assert
    assert actual_graph.body == expected_graph.body
