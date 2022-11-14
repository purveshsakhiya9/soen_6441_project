import json
import requests
from connection import connection
from tdg import TDG


class Main:
    @property
    def get_api_data(self):
        # car api
        url = "https://car-api2.p.rapidapi.com/api/trims"
        # url https://car-api2.p.rapidapi.com/api/trims followed by id no. will give the record of the table from api
        querystring = {"verbose": "yes", "sort": "id", "direction": "asc", "limit": "25", "year": 2020}
        #  taking 25 records from api with year set as 2020

        # host and api key
        headers = {
            "X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
            "X-RapidAPI-Host": "car-api2.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # fetching ids from api for each record
        information = response.json()["data"]

        db_value = []
        # fetching data from api using ids for all the required tables
        for i in range(0, 25):
            url = "https://car-api2.p.rapidapi.com/api/trims/" + str(information[i]['id'])
            response = requests.request("GET", url, headers=headers, params=querystring)
            database_value.append(response.json())

        db_value = json.dumps(database_value)
        return db_value

    @staticmethod
    def write_data_file(database_value):
        f = open("car.json", "w")
        f.write(database_value)
        f.close()

    @staticmethod
    def read_data_from_file():
        f = open("car.json", "r")
        data = json.loads(f.read())
        f.close()
        return data

    def connection_database(self):
        cursor = connection.connect(self)
        return cursor

    def menu(self):
        show_menu = ('\n1: Show Table data \n'
                     '2: Show Table data by Invoice\n'
                     '3: Update\n'
                     '4: Delete\n'
                     '5: Exit')
        print(show_menu)
        selected_option = int(input("Select Your Choice: "))
        return selected_option


if __name__ == "__main__":

    main = Main()
    tdg = TDG()

    if tdg.check_table_if_exists():
        print("Table already exists")
    else:
        database_value = main.get_api_data
        main.write_data_file(database_value)
        car_data = main.read_data_from_file()
        tdg.create_table()
        tdg.insert_vehicle(car_data)
        tdg.insert_body(car_data)
        tdg.insert_engine(car_data)
        tdg.insert_mileage(car_data)

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
