from backend.controller.cell_trace_controller import CellTraceController
from tests.unit.helper.graph_helper import init_digraph


def test_single_ref_doll_cell():
    """
    深さ1の$つき参照が1つだけのセルのグラフを作成できることのテスト
    """

    # Arrenge
    expected_graph = init_digraph()
    expected_graph.node(
        name="Sheet1!B6",
        label="{Sheet1!B6|=$B$2}"
    )
    expected_graph.node(
        name="Sheet1!B2",
        label="{Sheet1!B2|16}"
    )
    expected_graph.edge(
        tail_name="Sheet1!B6",
        head_name="Sheet1!B2"
    )

    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    actual_graph = controller.graph(
        sheet_name="Sheet1",
        row=6,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    # Assert
    assert actual_graph.body == expected_graph.body
