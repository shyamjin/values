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

String toolSetName = 'ts' + randomString

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

String toolName1 = WebUI.callTestCase(findTestCase('CreateTool'), [:], FailureHandling.STOP_ON_FAILURE)

String toolName2 = WebUI.callTestCase(findTestCase('CreateTool'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/a_New tool set'))

WebUI.setText(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/input_name'), toolSetName )

WebUI.click(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/span_Add'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/input_searchToolField'), toolName1)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/span_Add_1'))

WebUI.setText(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/input_searchToolField'), toolName2)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/span_Add_1'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/button_Update'))

WebUI.click(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/input_login-button'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), toolSetName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForAngularLoad(30)

WebUI.verifyElementPresent(findTestObject('CreateToolSet/Page_Amdocs GSS Value Pack/button_Edit'), 30)

return toolSetName

