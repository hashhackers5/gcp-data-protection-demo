from google.cloud import bigquery

def create_and_insert_customers(dataset_id: str, table_id: str, customer_data: list):
    """
    Creates a BigQuery dataset and table for customer data if they don't exist,
    and then inserts the provided customer_data into the table.

    Args:
        dataset_id (str): The ID of the BigQuery dataset.
        table_id (str): The ID of the BigQuery table.
        customer_data (list): A list of tuples, where each tuple represents a row
                              of customer data in the order of the schema:
                              (customer_id, full_name, email, phone, credit_card, dob).
    """
    client = bigquery.Client()
    
    # Define the schema for the customers table
    schema = [
        bigquery.SchemaField("customer_id", "STRING"),
        bigquery.SchemaField("full_name", "STRING"),
        bigquery.SchemaField("email", "STRING"),
        bigquery.SchemaField("phone", "STRING"),
        bigquery.SchemaField("credit_card", "STRING"),
        bigquery.SchemaField("dob", "DATE")
    ]

    # Create the dataset if it doesn't exist
    client.create_dataset(dataset_id, exists_ok=True)
    print(f"Dataset '{dataset_id}' ensured to exist.")

    # Construct the table reference
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    # Create the table if it doesn't exist
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table, exists_ok=True)
    print(f"Table '{table_id}' ensured to exist in dataset '{dataset_id}'.")

    # Prepare rows for insertion in JSON format
    # This maps the schema field names to the corresponding values in each row tuple
    rows_to_insert = [dict(zip([f.name for f in schema], row)) for row in customer_data]

    # Insert rows into the table
    errors = client.insert_rows_json(table, rows_to_insert)

    if errors:
        print("Errors encountered while inserting rows:")
        for error in errors:
            print(error)
    else:
        print(f"{len(customer_data)} rows inserted successfully into '{table_id}'.")

# --- Example Usage ---
if __name__ == "__main__":
    # Your customer data
    df = pd.read_csv(file_path)
    create_and_insert_customers("demo_data", "customers", df)
