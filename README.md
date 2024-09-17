# Cell Reference Tracer

Excelセルの数式に含まれる参照元を辿ってグラフにするツール

## 環境構築

### ミドルウェア

- WSL

以下を WSL 内にインストールする

- Python3.12
- pyenv (仮想環境用)
- Graphviz
- Docker Engine

### 構築手順

1. WSL を開く

1. リポジトリをクローンする

1. クローンしたプロジェクトフォルダを開く

1. pyenv から Python3.12 の仮想環境を作成する

    ```
    pyenv local 3.12
    python -m venv .venv
    source .venv/bin/activate
    ```

1. 外部ライブラリをインストールする

    ```
    pip install -r requirements.txt
    ```

## 実行

```
streamlit run main.py
```

## デバッグ

.vscode/settings.json の configurations を以下の内容に変更する

```json
    "configurations": [
        {
            "name": "Python デバッガー: Streamlit",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/bin/streamlit",
            "console": "integratedTerminal",
            "args": [
                "run",
                "main.py"
            ]
        }
    ]
```

## 単体テスト

1. VSCodeの拡張機能「Coverage Gutters」をインストール

1. 単体テストを実行
    ```
    python -m pytest tests/ --cov=backend/ --cov-report=xml
    ```

1. VSCodeの画面下部に表示される「〇 Watch」をクリックするとコード上にカバレッジが表示される

## Docker コンテナで実行

1. イメージ作成

    ```
    docker build --tag cell-reference-tracer .
    ```

    ### リモートリポジトリ用

    ```
    docker build --tag ghcr.io/ni-job/cell-reference-tracer .
    ```

1.  イメージ確認

    ```
    docker images
    ```

1. コンテナ作成

    ```
    docker run -d --restart always -p 8501:8501 (IMAGE ID)
    ```

1. コンテナ確認

    ```
    docker ps
    ```

1. localhost:8501 にアクセス