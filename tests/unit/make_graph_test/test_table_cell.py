from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_table_cell():
    """
    テーブルを参照するグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B23",
        label="{Sheet1!B23|=SUM(テーブル1[])}"
    )
    expected_graph.node(
        name="Sheet4!E1G4",
        label="{Sheet4!E1:G4|}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B23",
        head_name="Sheet4!E1G4"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=23,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # bodyの順序が変わってもグラフの構造は変わらない
    actual_graph.body = sorted(actual_graph.body)
    expected_graph.body = sorted(expected_graph.body)

    # Assert
    assert actual_graph.body == expected_graph.body
