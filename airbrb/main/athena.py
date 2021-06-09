from decouple import config
import boto3
import pandas as pd


def pedirCosaGenerica(Query):
    athena = boto3.client('athena', region_name="us-east-1", aws_access_key_id=config('aws_access_key_id'),
        aws_secret_access_key=config('aws_secret_access_key'))
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

def cleanQueryResult(result) :
    return [[data.get('VarCharValue') for data in row['Data']]
            for row in result['ResultSet']['Rows']]

def pedirCosas(precio):
    athena = boto3.client('athena', region_name="us-east-1", aws_access_key_id=config('aws_access_key_id'), 
        aws_secret_access_key=config('aws_secret_access_key'))
    Query = """ SELECT procedence, Count(price)           FROM  amsterdam_unido_ WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  berlin_unido_    WHERE {0} GROUP BY procedence  
UNION ALL SELECT procedence, Count(price) FROM  edinburgh_unido_ WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  istambul_        WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  madrid_unido_    WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  melbourne_unido_ WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  paris_unido_     WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  rio_unido_       WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  sydney_unido_    WHERE {0} GROUP BY procedence 
UNION ALL SELECT procedence, Count(price) FROM  tokio_unido_     WHERE {0} GROUP BY procedence """.format(precio)
    print(Query)
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


def pedirCosas2():
    athena = boto3.client('athena', region_name="us-east-1", aws_access_key_id=config('aws_access_key_id'),
        aws_secret_access_key=config('aws_secret_access_key'))
    Query = """ select amsterdam_unido_.procedence, amsterdam_lista_reducida_.number_of_reviews, avg(amsterdam_unido_.price) from amsterdam_lista_reducida_ join amsterdam_unido_ on amsterdam_lista_reducida_.id = amsterdam_unido_.listing_id group by amsterdam_lista_reducida_.number_of_reviews, amsterdam_unido_.procedence
union all select berlin_unido_.procedence, berlin_lista_reducida_.number_of_reviews, avg(berlin_unido_.price) from berlin_lista_reducida_ join berlin_unido_ on berlin_lista_reducida_.id = berlin_unido_.listing_id group by berlin_lista_reducida_.number_of_reviews, berlin_unido_.procedence
union all select edinburgh_unido_.procedence, edinburgh_lista_reducida_.number_of_reviews, avg(edinburgh_unido_.price) from edinburgh_lista_reducida_ join edinburgh_unido_ on edinburgh_lista_reducida_.id = edinburgh_unido_.listing_id group by edinburgh_lista_reducida_.number_of_reviews, edinburgh_unido_.procedence
union all select  istambul_.procedence,  istambul_lista_reducida_.number_of_reviews, avg( istambul_.price) from  istambul_lista_reducida_ join  istambul_ on  istambul_lista_reducida_.id =  istambul_.listing_id group by  istambul_lista_reducida_.number_of_reviews,  istambul_.procedence
union all select madrid_unido_.procedence, madrid_lista_reducida_.number_of_reviews, avg(madrid_unido_.price) from madrid_lista_reducida_ join madrid_unido_ on madrid_lista_reducida_.id = madrid_unido_.listing_id group by madrid_lista_reducida_.number_of_reviews, madrid_unido_.procedence """
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