import openpyxl as opxl


class ExcelHandler:
    """
    Excelを扱うハンドラー
    """

    def __init__(self) -> None:
        pass

    def load(self, path: str) -> None:
        """
        Excelファイルをロードする

        params:
            path: Excelファイルのパス
        """

        self.__path: str = path
        self.__wb: opxl.Workbook = opxl.load_workbook(self.__path)
    
    def sheet_names(self) -> list[str]:
        """
        Excelファイルのシート名一覧を取得する
        """

        return self.__wb.sheetnames
