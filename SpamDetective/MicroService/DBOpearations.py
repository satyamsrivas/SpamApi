import psycopg2
from faker import Faker

fake = Faker()

def generate_dummy_data(num_users=50, num_contacts=20, num_spam=10):
    # Connect to the PostgreSQL database
    print(fake.name())
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres@321'
    )
    cursor = conn.cursor()

    for _ in range(num_users):
        phone_number = fake.unique.phone_number()
        name = fake.name()
        email = fake.email()

        # Insert data into the CustomUser table
        cursor.execute(
            'INSERT INTO "SpamDetect_customuser" (phone_number, password, name,email,is_active,is_staff)'
            "VALUES (%s, %s, %s, %s,%s,%s)",
            (phone_number, 'password', name, email,True,True)
        )

    for _ in range(num_contacts):
        # Get a random user from the CustomUser table
        cursor.execute('SELECT id FROM "SpamDetect_customuser" ORDER BY RANDOM() LIMIT 1')
        user_id = cursor.fetchone()[0]

        name = fake.name()
        phone_number = fake.phone_number()
        email = fake.email()

        # Insert data into the Contact table
        cursor.execute(
            'INSERT INTO "SpamDetect_contact" (user_id, name, phone_number, email) '
            "VALUES (%s, %s, %s, %s)",
            (user_id, name, phone_number, email)
        )

    for _ in range(num_spam):
        number = fake.unique.phone_number()

        # Insert data into the Spam table
        cursor.execute(
            'INSERT INTO "SpamDetect_spam" (number) VALUES (%s)',
            (number,)
        )

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate_dummy_data()
    print("DATA IS PUSHED IN THE DB")
