*** Settings ***
Library    ../../libraries/MobileLibrary.py


*** Keywords ***

Launch Mobile Application
    Open Mobile Application

Close The Mobile Application
    Close Mobile Application

Verify Mobile Session Is Active
    Mobile Session Should Be Active

Verify Mobile Session Is Closed
    Mobile Session Should Not Be Active

Capture Current Screen
    [Arguments]    ${name}=mobile_screen
    Capture Mobile Screenshot    ${name}