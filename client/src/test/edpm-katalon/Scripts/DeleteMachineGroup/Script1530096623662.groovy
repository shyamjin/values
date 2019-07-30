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

String mgName = WebUI.callTestCase(findTestCase('CreateMachineGroup'), [:], FailureHandling.STOP_ON_FAILURE)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/a_Manage machines'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/a_Manage machine groups'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/input_searchMachine'), mgName)

WebUI.verifyElementText(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/span_mygroup1'), mgName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/span_Select'))

WebUI.waitForAngularLoad(30)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/button_Remove this machine gro'))

WebUI.verifyElementText(findTestObject('DeleteMachineGroup/Page_Amdocs GSS Value Pack/span_The Group was deleted suc'),'The Group was deleted successfully')

