---
# Setting for Markdown Preview Enhanced v0.6.3
toc:                        # 目次設定
  depth_from: 1             # - 目次化する開始ネスト
  depth_to: 4               # - 目次化する終了ネスト
  ordered: false            # - オーダーを表示しない
html:                       # HTMLファイル出力に関する設定
  embed_local_images: true  # - ローカル埋め込み画像ファイルを有効にする
  embed_svg: true           # - SVGの埋め込みを有効にする
  offline: true             # - offlineでの生成を有効にする
  toc: true                 # - デフォルトでサイドバーにTOCを表示する
export_on_save:             # ファイル保存時の振る舞い
  html: true                # - htmlで出力(※Markdown PDF等他のAddinの自動保存機能は無効化してください)
---



# 1. フレームワークとユーザスクリプトの境界仕様


```plantuml
!include ./objects.iuml
scale 0.8

remove Logger
remove TestPlant
remove ITestLogger
remove ITestSystem
remove ITestSystemDecorator


TestProject_A -up[hidden] ITestProject

class TestEntry <<E, limegreen>> {
    エントリポイントです。\n実装はTestProject_Aモジュールに含まれています。
}

TestDriver -le[hidden] TestEntry
TestDriver -do[hidden]- ITestProject
ITestProject -ri[hidden] TestPlantProvider
ITestCase -do[hidden]- ITestSuite

TestProject_A "1" -ri-> "*" TestSuiteX : <<create>>\nsuitesジェネレータ内\nで生成します。
TestEntry -do-> TestProject_A : <<create>>生成します。
TestEntry -up---> TestDriver : <<use>>\n生成したTestProjectを渡して\nテストを実行します。

TestDriver -> ITestSuite : <<call>>\nテストの準備・終了、及び\ntestcasesメソッドより\n実行対象のテストケースを取得します。
TestDriver -> ITestCase : <<call>> \nITestSuiteから取得したテストケースを\n順番に実行します。
TestDriver -do> TestPlantProvider : <<use>>\nテストプラントの操作や\nロギングを行います。
TestDriver -do-> ITestProject : <<use>>\n実行対象のテストスイートを取得します。

TestSuiteX "1" *-ri-> "*" TestCaseX : <<composite>>\ntestcasesジェネレータ内\nで生成します。
TestSuiteX -up> TestPlantProvider : <<use>>\nテストプラントの操作や\nロギングを行います。
TestCaseX -up> TestPlantProvider : <<use>>\nテストプラントの操作や\nロギングを行います。


```
# 2. フレームワーク内部(TestPlantProvider)の詳細


```plantuml
!include ./objects.iuml
scale 0.8

remove TestDriver
remove TestCaseX
remove TestSuiteX
remove TestSpec

'skinparam groupInheritance 2
Framework.Logger.ConcreteTestLogger -up[hidden]-- ITestLogger
Framework.TestPlantProvider *-up-> Framework.Logger.ConcreteTestLogger : <<composite>>\nITestProjectの情報に基づき\n生成し保持します
Framework.TestPlantProvider -up.> Framework.TestPlant.ConcreteTestSystem : <<create>>\nITestProjectの情報に基づき\n生成しデコレータに渡します。
Framework.TestPlantProvider *-up-> Framework.TestPlant.TestSystemCallNotifier : <<composite>>\n生成し保持します
Framework.TestPlant.TestSystemCallNotifier o-up- Framework.TestPlant.ITestSystem : <<aggregate>>\nコンストラクタで受け取った\nインスタンスを保有します


circle "ITestSystem" as Framework.Logger.ITestSystem_Implements_By

Framework.TestPlant.TestSystemCallNotifier -( Framework.Logger.ITestSystem_Implements_By : <<notify>>\nテストシステムの\nコールを通知します
Framework.Logger.ConcreteTestLogger - Framework.Logger.ITestSystem_Implements_By

Framework.TestPlantProvider -> Framework.ITestProject : <<use>>\nコンフィグ情報を使用し\nプロバイダを構築します。

TestPlantProvider --() 本プロバイダからテストプラントを操作します

```



# 3. 実行シーケンス

