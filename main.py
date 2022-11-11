import json
import uuid
import requests
import connection


# car api
url = "https://car-api2.p.rapidapi.com/api/trims"
# url https://car-api2.p.rapidapi.com/api/trims followed by id number will give the record of te tabels from the api
querystring = {"verbose":"yes","sort":"id","direction":"asc","limit":"25","year":2020}
#  taking 25 records from api with year set as 2020

# host and api key
headers = {
	"X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
	"X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# fetcing ids from api for each record
information= response.json()["data"]

database_value = []
# fetching data from api using ids for all the required tabels
for i in range (0,25):
	url="https://car-api2.p.rapidapi.com/api/trims/"+ str(information[i]['id'])
	response = requests.request("GET", url, headers=headers, params=querystring)
	database_value.append(response.json())

database_value = json.dumps(database_value)
f = open("car.json","w")
f.write(database_value)
f.close()

f = open("car.json", "r")
car_data = json.loads(f.read())
cursor = connection.mydb1.cursor()

def check_table_if_exists():
	cursor.execute("Show tables like 'vehicle'")
	check_tables = cursor.fetchone()
	if check_tables:
		return True
	else:
		return False

check = check_table_if_exists()
if check == True:
	print("Table already exists")
else:

	cursor.execute(
		"CREATE TABLE vehicle("
		"id varchar(255) NOT NULL,"
		"year int(10),"
		"name varchar(255),"
		"description varchar(255),"
		"msrp varchar(255),"
		"invoice varchar(255),"
		"PRIMARY KEY(id))"
	)

	cursor.execute(
		"CREATE TABLE engine("
		"engine_id varchar(255) NOT NULL, "
		"type varchar(255),"
		"fuel_type varchar(255),"
		"cylinders varchar(10),"
		"size int(20),"
		"horsepower_hp  int(20),"
		"horsepower_rpm int(20),"
		"cam_typ varchar(255),"
		"transmission varchar(255),"
		"e_id varchar(255),"
		"PRIMARY KEY (engine_id),"
		"FOREIGN KEY (e_id) references vehicle (id))"
	)

	cursor.execute(
		"CREATE TABLE BODY("
		"body_id varchar(255),"
		"type varchar(255),"
		"doors int(20),"
		"length int(20),"
		"width int(20),"
		"seats int(20),"
		"ground_clearance int(20),"
		"cargo_capacity int(20),"
		"wheal_base int(20),"
		"b_id varchar(255),"
		"primary key (body_id),"
		"foreign key (b_id) references vehicle (id))"
	)

	cursor.execute(
		"CREATE TABLE mileage("
		"mileage_id varchar(255),"
		"fuel_tankk_capacity varchar(255),"
		"range_city varchar(255),"
		"range_highway varchar(255),"
		"m_id varchar(255),"
		"primary key(mileage_id),"
		"foreign key (m_id) references vehicle (id))"
	)

	cursor.execute(
		"CREATE TABLE colour("
		"colour_id  varchar(255) not null ,"
		"col_name varchar(255),"
		"rgb varchar(255),"
		"c_id varchar(255),"
		"primary key (colour_id),"
		"foreign key (c_id) references vehicle(id))"
	)
	for item in car_data:
		# vehicle table
		# print('data-----',item['id'])
		id = item['id']
		year = item['year']
		name = item['name']
		description = item['description']
		msrp = item['msrp']
		invoice = item['invoice']
		cursor.execute(
			"INSERT INTO vehicle (id, year, name, description, msrp, invoice) values (%s,%s,%s,%s,%s,%s)",
			(id, year, name, description, msrp, invoice)
		)
		connection.mydb1.commit()

	for item in car_data:
		# body
		b_id = item['id']
		body_id = str(uuid.uuid4())
		body_type = item['make_model_trim_body']['type']
		doors = item['make_model_trim_body']['doors']
		length = item['make_model_trim_body']['length']
		width = item['make_model_trim_body']['width']
		seats = item['make_model_trim_body']['seats']
		ground_clearance = item['make_model_trim_body']['ground_clearance']
		cursor.execute(
			"INSERT INTO body (body_id,type,doors,length,width,seats,ground_clearance,b_id) values (%s,%s,%s,%s,%s,%s,%s,%s)",
			(body_id, body_type, doors, length, width, seats, ground_clearance, b_id)
		)
		connection.mydb1.commit()

	for item in car_data:
		# engine
		e_id = item['id']
		engine_id = str(uuid.uuid4())
		engine_type = item['make_model_trim_engine']['engine_type']
		fuel_type = item['make_model_trim_engine']['fuel_type']
		cylinders = item['make_model_trim_engine']['cylinders']
		size = item['make_model_trim_engine']['size']
		horsepower_hp = item['make_model_trim_engine']['horsepower_hp']
		horsepower_rpm = item['make_model_trim_engine']['horsepower_rpm']
		cam_typ = item['make_model_trim_engine']['cam_type']
		transmission = item['make_model_trim_engine']['transmission']
		cursor.execute(
			"INSERT INTO engine(engine_id,type,fuel_type,cylinders,size,horsepower_hp,horsepower_rpm,cam_typ,transmission,e_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
			(engine_id, engine_type, fuel_type, cylinders, size, horsepower_hp, horsepower_rpm, cam_typ, transmission,
			 e_id)
		)
		connection.mydb1.commit()

	for item in car_data:
		# mileage
		m_id = item['id']
		mileage_id = str(uuid.uuid4())
		fuel_tank_capacity = item['make_model_trim_mileage']['fuel_tank_capacity']
		range_city = item['make_model_trim_mileage']['range_city']
		range_highway = item['make_model_trim_mileage']['range_highway']
		cursor.execute(
			"INSERT INTO mileage(mileage_id,fuel_tankk_capacity,range_city,range_highway,m_id) values (%s,%s,%s,%s,%s)",
			(mileage_id, fuel_tank_capacity, range_city, range_highway, m_id)
		)
		connection.mydb1.commit()

