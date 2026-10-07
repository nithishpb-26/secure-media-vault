from database.database import (
    create_database,
    save_history,
    get_history
)


print("Creating database...")

create_database()

print("Saving test record...")

save_history(
    "test.jpg",
    "ENCRYPT",
    "SUCCESS",
    1024
)

print("\nEncryption History:")

records = get_history()

for record in records:
    print(record)

print("\nDatabase test completed!")