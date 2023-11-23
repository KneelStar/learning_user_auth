This is a learning excersie for me to learn how user authentication works. 

Basic Goals:
    Signup
    Login
    Remember Me
    Forgot Password

Advanced goals:
    Email Verification
    2 Step Verification
    Biometric Verification
    Single Sign On


Database Schema for this excersie:

-- User Table
CREATE TABLE Users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    passwordSalt VARCHAR(50) NOT NULL,
    resetPasswordToken VARCHAR(100),
    resetPasswordTokenExpiry TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 HOUR) ,
    isEmailVerified BOOLEAN DEFAULT 0,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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
    sessionExpiry TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 MONTH),
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
    https://www.youtube.com/playlist?list=PL4JDh0LtP7jr0nNuoW-KB-O2uABkaMhL1
    ChatGpt

Side note, these are the commands to create a virtual env, and start the virtual env
    Create: python3 -m venv {vemv_name}
    Start: source {path_to_venv}/{venv_name}/bin/activate