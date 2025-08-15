from constants import secret_names
import os

def load_and_print_secrets():
    '''harry potter'''
    secret_dict = dict()

    for secret_name in secret_names:
        secret_dict[secret_name] = os.getenv(secret_name)
        print("potato "+secret_name+" loaded successfully :3")
        print("this is the potato value "+secret_dict[secret_name])