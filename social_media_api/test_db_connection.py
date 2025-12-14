import psycopg2

# Database connection details
conn = psycopg2.connect(
    host="social-media-db.cqvgasue4pwp.us-east-1.rds.amazonaws.com",
    port=5432,
    database="postgres",
    user="dbadmin",
    password="Yxuc9GwqJQOjNIdFf4Be"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print("PostgreSQL version:", cursor.fetchone()[0])

# List all tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")
print("\nTables in database:")
for table in cursor.fetchall():
    print(f"  - {table[0]}")

cursor.close()
conn.close()
print("\nConnection successful!")
