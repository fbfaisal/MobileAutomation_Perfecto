*** Settings ***
Library    ../../libraries/MobileLibrary.py
Library    ../../libraries/LocatorReader.py


*** Keywords ***

Enter Username On Login Page
    [Arguments]    ${username}
    ${locator}=    Get Locator    login    username_field
    Input Mobile Text    ${locator}    ${username}

Enter Password On Login Page
    [Arguments]    ${password}
    ${locator}=    Get Locator    login    password_field
    Input Mobile Text    ${locator}    ${password}

Tap Login Button
    ${locator}=    Get Locator    login    login_button
    Click Mobile Element    ${locator}

Login Error Should Be Displayed
    ${locator}=    Get Locator    login    error_message
    Mobile Element Should Be Visible    ${locator}

Invalid Login Message Should Be Displayed
    ${locator}=    Get Locator    login    error_message
    Mobile Element Should Be Visible    ${locator}
    
Login Page Should Be Displayed
    ${locator}=    Get Locator    login    login_button
    Mobile Element Should Be Visible    ${locator}