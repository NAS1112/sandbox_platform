# sandbox_platform
简介
sandbox_platform是为了简化蜜罐沙箱的制作步骤，通过mitmproxy和rad作为部分引擎；可以对制作的沙箱的网站数据包进行灵活修改；比如挂上反制木马、js等
项目结构
sandbox_platform/
├── app.py
├── venv/
└──engine
    ├── rad_windows_amd64.exe
    ├── engine.exe
└── frontend/
    ├── node_modules/
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   │   └── ExecuteCommand.vue
    │   ├── App.vue
    │   └── main.js
    ├── .gitignore
    ├── babel.config.js
    ├── package.json
    ├── README.md
    └── vue.config.js
如何使用
pip install -r requirements.txt
