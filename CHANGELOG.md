## [Version 1.0] - 2024-09-17
### Introducing the application
- DB setup files added
- Driver code added
- UI template files defined
- Form-based input supported for HTTP requests

### Issues faced
- Message box diplaying "None" at home page during initial loading
    - **Status**: resolved - no such message box pops up now on intitial entry to home page


- In alert message for an operation, quoted fields were being encoded by Jinja as a typical sanity measure
    - **Status**: resolved - messages with quotes around keywords are now displayable to the user/client 
