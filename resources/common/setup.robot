*** Settings ***

Library    ../../libraries/PerfectoLibrary.py
Resource   ../../resource/variables/global.robot


*** Keywords ***

Open Mobile Application

    [Documentation]    Starts Appium session on Perfecto device

    Open Application    ${PLATFORM}
