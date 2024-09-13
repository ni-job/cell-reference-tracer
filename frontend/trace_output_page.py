import streamlit as st
from streamlit.navigation.page import StreamlitPage

from backend.controller.cell_trace_controller import CellTraceController


class TraceOutputPage:
    """
    シートとセルを選択して、参照元グラフを表示するページ
    """

    def __init__(self, controller: CellTraceController) -> None:
        self.__cell_trace_controller: CellTraceController = controller
        self.__sheet: str = ""
        self.__row: int = 1
        self.__clm: int = 1

    def page(self) -> StreamlitPage:
        """
        ページを取得する
        """

        return st.Page(
            self.__layout,
            title="グラフ表示",
            url_path="trace-output"
        )

    def __layout(self):
        st.write("シートとセルを選択してください")

        input_fld_clms = st.columns(4, vertical_alignment="bottom")

        with input_fld_clms[0]:
            self.__sheet = st.selectbox(
                label="シート",
                options=self.__cell_trace_controller.sheet_names(),

            )

        with input_fld_clms[1]:
            self.__row = st.number_input(
                label="行",
                min_value=1,
                max_value=1048576
            )

        with input_fld_clms[2]:
            self.__clm = st.number_input(
                label="列",
                min_value=1,
                max_value=1048576
            )

        with input_fld_clms[3]:
            st.write(self.__cell_trace_controller.get_column_letter(self.__clm))

        st.button(
            label="グラフを表示"
        )
