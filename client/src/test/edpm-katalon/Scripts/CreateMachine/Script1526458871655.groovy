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

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

String randomString = RandomStringUtils.randomAlphanumeric(7)

String machineName = 'm' + randomString

String machineHost = 'h' + randomString

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/a_Manage machines'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/a_Create a new machine'))

WebUI.setText(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/input_machine_name'), machineName)

WebUI.setText(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/input_ip'), '127.0.0.1')

WebUI.delay(5)

WebUI.selectOptionByIndex(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/select_ProductionIUTUTSTValue'), '1', 
    FailureHandling.STOP_ON_FAILURE)

WebUI.setText(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/input_host_name'), machineHost)

WebUI.setText(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/input_username'), 'usertest1')

WebUI.selectOptionByValue(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/select_password'), 'ssh', true)

WebUI.selectOptionByIndex(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/select_Not required'), '1',
	FailureHandling.STOP_ON_FAILURE)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/button_Create machine'))

WebUI.verifyElementText(findTestObject('CreateMachine/Page_Amdocs GSS Value Pack/addMachineSuccessPopup'), 'The machine is added successfully')

return machineName

