# *U*taipei*wU*

北市大選課模擬器 / utaipei course selection simulator.

修改自 NTH*Uw*U

## Feature

- 基本模擬排課
- 將課表輸出為圖片
- 分享/匯入課表
- 使用 Google OAuth 登入(由於許多瀏覽器均不再支援跨來源重新導向登入功能，因此目前無法使用，詳細資訊請參閱[這裡](https://firebase.google.com/docs/auth/web/redirect-best-practices?hl=zh&authuser=0))

## 開發

### 爬蟲

這個專案使用 poetry。它是一個現代的依賴管理工具。

要在本機運行專案，請使用以下命令：  
（你需要先在電腦上裝好 poetry）

```bash
poetry config virtualenvs.path .venv
poetry config virtualenvs.in-project true  
poetry install
poetry run python -m course_crawler
```

### 前端

這是一個純靜態 HTML + JS + CSS 專案，可以直接進行開發。
