from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_ws_def_name_cell():
    """
    ワークシートの定義された名前を参照するグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B16",
        label="{Sheet1!B16|=Sheet4!C1}"
    )
    expected_graph.node(
        name="Sheet4!C1",
        label="{Sheet4!C1|=AVERAGE(数列２)}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B16",
        head_name="Sheet4!C1"
    )
    expected_graph.node(
        name="Sheet4!B2B6",
        label="{Sheet4!B2:B6|}"
    )
    expected_graph.edge(
        tail_name="Sheet4!C1",
        head_name="Sheet4!B2B6"
    )
    expected_graph.node(
        name="Sheet4!B2",
        label="{Sheet4!B2|2}"
    )
    expected_graph.edge(
        tail_name="Sheet4!B2B6",
        head_name="Sheet4!B2"
    )
    expected_graph.node(
        name="Sheet4!B3",
        label="{Sheet4!B3|4}"
    )
    expected_graph.edge(
        tail_name="Sheet4!B2B6",
        head_name="Sheet4!B3"
    )
    expected_graph.node(
        name="Sheet4!B4",
        label="{Sheet4!B4|6}"
    )
    expected_graph.edge(
        tail_name="Sheet4!B2B6",
        head_name="Sheet4!B4"
    )
    expected_graph.node(
        name="Sheet4!B5",
        label="{Sheet4!B5|8}"
    )
    expected_graph.edge(
        tail_name="Sheet4!B2B6",
        head_name="Sheet4!B5"
    )
    expected_graph.node(
        name="Sheet4!B6",
        label="{Sheet4!B6|10}"
    )
    expected_graph.edge(
        tail_name="Sheet4!B2B6",
        head_name="Sheet4!B6"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=16,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # bodyの順序が変わってもグラフの構造は変わらない
    actual_graph.body = sorted(actual_graph.body)
    expected_graph.body = sorted(expected_graph.body)

    # Assert
    assert actual_graph.body == expected_graph.body
