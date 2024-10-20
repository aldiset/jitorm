import json
from faker import Faker

# Inisialisasi Faker
fake = Faker()

# Jumlah data dummy yang ingin dibuat
jumlah_data = 100000

# Membuat data dummy
data_dummy = []
for _ in range(jumlah_data):
    data = {
        "name": fake.name(),
        "username":fake.user_name(),
        "password":fake.password(),
        "address": fake.address(),
        "email": fake.email(),
        "job": fake.job(),
        "phone_number": fake.phone_number(),
        "birthdate": fake.date_of_birth().isoformat()
    }
    data_dummy.append(data)

# Menyimpan data dummy ke dalam file JSON
with open('data_dummy.json', 'w') as json_file:
    json.dump(data_dummy, json_file, indent=4)

print(f"Data dummy sebanyak {jumlah_data} berhasil disimpan ke dalam file 'data_dummy.json'")
