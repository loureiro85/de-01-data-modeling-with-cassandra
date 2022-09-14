import csv
import glob
import os
from typing import Callable, List, Tuple

from cassandra.cluster import Session


def get_file_path_list():
    """Get list of file paths."""

    # checking your current working directory
    print(os.getcwd())

    # Get your current folder and subfolder event data
    filepath = os.getcwd() + '/event_data'

    # Create a for loop to create a list of files and collect each filepath
    for root, dirs, files in os.walk(filepath):

        # join the file path and roots with the subdirectories using glob
        file_path_list = glob.glob(os.path.join(root, '*'))
        # print(file_path_list)

    print(f"Number of file paths: {len(file_path_list)}")

    return file_path_list


def generate_base_csv(file_path_list: List[str], output_file: str):
    """Generate base csv."""

    # initiating an empty list of rows that will be generated from each file
    full_data_rows_list = []

    # for every filepath in the file path list
    for f in file_path_list:

        # reading csv file
        with open(f, 'r', encoding='utf8', newline='') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            next(csvreader)

    # extracting each data row one by one and append it
            for line in csvreader:
                # print(line)
                full_data_rows_list.append(line)

    # uncomment the code below if you would like to get total number of rows
    print('len(full_data_rows_list):', len(full_data_rows_list))
    # uncomment the code below if you would like to check to see what the list of event data rows
    # will look like
    print('\nfull_data_rows_list[0]:', full_data_rows_list[0])

    # creating a smaller event data csv file called event_datafile_full csv that will be used to
    # insert data into the Apache Cassandra tables
    csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    with open(output_file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='myDialect')
        writer.writerow(['artist', 'first_name', 'gender', 'item_in_session', 'last_name', 'length',
                         'level', 'location', 'session_id', 'song', 'user_id'])
        for row in full_data_rows_list:
            if (row[0] == ''):
                continue
            writer.writerow((
                row[0],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[12],
                row[13],
                row[16]
            ))


def get_values_1(line: Tuple) -> Tuple:
    """Get values for insert 1, from line."""

    values = (
        line[0],
        line[9],
        float(line[5]),
        int(line[8]),
        int(line[3])
    )
    return values


def get_values_2(line: Tuple) -> Tuple:
    """Get values for insert 2, from line."""

    values = (
        line[0],
        line[9],
        line[1],
        line[4],
        int(line[10]),
        int(line[8]),
        int(line[3]),
    )
    return values


def get_values_3(line: Tuple) -> Tuple:
    """Get values for insert 3, from line."""

    values = (
        line[1],
        line[4],
        line[9],
    )
    return values


def read_csv_and_insert_in_table(file: str, session: Session, insert: str, values_fn: Callable):
    """Read data from csv file and insert into table."""

    with open(file, encoding='utf8') as f:
        csvreader = csv.reader(f)
        next(csvreader)  # skip header
        for line in csvreader:
            values_1 = values_fn(line)
            session.execute(insert, values_1)
