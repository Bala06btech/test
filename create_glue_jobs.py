import csv
import boto3
import json

def read_job_data_from_csv(csv_file_path):
    job_data = []
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                job_name = row['job_name']
                script_location = row['script_location']
                job_data.append({'job_name': job_name, 'script_location': script_location})
    except Exception as e:
        print("Error reading CSV:", str(e))
    return job_data

def create_glue_jobs(job_data):
    try:
        client = boto3.client('glue', region_name='your-region')
        for job_info in job_data:
            job_name = job_info['job_name']
            script_location = job_info['script_location']

            # Define Glue job parameters
            role_name = 'your-glue-role-name'

            job = {
                    'Name': job_name_b,
                    'Role': role_name_b,
                    'Command': {
                        'Name': 'glueetl',
                        'ScriptLocation': script_location_b
                    },
                    'DefaultArguments': {
                        '--job-language': 'python'
                    },
                    'ExecutionProperty': {
                        'MaxConcurrentRuns': 1
                    },
                    'MaxRetries': 0,
                    'AllocatedCapacity': 10,
                    'Timeout': 60,
                    'MaxCapacity': 10.0,
                    'GlueVersion': '2.0',
                    'MaxDPUs': 10,
                    'SecurityConfiguration': 'your-security-configuration-b',  # Optional
                    'WorkerType': 'G.1X',  # Optional
                    'NumberOfWorkers': 2,  # Optional
                    'Connections': ['your-connection-b'],  # Optional
                    'MaxWorkerCount': 10  # Optional
                }

            response = client.create_job(**job)

            print(f"Glue job '{job_name}' created successfully:")
            print(json.dumps(response, indent=2))
    
    except Exception as e:
        print("Error creating Glue jobs:", str(e))

def main():
    # Specify the path to your CSV file
    csv_file_path = 'your-csv-file.csv'

    # Read job data from the CSV
    job_data = read_job_data_from_csv(csv_file_path)

    # Create Glue jobs based on the data
    create_glue_jobs(job_data)

if __name__ == '__main__':
    main()
