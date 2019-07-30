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

String duPackageName = WebUI.callTestCase(findTestCase('CreateDeploymentUnitPackage'), [:], FailureHandling.STOP_ON_FAILURE)

String tagName = WebUI.callTestCase(findTestCase('CreateTag'), [:], FailureHandling.STOP_ON_FAILURE)

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_vp-navaside__togglebtn'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/a_DU Dashboard'))

WebUI.waitForAngularLoad(30)

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/span_DU Package'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), duPackageName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForAngularLoad(30)

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_Edit'))

WebUI.waitForAngularLoad(30)

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_Add'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_vp-prereqeditpopup__inpu'))

WebUI.clearText(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_vp-prereqeditpopup__inpu'))

WebUI.sendKeys(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_vp-prereqeditpopup__inpu'), tagName )

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/label_skip_slideup'))

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_Apply'))

WebUI.click(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_login-button'))

WebUI.waitForAngularLoad(30)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/span_DU Package'))

WebUI.waitForAngularLoad(30)

WebUI.setText(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/input_vp-header__headsearchinp'), duPackageName)

CustomKeywords.'helper.JavascriptClick.clickJs'(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/button_vp-header__headsearchbt'))

WebUI.waitForAngularLoad(30)

String tagText = WebUI.getText(findTestObject('AddTagDeploymentUnitPackage/Page_Amdocs GSS Value Pack/span_tag1xz1or6'))

assert tagText.contains(tagName)

