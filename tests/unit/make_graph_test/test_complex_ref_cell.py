from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_complex_ref_cell():
    """
    複雑な参照セルのグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B12",
        label="{Sheet1!B12|=IF(C1=1,\"\",SUM(C1:C5))}"
    )
    expected_graph.node(
        name="Sheet1!C1",
        label="{Sheet1!C1|1}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B12",
        head_name="Sheet1!C1"
    )
    expected_graph.node(
        name="Sheet1!C1C5",
        label="{Sheet1!C1:C5|}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B12",
        head_name="Sheet1!C1C5"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C5",
        head_name="Sheet1!C1"
    )
    expected_graph.node(
        name="Sheet1!C2",
        label="{Sheet1!C2|2}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C5",
        head_name="Sheet1!C2"
    )
    expected_graph.node(
        name="Sheet1!C3",
        label="{Sheet1!C3|3}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C5",
        head_name="Sheet1!C3"
    )
    expected_graph.node(
        name="Sheet1!C4",
        label="{Sheet1!C4|4}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C5",
        head_name="Sheet1!C4"
    )
    expected_graph.node(
        name="Sheet1!C5",
        label="{Sheet1!C5|5}"
    )
    expected_graph.edge(
        tail_name="Sheet1!C1C5",
        head_name="Sheet1!C5"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=12,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # bodyの順序が変わってもグラフの構造は変わらない
    actual_graph.body = sorted(actual_graph.body)
    expected_graph.body = sorted(expected_graph.body)

    # Assert
    assert actual_graph.body == expected_graph.body
