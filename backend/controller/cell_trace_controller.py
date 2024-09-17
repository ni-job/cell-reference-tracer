from io import BufferedReader

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
        self.__graph_handler:  GraphvizHandler
        self.__file_name: str
        self.__sheet: str
        self.__row: int
        self.__clm: int
        self.__format: str


    def upload_excel(self, file_bytes: bytes, file_name: str) -> None:
        """
        Excelファイルを読み込む

        params:
            file_obj: Excelファイルのファイルデータ
        """
        self.__file_name = file_name
        self.__excel_handler = ExcelHandler(file_bytes, file_name)

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

        self.__sheet = sheet_name
        self.__row = row
        self.__clm = clm
        self.__format = graph_format

        self.__graph_handler =  GraphvizHandler(graph_format)
        cell_tracer = CellTracer(self.__excel_handler, self.__graph_handler, max_trace_size)

        cell_tracer.make_graph(sheet_name, row, clm)
        return self.__graph_handler.get_graph()

    def export(self) -> tuple[bytes, str]:
        """
        グラフを出力する
        """
        return (
            self.__graph_handler.export(),
            f"{self.__file_name.split(".")[0]}_"\
                f"{self.__sheet}_{self.__row}_{self.__clm}.{self.__format}"
        )
