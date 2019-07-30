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
import org.openqa.selenium.Keys as Keys
import org.apache.commons.lang.RandomStringUtils as RandomStringUtils
import internal.GlobalVariable as GlobalVariable

CustomKeywords.'helper.Initializer.initWebUI'()

String randomString = RandomStringUtils.randomAlphanumeric(7)

String mgName = 'mg' + randomString

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

String machineName1 = WebUI.callTestCase(findTestCase('CreateMachine'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.navigateToUrl(GlobalVariable.envUrl)

String machineName2 = WebUI.callTestCase(findTestCase('CreateMachine'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.navigateToUrl(GlobalVariable.envUrl)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/a_Manage machines'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/a_Create new machine group'))

WebUI.setText(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/input_group_name'), mgName)

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/span_Add machines'))

WebUI.setText(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/input_vp-tooldepqeditpopup__in'), machineName1)

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/label_machineselect'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/button_Apply'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/span_Add machines'))

WebUI.setText(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/input_vp-tooldepqeditpopup__in'), machineName2)

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/label_machineselect'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/button_Apply'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/div_Select'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/firstFAfirstcheck'))

WebUI.click(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/button_Create machine group'))

WebUI.verifyElementText(findTestObject('CreateMachineGroup/Page_Amdocs GSS Value Pack/SuccessPopup'), 'The machine groups is saved successfully')

return mgName
