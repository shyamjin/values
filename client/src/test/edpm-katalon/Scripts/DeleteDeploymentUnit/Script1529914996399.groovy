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

String duName = WebUI.callTestCase(findTestCase('CreateDeploymentUnit'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/a_DU Dashboard'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), duName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForAngularLoad(30)

WebUI.click(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_Edit DU'))

WebUI.waitForAngularLoad(30)

WebUI.click(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_Remove this du'))

//WebUI.waitForElementVisible(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_Continue'), 30, FailureHandling.STOP_ON_FAILURE)

WebUI.verifyElementClickable(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_Continue'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_Continue'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), duName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForAngularLoad(30)

if (WebUI.verifyElementPresent(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/a_duName'), 10, FailureHandling.OPTIONAL)) {
	if (WebUI.verifyElementText(findTestObject('DeleteDeploymentUnit/Page_Amdocs GSS Value Pack/a_duName'), duName)) {
		return false
	}
} else {
	return true
}

