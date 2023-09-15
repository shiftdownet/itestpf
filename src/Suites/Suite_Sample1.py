
from collections.abc import Iterator
from Framework.TestSpec.ITestSuite import *

from Suites.Cases.Case_Sample_00001 import *

class Suite_Sample1(ITestSuite):
    def name( self ) -> str:
        return "SWE5TST-SUITE-SAMPLE1"

    def description() -> str:
        return "特記事項無し"

    def testcases(self) -> Iterator:# Iterator[ITestCase]: # CPythonは通るが、IronPythonだとエラーになる
        yield Case_Sample_00001()
        yield Case_Sample_00001()

    def prepare(self) -> None:
        pass

    def tear_down(self) -> None:
        pass
