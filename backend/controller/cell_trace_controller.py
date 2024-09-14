import os
import tempfile as tmpf

from streamlit.runtime.uploaded_file_manager import UploadedFile

from backend.domain.cell_tracer import CellTracer
from backend.handler.excel_handler import ExcelHandler
from backend.handler.graph_handler import GraphvizHandler, Digraph


class CellTraceController:
    """
    Excelのセル参照元をグラフにするユースケースのコントローラー
    """

    def __init__(self) -> None:
        self.cell_tracer: CellTracer
        self.__excel_handler: ExcelHandler

    def upload_excel(self, file_obj: UploadedFile) -> None:
        """
        Excelファイルを読み込む

        params:
            file_obj: Excelファイルのファイルデータ
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

    def graph(
            self, sheet_name: str, row: int, clm: int, graph_format: str, max_trace_size: int
        ) -> Digraph:
        """
        指定したシート、行、列のセルの参照元をたどったグラフを取得する

        params:
            sheet_name: シート名
            row: セルの行番号
            clm: セルの列番号
            graph_format: グラフのフォーマット
            max_trace_size: トレースできるRangeの最大サイズ
        return:
            Graphvizのグラフ
        """

        graph_handler =  GraphvizHandler(graph_format)
        cell_tracer = CellTracer(self.__excel_handler, graph_handler, max_trace_size)

        cell_tracer.make_graph(sheet_name, row, clm)
        return graph_handler.get_graph()
