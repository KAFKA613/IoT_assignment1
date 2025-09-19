# Brawl Stars API 近期對戰分析工具

透過 Brawl Stars 官方 API 來查詢玩家對戰記錄並進行統計分析的 Python 工具。

## 功能

- 查詢指定玩家的近期對戰記錄
- 統計玩家最常用的角色
- 顯示對戰期間（台灣時區）
- 分析對戰場數

## 環境需求

- Python 3.6 或更高版本
- Brawl Stars API 金鑰

## 安裝步驟

### 1. 下載專案

### 1. 建立虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 4. 設定環境變數
在專案根目錄創建 `.env` 檔案：
```bash
touch .env
```

在 `.env` 檔案中加入 Brawl Stars API 金鑰：
```
BRAWLSTARS_API_KEY=你的API金鑰
```

## 如何取得 API 金鑰

1. 前往 [Brawl Stars 開發者網站](https://developer.brawlstars.com/)
2. 註冊帳號
3. My Kay > Create API Key
4. 複製產生的 API 金鑰

## 使用方法

### 啟動程式
```bash
python app.py
```

### 輸入玩家標籤
程式會提示你輸入玩家標籤，例如：`1ABCD0ABC`

**注意：** 輸入時不需要包含 `#` 符號，程式會自動加上。

## 輸出範例

```
Brawl Stars 近期對戰統計
========================================
請輸入玩家標籤 (例如: 1ABCD0ABC): 1ABCD0ABC

正在查詢玩家 #1ABCD0ABC 的戰鬥記錄...

========================================
 玩家ID: #1ABCD0ABC
 近期對戰場數: 25
 對戰期間: 2024-01-15 14:30 至 2024-01-20 18:45 (台灣時間)
========================================
 常用角色排名:
   1. Shelly: 8 次
   2. Colt: 6 次
   3. Bull: 4 次
   4. Jessie: 3 次
   5. Dynamike: 2 次
   6. Bo: 2 次
========================================
```

## 專案結構

```
brawl_stars_api/
├── app.py              # 主程式檔案
├── requirements.txt    # Python 依賴套件清單
├── .env               # 環境變數檔案（需要自行創建）
├── venv/              # Python 虛擬環境
└── README.md          # 說明文件
```

## 依賴套件

- `requests`: HTTP 請求庫
- `python-dotenv`: 環境變數管理
- `certifi`: SSL 憑證驗證
- `charset-normalizer`: 字符編碼檢測
- `idna`: 國際化域名支援
- `urllib3`: HTTP 客戶端庫