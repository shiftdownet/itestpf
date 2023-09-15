
import abc
from collections.abc import Iterator
from Framework.TestSpec.ITestCase import *

class ITestSuite(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def testcases(self) -> Iterator:# Iterator[ITestCase]: # CPythonは通るが、IronPythonだとエラーになる
        raise NotImplementedError()

    @abc.abstractmethod
    def prepare(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def tear_down(self) -> None:
        raise NotImplementedError()
