from data import dependant_variables, independent_variables, insert_data, variables, filters, update_data, conditions
from pyspark.sql import SparkSession
from utils import create_storage_table_query, create_training_table_query, \
                 create_insert_query, create_retrieve_query, create_update_query, \
                 create_delete_query

spark = SparkSession \
    .builder \
    .appName("Citric Sheep Tech Test") \
    .enableHiveSupport() \
    .getOrCreate()

# Creating the database
spark.sql("""
          CREATE DATABASE IF NOT EXISTS elevator_data_storage_db
          COMMENT 'Database for floor prediction.';
         """)
# Creating training table
training_table_query = create_training_table_query("training_data", dependant_variables, independent_variables)
spark.sql(training_table_query)
# Creating data storage table
storage_table_query = create_storage_table_query("data_storing", independent_variables)
spark.sql(storage_table_query)
# Insert data [C]
insert_query = create_insert_query("data_storing", dependant_variables=None, independent_variables=independent_variables, data=insert_data)
spark.sql(insert_data)
# Retrieve data [R] [Data suitable for prediction]          
retrieve_query = create_retrieve_query("data_storing", variables, filters, orders=None)
data_as_list = spark.sql(retrieve_query).collect()
# Update data [U] [Business flair]
update_query = create_update_query("data_storing", update_data, conditions)
spark.sql(update_query)
# Delete data [D] [Business flair]
delete_query = create_delete_query("training_data", conditions)
#delete_query_2 = 
spark.sql(delete_query)
