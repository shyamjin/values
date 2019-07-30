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

WebUI.openBrowser('')

WebUI.navigateToUrl('http://localhost:8000/')

WebUI.openBrowser('')

WebUI.navigateToUrl('http://localhost:8000/')

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack (1)/input_uname'), 'superadmin')

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack (1)/input_pwd'), '12345')

WebUI.sendKeys(findTestObject('Page_Amdocs GSS Value Pack (1)/input_pwd'), Keys.chord(Keys.ENTER))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack (1)/button_vp-navaside__togglebtn'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack (1)/a_New DU'))

WebUI.setText(findTestObject('CreateDeploymentUnit/input_fa-fa1'), 'aaaaaa')

WebUI.click(findTestObject('CreateDeploymentUnit/button_CRM-BACKEND'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack (1)/span_CRM-BACKEND'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack (1)/div_Name'))

WebUI.closeBrowser()

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack/input_uname'), 'superadmin')

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack/input_pwd'), '12345')

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/input_login-button'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/div_vp-navaside__togglewrapper'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/a_New DU'))

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack/input_fa-fa1'), 'a')

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack/input_fa-FA1 (1)'), 'VV2a')

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/button_CRM-BACKEND'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/span_CRM-BACKEND'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/div_Name'))

WebUI.setText(findTestObject('Page_Amdocs GSS Value Pack/input_name'), 'asa')

WebUI.selectOptionByValue(findTestObject('Page_Amdocs GSS Value Pack/select_Fast TrackHot FixVersio'), '{"_id":{"$oid":"5a9ea4856980db41ac94a6c4"},"name":"Fast Track"}', 
    true)

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/button_Select'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/span_CRM-BACKEND'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/div_Name                      _1'))

WebUI.click(findTestObject('Page_Amdocs GSS Value Pack/input_login-button'))

WebUI.closeBrowser()

