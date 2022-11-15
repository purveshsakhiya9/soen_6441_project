from tdg import TDG
import unittest
import requests
from connection import connection
from main import Main

class MyTestCase(unittest.TestCase):
    def test_api(self):
        url = "https://car-api2.p.rapidapi.com/api/trims/6276"
        headers = {
            "X-RapidAPI-Key": "e9983c2065mshaf33398be4b091dp132915jsnb3a831923739",
            "X-RapidAPI-Host": "car-api2.p.rapidapi.com"
        }
        result = requests.request("GET", url, headers=headers)
        self.assertEqual(result.status_code, 200)  # add assertion here
    def test_check_table_if_exist(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        value = TDG.check_table_if_exists(self)
        if value == True:
            self.assertTrue(TDG.check_table_if_exists(self))
        else:
            self.assertFalse(TDG.check_table_if_exists(self))
    def test_create_tables(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        value = TDG.check_table_if_exists(self)
        if value == True:
            self.cursor.execute(f"DROP TABLE car.vehicle,car.engine,car.body,car.mileage")
            self.assertEqual(True,TDG.create_table(self))
        else:
            self.assertEqual(True,TDG.create_table(self))
    def test_db(self):
        self.assertEqual(connection.connect(self),Main.connection_database(self))
    def test_insert_vehicle(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"SELECT count(*) from vehicle")
        length = self.cursor.fetchall()[0][0]
        car_data = Main.read_data_from_file()
        TDG.insert_vehicle(self,car_data)
        self.cursor.execute(f"SELECT count(*) from vehicle")
        length_after_insert = self.cursor.fetchall()[0][0]
        self.assertEqual(length,length_after_insert-25)
    def test_insert_body(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"SELECT count(*) from body")
        length = self.cursor.fetchall()[0][0]
        car_data = Main.read_data_from_file()
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0")
        TDG.insert_body(self,car_data)
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 1")
        self.cursor.execute(f"SELECT count(*) from body")
        length_after_insert = self.cursor.fetchall()[0][0]
        self.assertEqual(length,length_after_insert-25)
    def test_insert_engine(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"SELECT count(*) from engine")
        length = self.cursor.fetchall()[0][0]
        # print(length)
        car_data = Main.read_data_from_file()
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0")
        TDG.insert_engine(self,car_data)
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 1")
        self.cursor.execute(f"SELECT count(*) from engine")
        length_after_insert = self.cursor.fetchall()[0][0]
        self.assertEqual(length,length_after_insert-25)
    def test_insert_mileage(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"SELECT count(*) from mileage")
        length = self.cursor.fetchall()[0][0]
        car_data = Main.read_data_from_file()
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0")
        TDG.insert_mileage(self,car_data)
        self.cursor.execute(f"SET FOREIGN_KEY_CHECKS = 1")
        self.cursor.execute(f"SELECT count(*) from mileage")
        length_after_insert = self.cursor.fetchall()[0][0]
        self.assertEqual(length,length_after_insert-25)
    def test_column(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"show columns from vehicle")
        column = [column[0] for column in self.cursor.fetchall()]
        self.assertEqual(column,TDG.column_names(self,"vehicle"))
    def test_table_data(self):
        c = connection.connect(self)
        self.cursor = c.cursor()
        self.cursor.execute(f"SELECT * FROM vehicle")
        table_data = self.cursor.fetchall()
        self.assertEqual(table_data,TDG.table_data(self,"vehicle"))


if __name__ == '__main__':
    unittest.main()
