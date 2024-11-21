# Expensive Mongo Project

一個基於 **Flask** 和 **MongoDB** 的簡單應用程式，用於管理收支項目的新增、查詢和刪除功能。

## 功能特點

- **新增項目**：添加新的項目資料到資料庫（分別可以為收入、支出）。
- **刪除項目**：從資料庫中移除指定的項目。
- **所有項目**：列出所有已添加的項目。

## 環境需求

- Python 3.x
- MongoDB 資料庫
- 虛擬環境工具（如 `venv` 或 `virtualenv`）

## 安裝指南

1. **clone此專案：**

    ```sh
    git clone <repository-url>
    ```

2. **進入專案目錄：**

    ```sh
    cd 
    ```

3. **建立並啟用虛擬環境：**

    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```

4. **安裝所需套件：**

    ```sh
    pip install -r requirements.txt
    ```

5. **設定環境變數：**

    - 建立一個 `.env` 檔案，並添加您的 MongoDB 連接字串：

      ```
      MONGO_URI=mongodb://localhost:27017/your-database
      ```

6. **啟動應用程式：**

    ```sh
    flask run
    ```
