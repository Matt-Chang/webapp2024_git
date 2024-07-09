# Project Pipeline
![Alt text](https://github.com/Matt-Chang/webapp2024_git/blob/main/Untitled%20diagram-2024-07-09-030557.png)

1. **Project Planning and Design**
    - Conceptualized the online payment system with features like sending money, requesting money, and managing accounts.
    - Defined key functions such as virtual account management, initial funds and currency selection, user registration, direct payments, payment requests, transaction history, currency conversion, and security measures.

2. **Presentation Layer**
    - Developed templates for user and administrator interactions.
    - Implemented views for users to see transactions, make direct payments, and request payments.
    - Ensured error handling for invalid actions like transferring money to oneself or entering wrong usernames.

3. **Business Logic Layer**
    - Created views containing the logic that accesses the model and defers to the appropriate templates.
    - Implemented PointsTransfer model to manage transactions with fields like receiver, amount of money transferred, and timestamp.
    - Developed forms to capture user inputs and validate anomalies.

4. **Data Access Layer**
    - Utilized SQLite as the Relational DataBase Management System (RDBMS) for data storage and retrieval.
    - Designed models to represent and access data effectively.

5. **Security Layer**
    - Implemented user authentication functionalities including registration, login, and logout.
    - Restricted access to web pages for unauthorized users.
    - Established HTTPS for secure communication.
    - Incorporated protections against cross-site scripting (XSS), cross-site request forgery (CSRF), SQL injection, and clickjacking.

6. **Web Services**
    - Developed a RESTful web service for currency conversion, allowing GET requests to convert between currencies using hard-coded rates.
    - Deployed the service on the same server for access by the business logic layer.

7. **Remote Procedure Call (RPC)**
    - Integrated a Thrift timestamp service to timestamp all transactions by accessing a remote Thrift server.

8. **Cloud Deployment**
    - Successfully deployed the application on an Amazon EC2 virtual machine.
    - Provided screenshots and documentation of commands issued on the console to run the Django web application on the cloud.
  

