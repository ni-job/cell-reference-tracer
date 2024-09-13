import streamlit as st

from backend.controller.cell_trace_controller import CellTraceController
from frontend.excel_select_page import ExcelSelectPage
from frontend.trace_output_page import TraceOutputPage

# コントローラーを用意する
if "cell_trace_controller" not in st.session_state:
    st.session_state.cell_trace_controller = CellTraceController()

# ページを用意する
if "excel_select_page" not in st.session_state:
    st.session_state.excel_select_page = ExcelSelectPage(
        st.session_state.cell_trace_controller
    ).page()
if "trace_output_page" not in st.session_state:
    st.session_state.trace_output_page = TraceOutputPage(
        st.session_state.cell_trace_controller
    ).page()

# アプリにページを登録する
app = st.navigation(
    [
        st.session_state.excel_select_page,
        st.session_state.trace_output_page
    ],
    position="hidden"
)

app.run()
