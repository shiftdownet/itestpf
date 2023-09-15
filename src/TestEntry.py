
from typing import List
from Framework.TestDriver import *
from Framework.TestSpec.ITestSuite import *
from Suites import *

class TestEntry():
    def execute(self):
        TestDriver().execute(
            (
                Suite_Sample1.Suite_Sample1(),
                # ここにカンマ区切りでテストスイートを追加してください。
                # 例)
                #   Suite_Sample2,
                #   Suite_Sample3,
                #   Suite_Sample4,
            )
        )


TestEntry().execute()

