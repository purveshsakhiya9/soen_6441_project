from prettytable import PrettyTable
import uuid
from connection import connection


class TDG:
    def __init__(self):
        c = connection.connect(self)
        self.cursor = c.cursor()

    def check_table_if_exists(self):
        self.cursor.execute("Show tables like 'vehicle'")
        check_tables = self.cursor.fetchone()
        if check_tables:
            return True
        else:
            return False

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE vehicle("
            "id varchar(255) NOT NULL,"
            "year int(10),"
            "name varchar(255),"
            "description varchar(255),"
            "msrp varchar(255),"
            "invoice varchar(255),"
            "PRIMARY KEY(id))"
        )
        self.cursor.execute(
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
        self.cursor.execute(
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
        self.cursor.execute(
            "CREATE TABLE mileage("
            "id varchar(255),"
            "fuel_tank_capacity varchar(255),"
            "range_city varchar(255),"
            "range_highway varchar(255),"
            "m_id varchar(255),"
            "primary key(id),"
            "foreign key (m_id) references vehicle (id))"
        )
        return True

    def insert_body(self, car_data):
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
            self.cursor.execute(
                f"INSERT INTO body (id,type,doors,length,width,seats,ground_clearance,b_id) "
                f"values (%s,%s,%s,%s,%s,%s,%s,%s)",
                (body_id, body_type, doors, length, width, seats, ground_clearance, b_id)
            )
            connection.mydb.commit()

    def insert_engine(self, car_data):
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
            self.cursor.execute(
                "INSERT INTO engine"
                "(id,type,fuel_type,cylinders,size,horsepower_hp,horsepower_rpm,cam_typ,transmission,e_id) "
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (engine_id, engine_type, fuel_type, cylinders, size, horsepower_hp, horsepower_rpm, cam_typ,
                 transmission,
                 e_id)
            )
            connection.mydb.commit()

    def insert_mileage(self, car_data):
        # mileage table
        for item in car_data:
            m_id = item['id']
            mileage_id = str(uuid.uuid4())
            fuel_tank_capacity = item['make_model_trim_mileage']['fuel_tank_capacity']
            range_city = item['make_model_trim_mileage']['range_city']
            range_highway = item['make_model_trim_mileage']['range_highway']
            self.cursor.execute(
                "INSERT INTO mileage(id,fuel_tank_capacity,range_city,range_highway,m_id) values (%s,%s,%s,%s,%s)",
                (mileage_id, fuel_tank_capacity, range_city, range_highway, m_id)
            )
            connection.mydb.commit()

    def insert_vehicle(self, car_data):
        # vehicle table
        for item in car_data:
            id = item['id']
            year = item['year']
            name = item['name']
            description = item['description']
            msrp = item['msrp']
            invoice = item['invoice']
            self.cursor.execute(
                "INSERT INTO vehicle (id, year, name, description, msrp, invoice) values (%s,%s,%s,%s,%s,%s)",
                (id, year, name, description, msrp, invoice)
            )
            connection.mydb.commit()

    def table_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        return data

    def display_table(self, table_name, data):
        column = TDG.column_names(self, table_name)
        t = PrettyTable(column)
        for tuples in data:
            t.add_row(list(tuples))
        print("\n", t)

    def column_names(self, table_name):
        self.cursor.execute(f"show columns from {table_name}")
        column = [column[0] for column in self.cursor.fetchall()]
        return column

    def show_table_by_invoice(self, table_choice, invoice):
        table_data = []
        if table_choice == 1:
            self.cursor.execute(
                f"SELECT * FROM Vehicle where invoice = {invoice}"
            )
            table_data = self.cursor.fetchall()
            print(table_data)
        elif table_choice == 2:
            self.cursor.execute(
                f"SELECT body.* "
                f"FROM body INNER JOIN Vehicle "
                f"ON body.b_id = vehicle.id "
                f"WHERE vehicle.invoice = {invoice}"
            )
            table_data = self.cursor.fetchall()
        elif table_choice == 3:
            self.cursor.execute(
                f"SELECT engine.* "
                f"FROM engine INNER JOIN vehicle "
                f"ON engine.e_id = vehicle.id "
                f"WHERE vehicle.invoice = {invoice}"
            )
            table_data = self.cursor.fetchall()
        elif table_choice == 4:
            self.cursor.execute(
                f"SELECT mileage.* "
                f"FROM mileage INNER JOIN vehicle "
                f"ON mileage.m_id = vehicle.id "
                f"WHERE vehicle.invoice = {invoice}"
            )
            table_data = self.cursor.fetchall()
        return table_data

    def update_table(self, table_name, update_field, update_value, id):
        self.cursor.execute(
            f"UPDATE {table_name} SET {update_field} = '{update_value}' where id = '{id}'"
        )
        connection.mydb.commit()

    def delete_record(self, id):
        self.cursor.execute(
            f"DELETE mileage from vehicle inner join mileage on vehicle.id = mileage.m_id where vehicle.id = '{id}' ")
        self.cursor.execute(
            f"DELETE engine from vehicle inner join engine on vehicle.id = engine.e_id where vehicle.id = '{id}' ")
        self.cursor.execute(
            f"DELETE body from vehicle inner join body on vehicle.id = body.b_id where vehicle.id = '{id}'"
        )
        self.cursor.execute(f"delete from vehicle where id = '{id}'")
        connection.mydb.commit()
        print("Record Deleted Successfully!.")
