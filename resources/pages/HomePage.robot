*** Settings ***
Library    ../../libraries/MobileLibrary.py
Library    ../../libraries/LocatorReader.py


*** Keywords ***

Home Page Should Be Displayed
    ${locator}=    Get Locator    home    home_title
    Mobile Element Should Be Visible    ${locator}

Get Account Balance
    ${locator}=    Get Locator    home    account_balance
    ${balance}=    Get Mobile Element Text    ${locator}
    RETURN    ${balance}

Tap Accounts Menu
    ${locator}=    Get Locator    home    accounts_menu
    Click Mobile Element    ${locator}
