
import abc
from collections.abc import Iterator
from Framework.TestPlant.ITestSystem import ITestSystem
from Framework.Logger.ITestLogger import ITestLogger

class ITestProject(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def logger(self) -> ITestLogger:
        raise NotImplementedError()

    @abc.abstractmethod
    def log_filename(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def log_encoding(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def test_system(self) -> ITestSystem:
        raise NotImplementedError()

    @abc.abstractmethod
    def suites(self) -> Iterator:
        raise NotImplementedError()
