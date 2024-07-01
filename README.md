# Sandbox Platform

## 简介

Sandbox Platform 是一个用于简化蜜罐沙箱制作步骤的平台。它通过 mitmproxy 和 rad 作为部分引擎，可以对制作的沙箱网站数据包进行灵活修改，例如挂上反制木马、JS 等。
## 如何使用

### 安装依赖

首先，确保你已经安装了 Python3.10 和 Node.js。然后，在项目的根目录下运行以下命令来安装 Python 依赖：
```sh
pip install -r requirements.txt
启动后端服务
在项目根目录下运行以下命令来启动 Flask 应用：
python app.py
安装并启动前端服务
导航到 frontend 目录并安装 Node.js 依赖：
cd frontend
npm install
然后，启动前端开发服务器：
npm run serve
访问平台
前端开发服务器启动后，你可以在浏览器中访问 http://localhost:8888 以使用 Sandbox Platform。

## 项目结构
sandbox_platform/
├── app.py
├── venv/
├── engine/
│ ├── rad_windows_amd64.exe
│ ├── engine.exe
├── frontend/
│ ├── node_modules/
│ ├── public/
│ ├── src/
│ │ ├── assets/
│ │ ├── components/
│ │ │ └── ExecuteCommand.vue
│ │ ├── App.vue
│ │ └── main.js
│ ├── .gitignore
│ ├── babel.config.js
│ ├── package.json
│ ├── README.md
│ └── vue.config.js



