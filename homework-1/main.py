"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
import psycopg2

current_directory = os.getcwd()
file_path_employees = os.path.join(current_directory, 'north_data', 'employees_data.csv')
file_path_customers = os.path.join(current_directory, 'north_data', 'customers_data.csv')
file_path_orders = os.path.join(current_directory, 'north_data', 'orders_data.csv')


class DataLoader:
    """Класс для загрузки данных из CSV-файла в базу данных."""
    def __init__(self, csv_file, table_name):
        self.csv_file = csv_file
        self.table_name = table_name

    def connect_to_database(self):
        """Устанавливает соединение с базой данных."""
        conn = psycopg2.connect(
            host="localhost",
            database="north",
            user="postgres",
            password="4242")
        return conn

    def insert_data(self):
        """Загружает данные из файла CSV в указанную таблицу."""
        conn = self.connect_to_database()
        cursor = conn.cursor()
        try:
            with open(self.csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Пропуск заголовка
                for row in reader:
                    placeholders = ', '.join(['%s'] * len(row))
                    query = f"INSERT INTO {self.table_name} VALUES ({placeholders})"
                    cursor.execute(query, row)
                conn.commit()
            print(f"Данные из файла успешно загружены в таблицу")
        except (psycopg2.Error, csv.Error) as e:
            print(f"Произошла ошибка при загрузке данных: {str(e)}")
        finally:
            cursor.close()
            conn.close()

data_loader = DataLoader(file_path_employees, 'employees')
data_loader.insert_data()

data_loader_2 = DataLoader(file_path_customers, 'customers')
data_loader_2.insert_data()

data_loader_3 = DataLoader(file_path_orders, 'orders')
data_loader_3.insert_data()

