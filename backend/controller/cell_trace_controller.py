from backend.handler.excel_handler import ExcelHandler


class CellTraceController:
    """
    Excelのセル参照元をグラフにするユースケースのコントローラー
    """

    def __init__(self) -> None:
        self.__excel_handler: ExcelHandler = ExcelHandler()

    def load_excel(self, path: str) -> None:
        """
        Excelファイルを読み込む

        params:
            path: Excelファイルのパス
        """
        self.__excel_handler.load(path)
