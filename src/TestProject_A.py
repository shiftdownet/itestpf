

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
from Suites import *

class TestProject(ITestProject):
    def logger(self) -> ITestLogger:
        return YamlTestLogger()

    def log_filename(self) -> str:
        return "./test_log.yaml"
    
    def log_encoding(self) -> str:
        return 'utf-8'
    
    def test_system(self) -> ITestSystem:
        return MockSimulator()

    def suites(self) -> Iterator:
        yield Suite_Sample1.Suite_Sample1()

if __name__ == "__main__": 
    TestDriver().launch( TestProject() )

