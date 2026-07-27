
*** Settings ***
Resource    ../pages/LoginPage.robot
Resource    ../pages/HomePage.robot
Resource    ../variables/global.robot


*** Keywords ***

Login To Application
    [Arguments]    ${username}=${USERNAME}    ${password}=${PASSWORD}
    Login Page Should Be Displayed
    Enter Username On Login Page    ${username}
    Enter Password On Login Page    ${password}
    Tap Login Button

Login Should Be Successful
    Home Page Should Be Displayed

Login With Invalid Credentials
    [Arguments]    ${username}    ${password}
    Enter Username On Login Page    ${username}
    Enter Password On Login Page    ${password}
    Tap Login Button

