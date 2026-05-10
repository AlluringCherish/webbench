"""
Implement the function to read the list of users from the 'users.txt' file.
This function reads the file line by line, splits each line by the pipe delimiter '|',
and constructs a list of user dictionaries with keys: 'username', 'email', 'phone', 'address'.
Returns:
    list of dict: List containing user information dictionaries.
"""
import os
DATA_DIR = 'data'
def read_users():
    users = []
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'phone': parts[2],
                        'address': parts[3]
                    })
    return users