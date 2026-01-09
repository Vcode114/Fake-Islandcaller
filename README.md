# Camera Button (Windows 10)

一个小型的 Python 伪装点名程序：在桌面显示一个无边框、透明背景的图标按钮，单击后启动 Windows 10 本地相机应用。
可以骗骗你那爱玩点名的同学 =)
使用前确保运行环境具有Python

准备：

- 将你的 `Icon.png`（带 alpha 透明通道）放到与 `main.py` 相同的目录：camera_button/。
- 安装依赖：
  先打开文件夹，运行cmd或者powershell，然后输入并回车
python -m pip install -r requirements.txt

运行：
python main.py

说明：

- 按钮无边框、背景透明，大小默认为 48x48，可在 `main.py` 中调整 `size` 参数。
- 启动相机使用 `start microsoft.windows.camera:` 协议，适用于 Windows 10 UWP Camera 应用。

