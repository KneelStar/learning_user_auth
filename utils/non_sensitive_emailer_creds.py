def get_smpt_server_of(sender:str):
    sender_dict = {"DEFAULT_EMAIL":"smtp.gmail.com"}
    return sender_dict[sender]

def get_smpt_port_of(sender:str):
    sender_dict = {"DEFAULT_EMAIL":465}
    return sender_dict[sender]

def get_smpt_username_of(sender:str):
    sender_dict = {"DEFAULT_EMAIL":"xxxxxxx@gmail.com"}
    return sender_dict[sender]

def get_smpt_password_of(sender:str):
    sender_dict = {"DEFAULT_EMAIL":"xxx_app_password_xxx"}
    return sender_dict[sender]