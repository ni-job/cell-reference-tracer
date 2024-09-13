import os
import tempfile as tmpf
import streamlit as st
from streamlit.navigation.page import StreamlitPage
from streamlit.runtime.uploaded_file_manager import UploadedFile

from backend.controller.cell_trace_controller import CellTraceController


class ExcelSelectPage:
    """
    Excelファイルを選択するページ
    """

    def __init__(self, controller: CellTraceController) -> None:
        self.__cell_trace_controller: CellTraceController = controller

    def page(self) -> StreamlitPage:
        """
        Excelファイルを選択するページを取得する
        """

        return st.Page(self.__layout, title="Excelファイル選択")

    def __layout(self):
        st.write("Excelのセル参照元をたどってグラフにします")

        self.__uploaded_excel_file: UploadedFile | None = st.file_uploader(
            label="Excelファイルを選択してください",
            type=["xlsx", "xlsm", "xls"]
        )

        if st.button(
            label="OK",
            disabled=self.__uploaded_excel_file is None
        ):
            print("click")
            self.__upload_file()

    def __upload_file(self):
        if self.__uploaded_excel_file is not None:
            path = self.__file_path()
            self.__cell_trace_controller.load_excel(path)
        else:
            raise Exception("Excelファイルが選択されていません")

    def __file_path(self) -> str:
        tmp_dir: str = tmpf.mkdtemp()
        path: str = os.path.join(tmp_dir, self.__uploaded_excel_file.name)

        with open(path, "wb") as f:
            f.write(self.__uploaded_excel_file.getvalue())

        return path
