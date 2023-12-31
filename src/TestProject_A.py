

import datetime
from collections.abc import Iterator
from Framework.ITestProject import ITestProject
from Framework.TestDriver import TestDriver
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.TestPlant.CsPlusSimulator import CsPlusSimulator
from Framework.TestPlant.MockSimulator import MockSimulator
from Framework.Logger.ITestLogger import ITestLogger
from Framework.Logger.TextTestLogger import TextTestLogger
from Framework.Logger.JsonTestLogger import JsonTestLogger
from Suites import *

class TestProject(ITestProject):
    def logger(self) -> ITestLogger:
        # ロガー形式を指定
        return JsonTestLogger() # 標準で使えるのがjsonパーサったのでjsonは実装
        #return TextTestLogger()

    def log_filename(self) -> str:
        return "./log_latest.log"
        # ログファイルに日付を含める場合は以下
        #return './log_' + (datetime.datetime.now()).strftime('%Y%m%d_%H%M%S') + '.log'
    
    def log_encoding(self) -> str:
        return 'utf-8'
    
    def test_system(self) -> ITestSystem:
        # テストシステムを指定する
        return MockSimulator()
        # 本番では以下を選択
        #return CsPlusSimulator()

    def suites(self) -> Iterator:
        # ここにテストスイートを次々に追加していく
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()
        yield Suite_Sample1()

if __name__ == "__main__": 
    TestDriver().launch( TestProject() )

    # Jsonのログをjsに変換
    from pathlib import Path
    src_path = Path(TestProject().log_filename())
    dst_path = Path("./testlog.js")
    stream = src_path.read_text(encoding=TestProject().log_encoding())
    stream = 'test_logs = ' + stream
    dst_path.write_text(stream, encoding=TestProject().log_encoding())
