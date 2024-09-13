import streamlit as st
from streamlit.navigation.page import StreamlitPage

from backend.controller.cell_trace_controller import CellTraceController


class TraceOutputPage:
    """
    シートとセルを選択して、参照元グラフを表示するページ
    """

    def __init__(self, controller: CellTraceController) -> None:
        self.__cell_trace_controller: CellTraceController = controller

    def page(self) -> StreamlitPage:
        """
        ページを取得する
        """

        return st.Page(self.__layout, title="グラフ表示")

    def __layout(self):
        st.write("シートとセルを選択してください")
