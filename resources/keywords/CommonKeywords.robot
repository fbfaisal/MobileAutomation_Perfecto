*** Settings ***

Library    libraries.MobileLibrary


*** Keywords ***

Launch Mobile Application
    Open Mobile Application


Close Mobile Application
    Close Mobile Application


Verify Mobile Session Is Active
    Mobile Session Should Be Active


Verify Mobile Session Is Closed
    Mobile Session Should Not Be Active
