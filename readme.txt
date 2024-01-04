This is a learning excersie for me to learn how user authentication works. 

Basic Goals:
    Signup
    Login
    Remember Me
    Logout
    Logout everywhere
    Forgot Password
    Reset Password

Advanced goals:
    Email Verification
    Rate Limiting
    2 Step Verification
    Biometric Verification
    Single Sign On
    Reduce session db quries by implementing jwt like features

Running the code:
1. Create a database with the following schema and the credentials in db.py
2. Use the ./run command to start the flask website
3. Use postman to send the queries (you will need to manually add nonces in database to complete requests successfully) 

Database Schema for this excersie:

-- User Table
CREATE TABLE Users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    passwordSalt VARCHAR(50) NOT NULL,
    isEmailVerified BOOLEAN DEFAULT 0,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Reset Password Table
CREATE TABLE ResetPasswords (
    resetTokenID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    resetToken VARCHAR(100) NOT NULL,
    resetTokenExpiry TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 HOUR),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- Email Verification Table
CREATE TABLE EmailVerifications (
    verificationID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    verificationToken VARCHAR(100) NOT NULL,
    verificationTokenExpiry TIMESTAMP NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- Session Table 
CREATE TABLE Sessions (
    sessionID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    sessionToken VARCHAR(100) NOT NULL,
    sessionExpiry TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 DAY),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- Two-Factor Authentication Table
CREATE TABLE TwoFactorAuth (
    userID INT PRIMARY KEY,
    twoFactorEnabled BOOLEAN DEFAULT 0,
    twoFactorMethod VARCHAR(50), -- TOTP, SMS, Email, etc.
    twoFactorSecretKey VARCHAR(255),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

-- Nonce table
CREATE TABLE Nonces (
    nonceID INT AUTO_INCREMENT PRIMARY KEY,
    nonce_value VARCHAR(255) NOT NULL,
    expiration_time TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 5 HOUR)
);

Learning Sources Used:
    Build a User Login System with Flask and MongoDB:
        https://www.youtube.com/playlist?list=PL4JDh0LtP7jr0nNuoW-KB-O2uABkaMhL1
    
    Session vs Token Authentication in 100 Seconds:
        https://youtu.be/UBUNrFtufWo?si=oELr4RowuE496C3
    
    What Is Single Sign-on (SSO)? How It Works:
        https://youtu.be/O1cRJWYF-g4?si=pTQaj3rIeR-CIs8c
    
    "Basic Authentication" in Five Minutes:
        https://youtu.be/rhi1eIjSbvk?si=sCaV7UX6E3B6W0HM
    
    Design a Simple Authentication System | System Design Interview Prep:
        https://youtu.be/uj_4vxm9u90?si=DepUqPBHmS5Y_CqM
    
    How to Store JWT for Authentication:
        https://youtu.be/iD49_NIQ-R4?si=ORXCto71d92VcH-x
    
    OAuth terminologies and flows explained - OAuth tutorial - Java Brains:
        https://youtu.be/3pZ3Nh8tgTE?si=sGmPEwUes9PH1AYB
    
    OAuth 2 Explained In Simple Terms:
        https://youtu.be/ZV5yTm4pT8g?si=e_rZpjG5FBKhQazc
    
    Stop using JSON Web Tokens. Use Cookies & Server Sessions instead:
        https://youtu.be/FVmxtmzyrSw?si=IxOpWStgQ8nmEh2l
    
    How to Create a Secure REST API with Node.js and Express:
        https://youtu.be/Tw5LupcpKS4?si=Sk3qjbEq2uq1pk7S
    
    Flask Blueprints Make Your Apps Modular & Professional:
        https://www.youtube.com/watch?v=_LMiUOYDxzE

    How to Send Emails in Python with Gmail:
        https://mailtrap.io/blog/python-send-email-gmail/
        
    https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_modal
    
    ChatGpt

Side note, these are the commands to create a virtual env, and start the virtual env
    Create: python3 -m venv {vemv_name}
    Start: source {path_to_venv}/{venv_name}/bin/activate
