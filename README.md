# 

## デプロイ (Docker)

1. イメージ作成

    ```
    docker build --tag cell-reference-tracer:(バージョン) .
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
