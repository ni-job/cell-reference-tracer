import os
import tempfile as tmpf
from streamlit.runtime.uploaded_file_manager import UploadedFile

from backend.handler.excel_handler import ExcelHandler


class CellTraceController:
    """
    Excelのセル参照元をグラフにするユースケースのコントローラー
    """

    def __init__(self) -> None:
        self.__excel_handler: ExcelHandler = ExcelHandler()

    def upload_excel(self, file_obj: UploadedFile) -> None:
        """
        Excelファイルを読み込む

        params:
            file_obj: Excelファイルのバイナリデータ
        """

        path = self.__file_path(file_obj)
        self.__load_excel(path)

    def __file_path(self, file_obj: UploadedFile) -> str:
        tmp_dir: str = tmpf.mkdtemp()
        path: str = os.path.join(tmp_dir, file_obj.name)

        with open(path, "wb") as f:
            f.write(file_obj.getvalue())

        return path

    def __load_excel(self, path: str) -> None:
        self.__excel_handler.load(path)
