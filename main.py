from prettytable import PrettyTable
import json
import uuid
import requests
import connection

class Main:
	def get_api_data(self):
		# car api
		url = "https://car-api2.p.rapidapi.com/api/trims"
		# url https://car-api2.p.rapidapi.com/api/trims followed by id number will give the record of the tabel from the api
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
		return database_value
	def write_data_file(self, database_value):
		f = open("car.json","w")
		f.write(database_value)
		f.close()
	def read_data_from_file(self):
		f = open("car.json", "r")
		car_data = json.loads(f.read())
		return car_data
	def connection_database(self):
		cursor = connection.mydb1.cursor()
		return cursor

class Database_calls(Main):
	def __int__(self,cursor):
		self.cursor = cursor
		self.main = Main()
	def check_table_if_exists(self, cursor):
		cursor.execute("Show tables like 'vehicle'")
		check_tables = cursor.fetchone()
		if check_tables:
			return True
		else:
			return False
	def create_table(self,cursor):
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
			"id varchar(255) NOT NULL, "
			"type varchar(255),"
			"fuel_type varchar(255),"
			"cylinders varchar(10),"
			"size int(20),"
			"horsepower_hp  int(20),"
			"horsepower_rpm int(20),"
			"cam_typ varchar(255),"
			"transmission varchar(255),"
			"e_id varchar(255),"
			"PRIMARY KEY (id),"
			"FOREIGN KEY (e_id) references vehicle (id))"
		)

		cursor.execute(
			"CREATE TABLE BODY("
			"id varchar(255),"
			"type varchar(255),"
			"doors int(20),"
			"length int(20),"
			"width int(20),"
			"seats int(20),"
			"ground_clearance int(20),"
			"b_id varchar(255),"
			"primary key (id),"
			"foreign key (b_id) references vehicle (id))"
		)

		cursor.execute(
			"CREATE TABLE mileage("
			"id varchar(255),"
			"fuel_tankk_capacity varchar(255),"
			"range_city varchar(255),"
			"range_highway varchar(255),"
			"m_id varchar(255),"
			"primary key(id),"
			"foreign key (m_id) references vehicle (id))"
		)

	def insert_data(self, car_data, cursor):
		# vehicle table
		for item in car_data:
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

		# body table
		for item in car_data:
			b_id = item['id']
			body_id = str(uuid.uuid4())
			body_type = item['make_model_trim_body']['type']
			doors = item['make_model_trim_body']['doors']
			length = item['make_model_trim_body']['length']
			width = item['make_model_trim_body']['width']
			seats = item['make_model_trim_body']['seats']
			ground_clearance = item['make_model_trim_body']['ground_clearance']
			cursor.execute(
				"INSERT INTO body (id,type,doors,length,width,seats,ground_clearance,b_id) values (%s,%s,%s,%s,%s,%s,%s,%s)",
				(body_id, body_type, doors, length, width, seats, ground_clearance, b_id)
			)
			connection.mydb1.commit()

		# engine table
		for item in car_data:
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
				"INSERT INTO engine(id,type,fuel_type,cylinders,size,horsepower_hp,horsepower_rpm,cam_typ,transmission,e_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
				(engine_id, engine_type, fuel_type, cylinders, size, horsepower_hp, horsepower_rpm, cam_typ, transmission,
				 e_id)
			)
			connection.mydb1.commit()
		# mileage table
		for item in car_data:
			m_id = item['id']
			mileage_id = str(uuid.uuid4())
			fuel_tank_capacity = item['make_model_trim_mileage']['fuel_tank_capacity']
			range_city = item['make_model_trim_mileage']['range_city']
			range_highway = item['make_model_trim_mileage']['range_highway']
			cursor.execute(
				"INSERT INTO mileage(id,fuel_tankk_capacity,range_city,range_highway,m_id) values (%s,%s,%s,%s,%s)",
				(mileage_id, fuel_tank_capacity, range_city, range_highway, m_id)
			)
			connection.mydb1.commit()
	def table_data(self, table_name, cursor):
		cursor.execute(f"SELECT * FROM {table_name}")
		table_data = cursor.fetchall()
		return table_data
	def display_table(self,table_name, table_data, cursor):
		column = dbcalls.column_names(table_name)
		t = PrettyTable(column)
		for tuple in table_data:
			t.add_row(list(tuple))
		print(t)

	def column_names(self,table_name):
		cursor.execute(f"show columns from {table_name}")
		column = [column[0] for column in cursor.fetchall()]
		return column

	def show_table_by_invoice(self,table_choice, invoice):
		if table_choice == 1:
			cursor.execute(
				f"SELECT * FROM Vehicle where invoice = {invoice}"
			)
			table_data = cursor.fetchall()
		elif table_choice == 2:
			cursor.execute(
				f"SELECT body.id,body.type,body.doors,body.length,body.width,body.seats,body.ground_clearance,body.b_id "
				f"FROM body INNER JOIN Vehicle "
				f"ON body.b_id = vehicle.id "
				f"WHERE vehicle.invoice = {invoice}"
			)
			table_data = cursor.fetchall()
		elif table_choice == 3:
			cursor.execute(
				f"SELECT engine.id,engine.type,engine.fuel_type,engine.cylinders,engine.size,engine.horsepower_hp,engine.horsepower_rpm,engine.cam_typ,engine.transmission,engine.e_id "
				f"FROM engine INNER JOIN vehicle "
				f"ON engine.e_id = vehicle.id "
				f"WHERE vehicle.invoice = {invoice}"
			)
			table_data = cursor.fetchall()
		elif table_choice == 4:
			cursor.execute(
				f"SELECT mileage.id,mileage.fuel_tankk_capacity,mileage.range_city,mileage.range_highway,mileage.m_id "
				f"FROM mileage INNER JOIN vehicle "
				f"ON mileage.m_id = vehicle.id "
				f"WHERE vehicle.invoice = {invoice}"
			)
			table_data = cursor.fetchall()
		return table_data

	def update_table(self,table_name,update_field,update_value,id,cursor):
		cursor.execute(
			f"UPDATE {table_name} SET {update_field} = '{update_value}' where id = '{id}'"
		)
		connection.mydb1.commit()


