from airflow import DAG 
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd




default_args = {
    'owner': 'airflow',                       # The owner of the DAG tasks
    'depends_on_past': False,                 # Tasks do not depend on previous runs
    'start_date': datetime(2024, 9, 12),      # The start date of the DAG
    'email': ['abcs@gmail.com'],              # Email notifications recipients
    'email_on_failure': True,                 # Disable email notifications on failure
    'email_on_retry': True,                   # Disable email notifications on retry
    'retries': 2,                             # Number of retry attempts after a failure
    'retry_delay': timedelta(minutes=2)       # Delay between retry attempts
}







def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit= kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    # Creating a dictionary with transformed data
    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature (C)": temp_farenheit,           # Updated to Celsius
        "Feels Like (C)": feels_like_farenheit,      # Updated to Celsius
        "Minimum Temp (C)": min_temp_farenheit,      # Updated to Celsius
        "Maximum Temp (C)": max_temp_farenheit,      # Updated to Celsius
        "Pressure": pressure,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "Time of Record": time_of_record,
        "Sunrise (Local Time)": sunrise_time,
        "Sunset (Local Time)": sunset_time                        
    }
    

    




    # Define AWS credentials before usage
    aws_credentials = {
        "key": "<Paste your own>",
        "secret": "<Paste your own>",
        "token": "<Paste your own>"
    }

    # Assuming transformed_data_list is already defined
    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    # Get current timestamp and format it for the file name
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    file_name = f"current_weather_data_boston_{dt_string}.csv"

    # Save DataFrame to S3 using provided AWS credentials
    df_data.to_csv(
        f"s3://weatherapis3bucket-yml/{file_name}",
        index=False,
        storage_options={
            "key": aws_credentials["key"],
            "secret": aws_credentials["secret"],
            "token": aws_credentials["token"]
        }
    )

with DAG('weather_dag',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:


        is_weather_api_ready = HttpSensor(
        task_id ='is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=boston&appid=893b8466cc9b47e39ef058c866e234a6'
        )
        
        extract_weather_data = SimpleHttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint='/data/2.5/weather?q=boston&appid=893b8466cc9b47e39ef058c866e234a6',
        method = 'GET',
        response_filter= lambda r: json.loads(r.text),
        log_response=True
        )
        
        transform_load_weather_data = PythonOperator(
        task_id= 'transform_load_weather_data',
        python_callable = transform_load_data
        )           
        
        
        
        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data