import openpyxl as opxl


class ExcelHandler:
    """
    Excelを扱うハンドラー
    """

    def __init__(self, path: str) -> None:
        self.__wb: opxl.Workbook = opxl.load_workbook(path)

    def sheet_names(self) -> list[str]:
        """
        Excelファイルのシート名一覧を取得する
        """

        return self.__wb.sheetnames

    def get_column_letter(self, num: int) -> str:
        """
        列番号をアルファベットに変換する
        """
        return opxl.utils.get_column_letter(num)