if __name__ == "__main__":
	main = Main()
	database_value = main.get_api_data()

	main.write_data_file(database_value)

	cursor = main.connection_database()

	car_data = main.read_data_from_file()

	dbcalls = Database_calls()

	if dbcalls.check_table_if_exists(cursor) == True:
		print("Table already exists")
	else:
		dbcalls.create_table(cursor)
		dbcalls.insert_data(car_data,cursor)


	def menu():
		strs = ('1: Show Table data \n'
				'2: Show Table data by Ivoice\n'
				'3: Update\n'
				'4: Delete\n'
				'5: Exit')
		print(strs)
		choice = int(input("Select Your Choice: "))
		return int(choice)
	tables = ['vehicle','body','engine','mileage']
	while True:  # use while True
		choice = menu()
		if choice == 1:
			while True:
				strs = ('1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select Your Choice: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data = dbcalls.table_data(table_name,cursor)
				dbcalls.display_table(table_name,table_data, cursor)

		elif choice == 2:
			invoice = input("Enter Invoice Number: ")
			while True:
				strs = ('1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select Your Choice: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data = dbcalls.show_table_by_invoice(table_choice,invoice)
				dbcalls.display_table(table_name,table_data,cursor)
		elif choice == 3:
			while True:
				strs = ('1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select the Table you want to Update: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data= dbcalls.table_data(table_name,cursor)
				dbcalls.display_table(table_name, table_data, cursor)
				print(dbcalls.column_names(table_name))
				update_field = input("Enter the field you want to update: ")
				id = input("Enter the id you want to update: ")
				update_value = input(f"Enter the new value for {update_field}: ")
				dbcalls.update_table(table_name,update_field,update_value,id,cursor)
				table_data = dbcalls.table_data(table_name, cursor)
				dbcalls.display_table(table_name, table_data, cursor)

		elif choice == 4:
			break

