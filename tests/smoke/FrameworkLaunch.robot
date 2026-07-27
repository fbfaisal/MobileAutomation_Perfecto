*** Settings ***

Resource    ../../resource/common/setup.robot
Resource    ../../resource/common/teardown.robot


Suite Setup       Open Mobile Application
Suite Teardown    Close Mobile Application


*** Test Cases ***

Verify Framework Launch

    Log    Framework connected successfully
