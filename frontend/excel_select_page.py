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

        return st.Page(
            self.__layout,
            title="Excelファイル選択",
            url_path="excel-select"
        )

    def __layout(self):
        # 開発者向けオプションを非表示
        st.markdown("""
            <style>
                .reportview-container {
                    margin-top: -2em;
                }
                #MainMenu {visibility: hidden;}
                .stAppDeployButton {display:none;}
                footer {visibility: hidden;}
                #stDecoration {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.write("Excelのセル参照元をたどってグラフにします")

        st.file_uploader(
            label="Excelファイルを選択してください",
            type=["xlsx", "xlsm", "xls"],
            key="uploaded_excel_file"
        )

        if st.button(
            label="OK",
            disabled=st.session_state.uploaded_excel_file is None
        ):
            if st.session_state.uploaded_excel_file is not None:
                self.__cell_trace_controller.upload_excel(st.session_state.uploaded_excel_file)
                st.switch_page(st.session_state.trace_output_page)
            else:
                raise Exception("Excelファイルが選択されていません")
