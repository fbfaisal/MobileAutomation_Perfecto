
*** Settings ***
Library    ../pages/LoginPage.py
Library    ../../libraries/MobileLibrary.py
*** Keywords ***

Login To Application
    Open Mobile Application
    Enter Username    ${USERNAME}
    Enter Password    ${PASSWORD}
    Tap Login

Home Screen Should Be Displayed