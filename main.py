import streamlit as st

from backend.controller.cell_trace_controller import CellTraceController
from frontend.excel_select_page import ExcelSelectPage
from frontend.trace_output_page import TraceOutputPage

# コントローラーを用意する
cell_trace_controller = CellTraceController()

# ページを用意する
excel_select_page = ExcelSelectPage(cell_trace_controller).page()
trace_output_page = TraceOutputPage(cell_trace_controller).page()

# アプリにページを登録する
app = st.navigation(
    [
        excel_select_page,
        trace_output_page
    ],
    position="hidden"
)

app.run()
