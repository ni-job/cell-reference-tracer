from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_wb_def_name_cell():
    """
    ワークブックの定義された名前を参照するグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B15",
        label="{Sheet1!B15|=SUM(数列1)}"
    )
    expected_graph.node(
        name="Sheet4!A2A6",
        label="{Sheet4!A2:A6|}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B15",
        head_name="Sheet4!A2A6"
    )
    expected_graph.node(
        name="Sheet4!A2",
        label="{Sheet4!A2|1}"
    )
    expected_graph.edge(
        tail_name="Sheet4!A2A6",
        head_name="Sheet4!A2"
    )
    expected_graph.node(
        name="Sheet4!A3",
        label="{Sheet4!A3|3}"
    )
    expected_graph.edge(
        tail_name="Sheet4!A2A6",
        head_name="Sheet4!A3"
    )
    expected_graph.node(
        name="Sheet4!A4",
        label="{Sheet4!A4|5}"
    )
    expected_graph.edge(
        tail_name="Sheet4!A2A6",
        head_name="Sheet4!A4"
    )
    expected_graph.node(
        name="Sheet4!A5",
        label="{Sheet4!A5|7}"
    )
    expected_graph.edge(
        tail_name="Sheet4!A2A6",
        head_name="Sheet4!A5"
    )
    expected_graph.node(
        name="Sheet4!A6",
        label="{Sheet4!A6|9}"
    )
    expected_graph.edge(
        tail_name="Sheet4!A2A6",
        head_name="Sheet4!A6"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=15,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # bodyの順序が変わってもグラフの構造は変わらない
    actual_graph.body = sorted(actual_graph.body)
    expected_graph.body = sorted(expected_graph.body)

    # Assert
    assert actual_graph.body == expected_graph.body
