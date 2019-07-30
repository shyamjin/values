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

String randomNumber = RandomStringUtils.randomNumeric(5)

String teamName = 'Team' + randomNumber

WebUI.callTestCase(findTestCase('Login'), [:], FailureHandling.STOP_ON_FAILURE)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/a_Manage users  teams'))

WebUI.click(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/a_Teams'))

WebUI.click(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/button_Add teams'))

WebUI.setText(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/input_vp-userform__nameinput'), teamName)

WebUI.setText(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/textarea_vp-usergroupform___te'), 'Katalon CreateTeam Auto Test')

WebUI.setText(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/input_vp-userform__distributio'), randomNumber + '@aaa.com')

WebUI.selectOptionByValue(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/select_--- Select default home'), 'DU Dashboard', true)

WebUI.click(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/button_Add user group'))

WebUI.verifyElementText(findTestObject('CreateTeam/Page_Amdocs GSS Value Pack/span_The team is created succe'), 'The team is created successfully')

return teamName

