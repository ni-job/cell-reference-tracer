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
        header_clms = st.columns(
            [1, 4, 1],
            vertical_alignment="bottom"
        )

        with header_clms[0]:
            st.page_link(
                page=st.session_state.excel_select_page,
                label="< 戻る"
            )

        with header_clms[-1]:
            with st.popover(label="設定"):
                st.write("test")

        input_fld_clms = st.columns(
            [6, 3, 3, 1],
            vertical_alignment="bottom"
        )

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
                max_value=16384
            )

        with input_fld_clms[3]:
            st.write("= " + self.__cell_trace_controller.get_column_letter(self.__clm))

        with st.spinner("作成中..."):
            if st.button(label="グラフを表示"):
                st.session_state.graph = self.__cell_trace_controller.graph(
                    self.__sheet,
                    self.__row,
                    self.__clm
                )

        if "graph" in st.session_state:
            st.graphviz_chart(st.session_state.graph)
