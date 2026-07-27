*** Settings ***
Resource    ../../resources/keywords/CommonKeywords.robot
Resource    ../../resources/keywords/LoginKeywords.robot

Test Setup       Launch Mobile Application
Test Teardown    Close The Mobile Application


*** Test Cases ***

Valid User Should Be Able To Login
    [Tags]    smoke    login
    Login To Application
    Login Should Be Successful
    

Invalid User Should Not Be Able To Login
    [Tags]    negative    login
    Login With Invalid Credentials
    ...    invalid_user
    ...    invalid_password
    Invalid Login Message Should Be Displayed