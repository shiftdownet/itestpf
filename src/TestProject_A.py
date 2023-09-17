

import datetime
from collections.abc import Iterator
from Framework.ITestProject import ITestProject
from Framework.TestDriver import TestDriver
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.TestPlant.CsPlusSimulator import CsPlusSimulator
from Framework.TestPlant.MockSimulator import MockSimulator
from Framework.Logger.ITestLogger import ITestLogger
from Framework.Logger.YamlTestLogger import YamlTestLogger
from Framework.Logger.XmlTestLogger import XmlTestLogger
from Framework.Logger.TextTestLogger import TextTestLogger
from Framework.Logger.JsonTestLogger import JsonTestLogger
from Suites import *

class TestProject(ITestProject):
    def logger(self) -> ITestLogger:
        return JsonTestLogger()
        #return YamlTestLogger()
        #return XmlTestLogger()
        #return TextTestLogger()

    def log_filename(self) -> str:
        return "./log_latest.json"
        # ログファイルに日付を含める場合は以下
        #return './log_' + (datetime.datetime.now()).strftime('%Y%m%d_%H%M%S') + '.yaml'
    
    def log_encoding(self) -> str:
        return 'utf-8'
    
    def test_system(self) -> ITestSystem:
        return MockSimulator()
        # 本番では以下を選択
        #return CsPlusSimulator()

    def suites(self) -> Iterator:
        yield Suite_Sample1()
        yield Suite_Sample1()

if __name__ == "__main__": 
    TestDriver().launch( TestProject() )

