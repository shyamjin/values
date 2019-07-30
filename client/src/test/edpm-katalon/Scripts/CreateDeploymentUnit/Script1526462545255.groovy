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
import org.apache.commons.lang.RandomStringUtils as RandomStringUtils

CustomKeywords.'helper.Initializer.initWebUI'()

String randomString = RandomStringUtils.randomAlphanumeric(7)

String duName = 'du' + randomString

String brName = 'br' + randomString

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/a_New DU'))

WebUI.setText(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/input_name'), duName)

WebUI.click(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/li_Type'))

WebUI.selectOptionByLabel(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/select_Fast TrackHot FixVersio'), 
    'Fast Track', false)

WebUI.setText(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/input_branch'), brName)

WebUI.scrollToElement(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/div_Select'), 0)

WebUI.click(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/div_Select'))

WebUI.click(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/span_CRM-DB'))

WebUI.click(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/input_vp-dttoolbar__savebtn vp'))

WebUI.verifyElementPresent(findTestObject('CreateDeploymentUnit/Page_Amdocs GSS Value Pack/div_newHeader'), 0, FailureHandling.STOP_ON_FAILURE)

//WebUI.callTestCase(findTestCase('DeleteDeploymentUnit'), ["duName":duName], FailureHandling.STOP_ON_FAILURE)

return duName
