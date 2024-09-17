from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_func_formula_cell():
    """
    関数式のセルのグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B4",
        label="{Sheet1!B4|=NOW()}"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=4,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # Assert
    assert actual_graph.body == expected_graph.body
