package helper

import static com.kms.katalon.core.checkpoint.CheckpointFactory.findCheckpoint
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject

import com.kms.katalon.core.annotation.Keyword
import com.kms.katalon.core.checkpoint.Checkpoint
import com.kms.katalon.core.checkpoint.CheckpointFactory
import com.kms.katalon.core.mobile.keyword.MobileBuiltInKeywords
import com.kms.katalon.core.model.FailureHandling
import com.kms.katalon.core.testcase.TestCase
import com.kms.katalon.core.testcase.TestCaseFactory
import com.kms.katalon.core.testdata.TestData
import com.kms.katalon.core.testdata.TestDataFactory
import com.kms.katalon.core.testobject.ObjectRepository
import com.kms.katalon.core.testobject.TestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords

import internal.GlobalVariable

import MobileBuiltInKeywords as Mobile
import WSBuiltInKeywords as WS
import WebUiBuiltInKeywords as WebUI

import org.openqa.selenium.chrome.ChromeDriver as ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions as ChromeOptions
import org.openqa.selenium.remote.DesiredCapabilities as DesiredCapabilities
import com.kms.katalon.core.webui.driver.DriverFactory as DriverFactory
import com.kms.katalon.core.webui.driver.WebUIDriverType as WebUIDriverType

public class Initializer {
	@Keyword
	public static initWebUI(){
		if (GlobalVariable.sameBrowser && GlobalVariable.browserIsUp) {
			WebUI.navigateToUrl(GlobalVariable.envUrl)
		} else {
			ChromeOptions options = new ChromeOptions()
			if (DriverFactory.getExecutedBrowser() == WebUIDriverType.HEADLESS_DRIVER) {
				options.addArguments('--headless',
						'--disable-gpu',
						'window-size=1920,1080'
						)
			} else {
				options.addArguments('--start-maximized',
						'--ignore-certificate-errors',
						'--disable-popup-blocking',
						'--incognito'
						)
			}
			DesiredCapabilities capabilities = new DesiredCapabilities()
			capabilities.setCapability(ChromeOptions.CAPABILITY, options)
			System.setProperty('webdriver.chrome.driver', DriverFactory.getChromeDriverPath())
			ChromeDriver driver = new ChromeDriver(capabilities)
			DriverFactory.changeWebDriver(driver)
			GlobalVariable.browserIsUp = true;
			WebUI.navigateToUrl(GlobalVariable.envUrl)
		}
	}
}
