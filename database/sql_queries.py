count_if_username_exist_in_db = "SELECT COUNT(*) FROM Users WHERE username = %s"
count_if_email_exist_in_db = "SELECT COUNT(*) FROM Users WHERE email = %s"
count_if_non_expired_nonce_exist_in_db = "SELECT COUNT(*) FROM Nonces WHERE nonce_value = %s AND expiration_time > NOW()"
count_if_session_exist_in_db = "SELECT COUNT(*) FROM Sessions WHERE sessionToken = %s"

delete_nonce = "DELETE FROM Nonces WHERE nonce_value = %s"
delete_one_session = "DELETE FROM Sessions WHERE userID = %s AND sessionToken = %s"
delete_all_sessions = "DELETE FROM Sessions WHERE userID = %s"

add_user_to_db = "INSERT INTO Users (username, email, passwordHash, passwordSalt) VALUES (%s, %s, %s, %s)"
add_email_verification_token_to_email_veri_table = "INSERT INTO EmailVerifications (userID, verificationToken) VALUES (%s, %s)"
add_reset_pass_token_with_userID = "INSERT INTO ResetPasswords (userID, resetToken) VALUES (%s, %s)"

get_user_id_using_username = "SELECT userID FROM Users WHERE username = %s"
get_user_id_using_email = "SELECT userID FROM Users WHERE email = %s"
get_user_id_using_session_token = "SELECT userID FROM Sessions WHERE sessionToken = %s"
get_username_using_user_id = "SELECT username FROM Users WHERE userID = %s"
get_email_using_username = "SELECT email FROM Users WHERE username = %s"
get_password_hash_using_user_id = "SELECT passwordHash FROM Users WHERE userID = %s"

create_regular_session_using_userid = "INSERT INTO Sessions (userID, sessionToken) VALUES (%s, %s)"
create_week_long_session_using_userid = "INSERT INTO Sessions (userID, sessionToken, sessionExpiry) VALUES (%s, %s, CURRENT_TIMESTAMP + INTERVAL 1 WEEK)"
