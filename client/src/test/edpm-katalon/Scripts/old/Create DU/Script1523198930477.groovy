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

import org.openqa.selenium.chrome.ChromeDriver as ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions as ChromeOptions
import org.openqa.selenium.remote.DesiredCapabilities as DesiredCapabilities
import com.kms.katalon.core.webui.driver.DriverFactory as DriverFactory

//Set chromedriver path
ChromeOptions options = new ChromeOptions()
options.addArguments(['--headless', '--window-size=1920,1080'])

DesiredCapabilities capabilities = new DesiredCapabilities()

capabilities.setCapability(ChromeOptions.CAPABILITY, options)

System.setProperty('webdriver.chrome.driver', GlobalVariable.chromeWebdriverPath)

ChromeDriver driver = new ChromeDriver(capabilities)

DriverFactory.changeWebDriver(driver)

WebUI.navigateToUrl(GlobalVariable.envUrl)

WebUI.setText(findTestObject('CreateDeploymentUnit/input_uname'), 'admin')

WebUI.setText(findTestObject('CreateDeploymentUnit/input_pwd'), '12345')

WebUI.sendKeys(findTestObject('CreateDeploymentUnit/input_pwd'), Keys.chord(Keys.ENTER))

WebUI.delay(2)

WebUI.click(findTestObject('CreateDeploymentUnit/button_vp-navaside__togglebtn'))

WebUI.delay(1)

WebUI.click(findTestObject('CreateDeploymentUnit/a_New DU'))

WebUI.delay(1)

WebUI.setText(findTestObject('CreateDeploymentUnit/input_name'), 'test-du-' + System.currentTimeMillis())

WebUI.selectOptionByLabel(findTestObject('CreateDeploymentUnit/select_Fast TrackHot FixVersio'), 'Fast Track', false)

WebUI.setText(findTestObject('CreateDeploymentUnit/textarea_vp-teamsform___teamde'), 'desc')

WebUI.setText(findTestObject('CreateDeploymentUnit/input_branch'), 'branch')

//WebUI.click(findTestObject('CreateDeploymentUnit/button_Add'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/label_a'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/button_Apply'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/button_Add'))
//
//WebUI.click(findTestObject('null'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/button_Apply'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/span_Add'))
//
//WebUI.setText(findTestObject('CreateDeploymentUnit/input_input_name'), 'f')
//
//WebUI.selectOptionByValue(findTestObject('CreateDeploymentUnit/select_textpasswordemaildatech'), 'text', true)
//
//WebUI.setText(findTestObject('CreateDeploymentUnit/input_field_default_value'), 'v')

//WebUI.setText(findTestObject('CreateDeploymentUnit/input_tooltip'), 't')

//WebUI.click(findTestObject('CreateDeploymentUnit/button_Done'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/button_Select'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/span_CRM-BACKEND'))
//
//WebUI.click(findTestObject('CreateDeploymentUnit/div'))
//

WebUI.setText(findTestObject('CreateDeploymentUnit/input_fa-fa1'), 'aaaaaa')

//WebUI.click(findTestObject('CreateDeploymentUnit/button_CRM-BACKEND'))
//WebUI.click(findTestObject('CreateDeploymentUnit/span_CRM-BACKEND'))

WebUI.click(findTestObject('CreateDeploymentUnit/input_vp-dttoolbar__savebtn vp'))

WebUI.delay(2)

assert WebUI.getUrl().contains('deploymentunit/view')

WebUI.closeBrowser()

