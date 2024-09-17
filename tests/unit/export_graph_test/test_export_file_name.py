from backend.controller.cell_trace_controller import CellTraceController


def test_export_file_name():
    """
    グラフをSVGでエクスポートしたファイル名が正しいことのテスト
    """
    # Arrenge
    controller = CellTraceController()

    # Act
    with open("tests/files/test.xlsx", "rb") as f:
        controller.upload_excel(f.read(), "test.xlsx")

    controller.graph(
        sheet_name="Sheet1",
        row=1,
        clm=2,
        graph_format="svg",
        max_trace_size=10
    )

    _, acutual_name = controller.export()

    # Assert
    assert acutual_name == "test_Sheet1_1_2.svg"
