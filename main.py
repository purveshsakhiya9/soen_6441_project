import json
import requests
import connection
from tdg import TDG


class Main:
	def get_api_data(self):
		# car api
		url = "https://car-api2.p.rapidapi.com/api/trims"
		# url https://car-api2.p.rapidapi.com/api/trims followed by id number will give the record of the tabel from the api
		querystring = {"verbose": "yes", "sort": "id", "direction": "asc", "limit": "25", "year": 2020}
		#  taking 25 records from api with year set as 2020

		# host and api key
		headers = {
			"X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
			"X-RapidAPI-Host": "car-api2.p.rapidapi.com"
		}

		response = requests.request("GET", url, headers=headers, params=querystring)

		# fetcing ids from api for each record
		information = response.json()["data"]

		database_value = []
		# fetching data from api using ids for all the required tabels
		for i in range(0, 25):
			url = "https://car-api2.p.rapidapi.com/api/trims/" + str(information[i]['id'])
			response = requests.request("GET", url, headers=headers, params=querystring)
			database_value.append(response.json())

		database_value = json.dumps(database_value)
		return database_value

	def write_data_file(self, database_value):
		f = open("car.json", "w")
		f.write(database_value)
		f.close()

	def read_data_from_file(self):
		f = open("car.json", "r")
		car_data = json.loads(f.read())
		return car_data

	# def connection_database(self):
	# 	cursor = connection.mydb1.cursor()
	# 	return cursor

	def menu(self):
		strs = ('\n1: Show Table data \n'
				'2: Show Table data by Ivoice\n'
				'3: Update\n'
				'4: Delete\n'
				'5: Exit')
		print(strs)
		choice = int(input("Select Your Choice: "))
		return int(choice)

if __name__ == "__main__":

	main = Main()
	tdg = TDG()

	if tdg.check_table_if_exists():
		print("Table already exists")
	else:
		database_value = main.get_api_data()
		main.write_data_file(database_value)
		car_data = main.read_data_from_file()
		tdg.create_table()
		tdg.insert_data(car_data)

	tables = ['vehicle', 'body', 'engine', 'mileage']
	while True:  # use while True
		choice = main.menu()
		if choice == 1:
			while True:
				strs = ('\n1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select Your Choice: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data = tdg.table_data(table_name)
				tdg.display_table(table_name, table_data)

		elif choice == 2:
			invoice = input("\nEnter Invoice Number: ")
			while True:
				strs = ('\nTables:- \n'
						'1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select Your Choice: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data = tdg.show_table_by_invoice(table_choice, invoice)
				tdg.display_table(table_name, table_data)

		elif choice == 3:
			while True:
				strs = ('\nTables:- \n'
						'1: Vehicle \n'
						'2: Body\n'
						'3: Engine\n'
						'4: Mileage\n'
						'5: Go Back')
				print(strs)
				table_choice = int(input("Select the Table you want to Update: "))
				if table_choice == 5:
					break
				table_name = tables[table_choice - 1]
				table_data = tdg.table_data(table_name)
				tdg.display_table(table_name, table_data)
				print("Column Fields: ", str(tdg.column_names(table_name))[1:-1])
				update_field = input("Enter the field you want to update: ")
				id = input("Enter the id you want to update: ")
				update_value = input(f"Enter the new value for {update_field}: ")
				tdg.update_table(table_name, update_field, update_value, id)
				table_data = tdg.table_data(table_name)
				tdg.display_table(table_name, table_data)

		elif choice == 4:
			while True:
				table_data = tdg.table_data("vehicle")
				tdg.display_table("vehicle", table_data)
				id = input("\nEnter the id you want to delete: ")
				if id == "exit":
					break
				tdg.delete_record(id)
				table_data = tdg.table_data("vehicle")
				tdg.display_table("vehicle", table_data)

		elif choice == 5:
			break
