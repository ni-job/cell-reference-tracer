from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_literal_formula_cell():
    """
    数値だけの式のセルのグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B3",
        label="{Sheet1!B3|=1}"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=3,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # Assert
    assert actual_graph.body == expected_graph.body
