Sandbox Platform
简介
Sandbox Platform 是一个用于简化蜜罐沙箱制作步骤的平台。它通过 mitmproxy 和 rad 作为部分引擎，可以对制作的沙箱网站数据包进行灵活修改，例如挂上反制木马、JS 等。

项目结构
plaintext
复制代码
sandbox_platform/
├── app.py
├── venv/
├── engine/
│   ├── rad_windows_amd64.exe
│   ├── engine.exe
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── ExecuteCommand.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .gitignore
│   ├── babel.config.js
│   ├── package.json
│   ├── README.md
│   └── vue.config.js
如何使用
安装依赖
首先，确保你已经安装了 Python3.10以上 和 Node.js v20.15.0然后，在项目的根目录下运行以下命令来安装 Python 依赖：


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

项目结构详解
app.py：后端 Flask 应用的入口文件。
venv/：Python 虚拟环境目录，包含项目的 Python 依赖。
engine/：存放引擎的目录，包括 rad 和其他执行文件。
frontend/：前端项目目录，使用 Vue.js 开发。
node_modules/：Node.js 依赖目录。
public/：公共静态资源目录。
src/：前端源代码目录。
assets/：静态资源，如图像、样式等。
components/：Vue 组件目录。
ExecuteCommand.vue：执行命令的组件。
App.vue：主应用组件。
main.js：前端入口文件。
.gitignore：Git 忽略文件配置。
babel.config.js：Babel 配置文件。
package.json：Node.js 项目配置文件，包含项目依赖和脚本。
README.md：前端项目的 README 文件。
vue.config.js：Vue 项目的配置文件。
按照上述步骤和说明，你可以轻松地启动并运行 Sandbox Platform，体验蜜罐沙箱数据包的灵活修改功能。
