package internal

import com.kms.katalon.core.configuration.RunConfiguration
import com.kms.katalon.core.testobject.ObjectRepository as ObjectRepository
import com.kms.katalon.core.testdata.TestDataFactory as TestDataFactory
import com.kms.katalon.core.testcase.TestCaseFactory as TestCaseFactory
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import static com.kms.katalon.core.testdata.TestDataFactory.findTestData
import static com.kms.katalon.core.testcase.TestCaseFactory.findTestCase

/**
 * This class is generated automatically by Katalon Studio and should not be modified or deleted.
 */
public class GlobalVariable {
     
    /**
     * <p></p>
     */
    public static Object envUrl
     
    /**
     * <p></p>
     */
    public static Object globalUser
     
    /**
     * <p></p>
     */
    public static Object globalPassword
     
    /**
     * <p></p>
     */
    public static Object sameBrowser
     
    /**
     * <p></p>
     */
    public static Object browserIsUp
     

    static {
        def allVariables = [:]        
        allVariables.put('default', ['envUrl' : 'http://localhost:8000', 'globalUser' : 'admin', 'globalPassword' : '12345', 'sameBrowser' : true, 'browserIsUp' : false])
        allVariables.put('gitpipeline', allVariables['default'] + ['envUrl' : '##ENV_URL##', 'globalUser' : 'admin', 'globalPassword' : '12345', 'sameBrowser' : true, 'browserIsUp' : false])
        allVariables.put('illin4489', allVariables['default'] + ['envUrl' : 'http://illin4489:8020', 'globalUser' : 'admin', 'globalPassword' : '12345', 'sameBrowser' : true, 'browserIsUp' : false])
        
        String profileName = RunConfiguration.getExecutionProfile()
        
        def selectedVariables = allVariables[profileName]
        envUrl = selectedVariables['envUrl']
        globalUser = selectedVariables['globalUser']
        globalPassword = selectedVariables['globalPassword']
        sameBrowser = selectedVariables['sameBrowser']
        browserIsUp = selectedVariables['browserIsUp']
        
    }
}
