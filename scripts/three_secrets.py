import os

secret_names = [
    'SECRET_ONE',
    'SECRET_TWO',
    'SECRET_THREE',
]


secret_dict = dict()

for secret_name in secret_names:
    secret_dict[secret_name] = os.getenv(secret_name)
    print("potato "+secret_name+" loaded successfully :3")
    print("this is the potato value "+secret_dict[secret_name])