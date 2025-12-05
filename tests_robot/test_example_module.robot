*** Settings ***
Documentation     Test suite generated for example_module
...               Traceability: REQ-101
Library           ../examples/src_project/example_module.py

*** Test Cases ***
Test add Basic
    [Documentation]    Basic positive test for add
    [Tags]    REQ-101
    ${result}=    add    1    1
    Should Not Be Equal    ${result}    ${None}

Test add Error
    [Documentation]    Verify error handling (expecting failure with bad args)
    [Tags]    REQ-101    Negative
    Run Keyword And Expect Error    * add    ${None}    ${None}


*** Settings ***
Documentation     Test suite generated for example_module
...               Traceability: REQ-102
Library           ../examples/src_project/example_module.py

*** Test Cases ***
Test safe_divide Basic
    [Documentation]    Basic positive test for safe_divide
    [Tags]    REQ-102
    ${result}=    safe_divide    0.5    0.5
    Should Not Be Equal    ${result}    ${None}

Test safe_divide Error
    [Documentation]    Verify error handling (expecting failure with bad args)
    [Tags]    REQ-102    Negative
    Run Keyword And Expect Error    * safe_divide    ${None}    ${None}


*** Settings ***
Documentation     Test suite generated for example_module
...               Traceability: REQ-103
Library           ../examples/src_project/example_module.py

*** Test Cases ***
Test square Basic
    [Documentation]    Basic positive test for square
    [Tags]    REQ-103
    ${result}=    square    1
    Should Not Be Equal    ${result}    ${None}

Test square Error
    [Documentation]    Verify error handling (expecting failure with bad args)
    [Tags]    REQ-103    Negative
    Run Keyword And Expect Error    * square    ${None}
