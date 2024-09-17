# 

## 単体テスト

1. VSCodeの拡張機能「Coverage Gutters」をインストール

1. 単体テストを実行
    ```
    python -m pytest tests/ --cov=backend/ --cov-report=xml
    ```

1. VSCodeの画面下部に表示される「〇 Watch」をクリックするとコード上にカバレッジが表示される

## デプロイ (Docker)

1. イメージ作成

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
