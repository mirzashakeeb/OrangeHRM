import csv
import os

def read_csv(file_name, required_headers):
    """
    Reads a CSV file and returns data as a list of tuples.
    Raises error if required headers are missing.
    """
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_data", file_name))
    data = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if not set(required_headers).issubset(reader.fieldnames):
                raise KeyError(f"CSV must have headers: {required_headers}")

            for row in reader:
                record = tuple(row[h] for h in required_headers)
                data.append(record)

    except FileNotFoundError:
        print(f"❌ CSV file not found: {file_path}")

    except KeyError as e:
        print(f"❌ CSV header mismatch: {e}")

    return data


def get_login_data():
    return read_csv("login_data.csv", ["username", "password", "expected"])