```plantuml
!pragma teoz true
scale 0.8

skinparam SequenceLifeLineBackgroundColor LightSteelBlue

participant IronPythonConsole

participant "TestEntry\n※TestProject_Aに含まれる" as TestEntry
participant TestProject_A
participant TestSuiteX
participant TestCaseX
box Framework
    participant TestDriver
    box Logger
        participant ConcreteTestLogger
    endbox
    box TestPlant
        participant ConcreteTestSystem
        participant TestSystemCallNotifier
        participant TestPlantProvider
    endbox
endbox


autoactivate on

activate IronPythonConsole

IronPythonConsole -> TestEntry  : Source(TestProject_A)

    create TestProject_A
    TestEntry -> TestProject_A  : __init()
    return


    '#----------------------------------------------------
    '# TestDriver.launch()
    '#----------------------------------------------------
    TestEntry -> TestDriver  : launch( instance of TestProject_A )

        TestDriver -> TestDriver  : __prepare()
            '#----------------------------------------------------
            '# TestPlantProvider.setup()
            '#----------------------------------------------------
            TestDriver -> TestPlantProvider  : setup()
                TestPlantProvider -> TestProject_A : logger()
                    create ConcreteTestLogger
                    TestProject_A -> ConcreteTestLogger  : __init()
                    return
                return instance of ConcreteTestLogger

                TestPlantProvider -> TestProject_A : test_system()
                    create ConcreteTestSystem
                    TestProject_A -> ConcreteTestSystem  : __init()
                    return
                return instance of ConcreteTestSystem

                create TestSystemCallNotifier
                TestPlantProvider -> TestSystemCallNotifier  :  __init( instance of ConcreteTestSystem )
                return
                TestPlantProvider -> TestSystemCallNotifier  :  set_notifee( instance of ConcreteTestLogger )
                return
                TestPlantProvider -> TestProject_A : log_filename()\nlog_encoding()
                return ファイル名, フファイルエンコーディング
                hnote over TestPlantProvider : ファイルオープン
                TestPlantProvider -> ConcreteTestLogger  : set_stream( stream )
                return
            return
        return

        TestDriver -> TestDriver  : __execute()

            TestDriver -> ConcreteTestLogger  : TestPlantProvider.logger.start_test()
            return

            loop ジェネレータがテストスイートを返さなくなるまで
                TestDriver -> TestProject_A : suites()\nテストスイートをジェネレータで\n1件づつ取得
                return

                TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.start_suite( suite )
                return

                TestDriver -> TestSuiteX  : prepare()
                return

                loop ジェネレータがテストケースを返さなくなるまで
                    TestDriver -> TestSuiteX : testcases()\nテストケースをジェネレータで\n1件づつ取得
                    return
                    TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.start_case( testcase )
                    return
                    TestDriver -> TestCaseX : prepare()
                    return

                    loop ジェネレータがテストステップを返さなくなるまで
                        TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.start_step()
                        return
                        TestDriver -> TestCaseX : steps()
                            group example ステップの実行例
                                TestCaseX -> TestSystemCallNotifier : TestPlantProvider.system.test_variable( 変数名, 期待値 )
                                    TestSystemCallNotifier -> ConcreteTestSystem : test_variable( 変数名, 期待値 )
                                    return
                                    TestSystemCallNotifier -> ConcreteTestLogger : test_variable( 変数名, 期待値 )
                                    return
                                return
                            end
                        return
                        TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.end_step()
                        return
                    end loop

                    TestDriver -> TestCaseX : tear_down()
                    return
                    TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.end_case( testcase )
                    return

                end loop

                TestDriver -> TestSuiteX  : tear_down()
                return

                TestDriver -> ConcreteTestLogger : TestPlantProvider.logger.end_suite( suite )
                return
            end loop
        return

        TestDriver -> TestDriver  : __tear_down()
            TestDriver -> ConcreteTestLogger  : TestPlantProvider.logger.end_test()
            return
            TestDriver -> TestPlantProvider : tear_down()
                hnote over TestPlantProvider : ファイルクローズ
            return
        return
    return

return



'TestEntry 


```


<header id="header"><div id="title">{meta.documentName}</div><div id="document_info"><div id="document_id">{meta.documentID}-{meta.version}</div><div id="version">{meta.version}</div></div></header>
<footer id="footer">- {meta.issued} - CONFIDENTIAL</footer>
<style> header { position:fixed !important; height: 60px; width:100%; z-index:3000; top: 0px; left:0px; background-color: rgba(255,255,255,0.8); border-bottom: 1px solid gray !important; box-sizing: border-box;} #title { padding-left:0.5em; font-size:20px; font-weight:bold; } #document_info { display:block; position:fixed; top:0.5em; right:1em; font-weight:bold; color:#666, font-size:14px; text-align:right;} #document_id::before {content:"DOCUMENT ID: "} #version { display:inline;} #version::before { content: "VERSION: "} footer { position:fixed !important; bottom:0px; left:0px; width:100%; height:20px; z-index:3500; background-color:white; border-top: 1px solid slategray; text-align:center; font-size:15px; color:#333; font-weight:bold; } .md-sidebar-toc{ top:60px !important; height: calc(100% - 60px - 20px) !important; overflow:scroll !important; white-space:nowrap; font-size:12px !important; } .markdown-preview { margin:0 !important; padding: 1em 1em 1em 1em !important; position:fixed !important; top:60px !important; height:calc(100% - 60px) !important; overflow:scroll !important;} html body[for="html-export"]:not([data-presentation-mode]):not([html-show-sidebar-toc]) .markdown-preview{left:0% !important; transform: initial !important;} .md-sidebar-toc::-webkit-scrollbar { height:8px !important; } #sidebar-toc-btn { bottom:0px !important; top:60px;} h1, h2, h3, h4, h5, h6 { border-bottom: solid 2px #333 !important; font-weight:bold; margin:2em 0em 0em 0em !important; } h1 + h2 { page-break-before:auto; margin-top : 0.5em !important; } h2 + h3 { page-break-before: auto; margin-top: 0.5em !important; } h3 + h4 { page-break-before: auto; margin-top: 0.5em !important; }  h3 + h4 { page-break-before: auto; margin-top: 0.5em !important; }  h4 + h5 { page-break-before: auto; margin-top: 0.5em !important; }  h5 + h6 { page-break-before: auto; margin-top: 0.5em !important; } h1,h2,h3{ font-size:24px !important;} h4,h5,h6 { font-size:22px !important; } .column-left{ float: left; width: calc(50% - 10px); text-align: left;} .column-right{ float: right; width: calc(50% - 10px);text-align: left;}  .three-column{ float: left; width: calc(33% - 15px); text-align: left; margin-left: 10px;} .clearfix::after{ content: ""; clear: both; display: block; } pre, code, var, samp, kbd, .mono { font-family: 'ＭＳ ゴシック', Consolas, 'Courier New', Courier, Monaco, monospace !important; line-height: 1.2 !important;}
</style>
