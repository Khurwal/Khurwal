import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import sha2, concat_ws


def main(input_file, output_file):
# Initialize SparkSession
spark = SparkSession.builder \
    .appName("AnonymizeData") \
    .getOrCreate()

# Load the CSV file into a DataFrame
df = spark.read.csv('input_file', header=True)

# Anonymize the required columns
anonymized_df = df.withColumn('first_name', sha2('first_name', 256)) \
                  .withColumn('last_name', sha2('last_name', 256)) \
                  .withColumn('address', sha2('address', 256))

# Save the anonymized DataFrame to a new CSV file
anonymized_df.write.csv(output_file, header=True)

# Stop the Spark session
spark.stop()

  if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: anonymized_data_spark.py <input_file> <Output_file>")
        sys.exit(-1)

    input_file = sys.argv[1] #
    output_file = sys.argv[2] #'anonymized_sample_spark.csv'

    main(input_file, output_file)