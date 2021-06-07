import boto3
import pandas as pd

"""# Credenciales"""
aws_access_key_id = 'AKIA4UBERADCSNV2X5WC'
aws_secret_access_key = '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'


def cleanQueryResult(result) :
    return [[data.get('VarCharValue') for data in row['Data']]
            for row in result['ResultSet']['Rows']]

def pedirCosas():
    athena = boto3.client('athena', region_name="us-east-1", aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    Query = 'SELECT * FROM rio_unido_ WHERE 20000<listing_id AND listing_id<40000 LIMIT 10'
    athena_job_query = athena.start_query_execution(
        QueryString=Query,
        QueryExecutionContext={
            'Database': 'grupo4_db'
        },
        ResultConfiguration={
            'OutputLocation': 's3://aypmd-grupo4/Queries/'
        }
    )
    query_execution_id = athena_job_query['QueryExecutionId']

    #  Aqui vemos el status de la solicitud
    athena_job_status_query = athena.get_query_execution(QueryExecutionId=query_execution_id)
    while (athena_job_status_query['QueryExecution']['Status']['State'] == 'QUEUED' or
        athena_job_status_query['QueryExecution']['Status']['State'] == 'RUNNING'):
        athena_job_status_query = athena.get_query_execution(QueryExecutionId=query_execution_id)
        #print(f"\r{athena_job_status_query['QueryExecution']['Status']['State']}")

    args = {
        'QueryExecutionId': query_execution_id,
        'MaxResults': 1000
    }
    response = athena.get_query_results(**args)

    table = cleanQueryResult(response)
    return table
    df = pd.DataFrame(table)
    df_names = df.query('index == 0')
    df = df.drop([0])
    """
    0 = listing_id
    1 = price
    2 = procedence
    3 = count
    """
    print(df)
    print(df_names)
    return df