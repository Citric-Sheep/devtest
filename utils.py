def format_dict(dict: dict):
    """Format dict with variable name and data type for sql query"""
    query = ", ".join(f"{key} {value}\n" for key, value in dict.items())
    
    return query

def create_training_table_query(table_name:str, dependant_variables: dict, independent_variables: dict):
    """Creates query for training table"""
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    if dependant_variables:
        query += format_dict(dependant_variables)
        query += ", "

    query += format_dict(independent_variables)

    query += ");"


    return query

def create_storage_table_query(table_name:str, independent_variables: dict):
    """Creates query for training table"""
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    query += format_dict(independent_variables)

    query += ");"

    return query

def create_insert_query(table_name: str, dependant_variables: dict, independent_variables: dict, data: dict):
    """Creates insert into query"""
    query = f"INSERT INTO {table_name} (" 
    if dependant_variables:
        query += ", ".join(list(dependant_variables.keys()))
    query += f"{', '.join(list(independent_variables.keys()))}) VALUES ({', '.join([str(data[key]) for key in data.keys()])});"

    return query

def create_retrieve_query(table_name: str, retrieve_variables: list, filters: dict, orders: dict):
    """Creates retrieve query"""
    query = f"""SELECT {', '.join(retrieve_variables)} FROM {table_name} 
                WHERE {'AND '.join([f'{key} {value[1]} {value[0]} ' for key, value in filters.items()])}
                {'ORDER BY ' if orders else ''} {', '.join([f'{key} {value}' for key, value in orders.items()]) if orders else ''};
                """
            
    return query

def create_update_query(table_name: str, update_values: dict, conditions: dict):
    """Creates update query"""
    query = f"""UPDATE {table_name} SET {'AND '.join([f'{key}={value} ' for key, value in update_values.items()])}
                WHERE {'AND '.join([f'{key} {value[1]} {value[0]} ' for key, value in conditions.items()])};
             """

    return query

def create_delete_query(table_name: str, conditions: dict):
    """Creates delete query"""
    query = f"DELETE FROM {table_name} WHERE {'AND '.join([f'{key} {value[1]} {value[0]} ' for key, value in conditions.items()])};"
    
    return query