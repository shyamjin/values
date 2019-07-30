set PROJECT_PATH=%cd%
cd %KATALON_HOME%
katalon.exe -noSplash -consoleLog -runMode=console -projectPath="%PROJECT_PATH%/edpm-katalon.prj" -retry=0 -testSuitePath="Test Suites/BasicSanity" -executionProfile="default" -browserType="Chrome (headless)"