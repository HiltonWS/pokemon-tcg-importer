def read_file(file_path):
    with open(file_path, 'r') as sql_file:
        return sql_file.read()