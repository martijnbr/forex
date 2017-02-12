from pyoanda import Client, PRACTICE

def practice ( ):
    con = Client(
        environment = PRACTICE,
        account_id = "5828851",
        access_token = "1781315285cf9234a14e0f7434cb7abf-7fa1e5faf584a0cbfc79553e7c2b0c2b"
    )
    return con