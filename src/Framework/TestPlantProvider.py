


from Framework.TestPlant.ITestSystem import *
from Framework.TestPlant.CsPlusSimulator import *
from Framework.TestPlant.TestSystemCallNotifier import *
from Framework.Logger.ITestLogger import *
from Framework.Logger.XmlTestLogger import *
from Framework.Logger.TextTestLogger import *
from lib.Singleton import *

class TestPlantProvider(Singleton):
    def __init__(self):
        pass

    def setup( self ) -> None:
        # 生成するロガーを変更する場合、以下を書き換えてください
        #self.__logger = XmlTestLogger()
        self.__logger = TextTestLogger()

        # ターゲットのテストシステムを変更する場合、以下を書き換えてください
        # 例) CS+からGHSに変更
        test_system = CsPlusSimulator()

        self.__system = TestSystemCallNotifier( test_system )
        self.__system.set_notifee( self.__logger )

    def system( self ) -> ITestSystem:
        return self.__system

    def logger( self ) -> ITestLogger:
        return self.__logger



