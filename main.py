import streamlit as st

from backend.controller.cell_trace_controller import CellTraceController
from frontend.excel_select_page import ExcelSelectPage

# コントローラーを用意する
cell_trace_controller = CellTraceController()

# ページを用意する
excel_select_page = ExcelSelectPage(cell_trace_controller).page()

app = st.navigation([
    excel_select_page
])

app.run()
