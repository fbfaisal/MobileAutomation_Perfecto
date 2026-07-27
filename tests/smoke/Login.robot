*** Settings ***
Resource    ../../resources/keywords/LoginKeywords.robot

*** Test Cases ***

Valid Login
    Login To Application
    Home Screen Should Be Displayed