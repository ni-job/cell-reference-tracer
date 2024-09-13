import os
import tempfile as tmpf
from streamlit.runtime.uploaded_file_manager import UploadedFile

from backend.handler.excel_handler import ExcelHandler


class CellTraceController:
    """
    Excelのセル参照元をグラフにするユースケースのコントローラー
    """

    def __init__(self) -> None:
        self.__excel_handler: ExcelHandler

    def upload_excel(self, file_obj: UploadedFile) -> None:
        """
        Excelファイルを読み込む

        params:
            file_obj: Excelファイルのバイナリデータ
        """

        path = self.__file_path(file_obj)
        self.__excel_handler = ExcelHandler(path)

    def __file_path(self, file_obj: UploadedFile) -> str:
        tmp_dir: str = tmpf.mkdtemp()
        path: str = os.path.join(tmp_dir, file_obj.name)

        with open(path, "wb") as f:
            f.write(file_obj.getvalue())

        return path

    def sheet_names(self) -> list[str]:
        """
        Excelファイルのシート名一覧を取得する
        """

        return self.__excel_handler.sheet_names()

    def get_column_letter(self, num:int) -> str:
        """
        列番号をアルファベットに変換する
        """

        return self.__excel_handler.get_column_letter(num)
