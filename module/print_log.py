from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os, subprocess, asyncio
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # 디스플레이 설정에 따라 변하게

class RunCommand(QThread):
    def __init__(self):
        super().__init__()
        self.commandQueue = []

    def appendQueue(self, command):
        self.commandQueue.append(command)

    async def run(self, command, widget):
        try:
            process = await asyncio.create_subprocess_shell(command,
                                        stdout=asyncio.subprocess.PIPE,
                                        stderr=asyncio.subprocess.STDOUT,
                                        text=True)
            async for line in process.stdout:
                widget.appendPlainText(line.strip())
            await process.wait()
        except Exception as e:
            widget.appendPlainText(f"명령어 실행 중 오류 발생: {str(e)}")

    async def runCommands(self):
        for command in self.commandQueue:
            await self.run(command)