# 🌤️ Weather Data ETL Pipeline using Airflow, AWS EC2, and S3 ☁️ 

[![Airflow](https://img.shields.io/badge/Airflow-2.3.4-blue)](https://airflow.apache.org/) [![AWS EC2](https://img.shields.io/badge/AWS-EC2-orange)](https://aws.amazon.com/ec2/) [![S3](https://img.shields.io/badge/S3-Storage-green)](https://aws.amazon.com/s3/) [![Python](https://img.shields.io/badge/Python-3.9.5-yellow)](https://www.python.org/)

### Project Overview 🚀

This project demonstrates a fully automated **ETL pipeline** that extracts weather data from the **OpenWeatherMap API**, processes it using **Python**, and stores the transformed data as **CSV** files in **Amazon S3**. The entire orchestration is managed using **Apache Airflow**, deployed on an **AWS EC2** instance, and the pipeline is scheduled to run daily.

This project is particularly useful for learning about:
- **ETL (Extract, Transform, Load)** pipelines.
- Cloud deployment using **AWS EC2** and storage in **Amazon S3**.
- Automating workflows using **Apache Airflow**.

---

### What Has Been Done?

1. **Data Extraction**:
   - The weather data for **Boston** is fetched from the **OpenWeatherMap API** in JSON format using Airflow's `SimpleHttpOperator`.
   - The pipeline checks the availability of the API before proceeding with the extraction using the `HttpSensor` task.

2. **Data Transformation**:
   - The raw JSON data is transformed by:
     - **Converting temperatures** from Kelvin to Fahrenheit for easier comprehension.
     - **Formatting timestamps** from Unix to human-readable format.
   - The transformed data includes details like:
     - City Name 🌆
     - Temperature 🌡️
     - Feels-like Temperature 🔥
     - Humidity 💧
     - Wind Speed 🌬️
     - Time of the weather recording ⏰.

3. **Data Loading**:
   - The transformed data is written into a **CSV file** using the `pandas` library.
   - The CSV file is stored in an **Amazon S3 bucket**, ensuring secure, durable, and scalable storage.

4. **Automation & Orchestration**:
   - **Apache Airflow** is used to manage and automate the entire workflow. The pipeline is scheduled to run daily, meaning the weather data is updated every day.
   - Features of Airflow include task scheduling, retries on failures, and email notifications for errors or retries.

---

### Architecture 📋

![image](https://github.com/user-attachments/assets/9c47cf1f-6ded-467d-a059-2738c87fbd27)


---

### Key Features 🔥

1. **Automated Weather Data Extraction** ⛅:
   - The pipeline fetches real-time weather data from the OpenWeatherMap API for a specific location (Boston in this case).
   - **HttpSensor** ensures that the API is available before starting the ETL process, providing reliability.

2. **Data Transformation** 🌡️:
   - Data transformations, such as converting temperature from **Kelvin to Fahrenheit** and formatting timestamps, are handled by Python’s data manipulation libraries, particularly **pandas**.

3. **Cloud-Based Data Storage** 🗄️:
   - After transformation, the data is saved in **Amazon S3** as a **CSV file**, making it easily accessible for further analysis or integration with other systems.

4. **Apache Airflow Orchestration** 📋:
   - **Airflow DAG** (Directed Acyclic Graph) manages the order of tasks, ensuring the process is completed in the correct sequence:
     1. **Check API availability**.
     2. **Extract raw weather data**.
     3. **Transform the data**.
     4. **Save the data in an S3 bucket**.
   - Airflow also allows the pipeline to be scheduled, with automatic retries on failures and notifications for issues.

5. **Scalable Infrastructure** 🖥️:
   - The project is deployed on **AWS EC2**, allowing for scalability in terms of computational power, as the ETL pipeline grows in complexity or handles more data.

---

### Sample Output 💾

The transformed data is saved as a CSV in the S3 bucket. Below is a sample of how the output file might look:

| 🌆 **City** | 🌡️ **Temp (F)** | 🔥 **Feels Like (F)** | 💧 **Humidity** | 🌬️ **Wind Speed** | ⏰ **Time** |
|-------------|-----------------|----------------------|-----------------|-------------------|------------|
| **Boston**  | 75.2            | 74.3                 | 65%             | 5.4 mph           | 15:30      |

---

### Setup Instructions ⚙️

#### Prerequisites:
1. **AWS EC2**: You need an EC2 instance with the appropriate permissions to handle the ETL pipeline.
2. **Amazon S3**: A pre-configured S3 bucket where the processed data will be stored.
3. **Apache Airflow**: Installed and configured on your EC2 instance for managing the DAG.
4. **Python**: Installed along with necessary libraries like `pandas`, `s3fs`, and `apache-airflow`.

#### Step-by-Step Guide:

1. **Set Up AWS IAM Roles**:
   - Create a user group with **AmazonEC2FullAccess** and **AmazonS3FullAccess** policies.
   - Attach this role to the EC2 instance to allow it to access both EC2 and S3 services securely.

2. **EC2 Instance Setup**:
   - Connect to your EC2 instance and install the required software:
     ```bash
     sudo apt update
     sudo apt install python3-pip
     python3 -m venv airflow_venv
     source airflow_venv/bin/activate
     pip install pandas s3fs apache-airflow
     ```
   - Start Airflow:
     ```bash
     airflow standalone
     ```

3. **Configure Airflow DAG**:
   - Upload the `weather_dag.py` to the Airflow DAGs folder:
     ```bash
     cp scripts/weather_dag.py ~/airflow/dags/
     ```
   - Add your **OpenWeatherMap API key** to the `weather_dag.py` file before running the pipeline.

4. **Running the Pipeline**:
   - The DAG can be triggered manually or set to run on a schedule (daily). The extracted and transformed data will be saved automatically to the specified S3 bucket.

---
### Technologies Used 🛠️

- **Airflow**: Orchestrates the ETL tasks 📋.
- **AWS EC2**: The compute instance running the ETL code 🖥️.
- **S3**: AWS storage for saving the output data 💾.
- **Python**: The programming language that handles the data transformation 🐍.
- **OpenWeatherMap API**: The data source for the weather information 🌍.

---

### Project License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

