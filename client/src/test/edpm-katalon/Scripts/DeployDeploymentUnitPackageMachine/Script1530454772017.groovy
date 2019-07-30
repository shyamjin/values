import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.checkpoint.Checkpoint as Checkpoint
import com.kms.katalon.core.checkpoint.CheckpointFactory as CheckpointFactory
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as MobileBuiltInKeywords
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords as Mobile
import com.kms.katalon.core.model.FailureHandling as FailureHandling
import com.kms.katalon.core.testcase.TestCase as TestCase
import com.kms.katalon.core.testcase.TestCaseFactory as TestCaseFactory
import com.kms.katalon.core.testdata.TestData as TestData
import com.kms.katalon.core.testdata.TestDataFactory as TestDataFactory
import com.kms.katalon.core.testobject.ObjectRepository as ObjectRepository
import com.kms.katalon.core.testobject.TestObject as TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WSBuiltInKeywords
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUiBuiltInKeywords
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import internal.GlobalVariable as GlobalVariable
import org.openqa.selenium.Keys as Keys

CustomKeywords.'helper.Initializer.initWebUI'()

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/a_DU Dashboard'))

WebUI.click(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/span_DU Package'))

WebUI.waitForAngularLoad(30)

WebUI.waitForElementVisible(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_Deploy'), 5, FailureHandling.STOP_ON_FAILURE)

WebUI.setText(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), 'KatalonDUPackTest')

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForElementVisible(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_Deploy'), 5, FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_Deploy'))

WebUI.setText(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/input_searchMachine'), 'KatalonMachineTest2')

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/span_Select for all entities machine'))

WebUI.waitForAngularLoad(30)

if (WebUI.verifyElementPresent(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/label_Skip If Already Deployed'), 10, FailureHandling.OPTIONAL)) {
    WebUI.click(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/label_Skip If Already Deployed'))
}

WebUI.click(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/button_Submit for deployment'))

WebUI.verifyElementPresent(findTestObject('DeployDeploymentUnitPackageMachine/Page_Amdocs GSS Value Pack/td_The request has completed'),200)

