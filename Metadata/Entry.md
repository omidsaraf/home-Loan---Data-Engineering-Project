
### **1. ADF\_Metadata Table (For Batch Processing)**

Here we log metadata for **ADF pipeline executions** related to batch processing. These will capture pipeline status, parameters, and run timestamps.

#### Sample Entries:

| **pipeline\_id** | **pipeline\_name**     | **source\_system** | **frequency** | **start\_time**     | **end\_time**       | **status** | **last\_run\_status** | **parameters**                                           | **created\_at**     | **updated\_at**     |
| ---------------- | ---------------------- | ------------------ | ------------- | ------------------- | ------------------- | ---------- | --------------------- | -------------------------------------------------------- | ------------------- | ------------------- |
| 1                | Loan\_Application\_ETL | CRM                | Daily         | 2023-08-01 00:00:00 | 2023-08-01 00:30:00 | Completed  | Success               | {"start\_date": "2023-08-01", "end\_date": "2023-08-01"} | 2023-08-01 00:00:00 | 2023-08-01 00:30:00 |
| 2                | Loan\_Approval\_Batch  | Core Banking       | Weekly        | 2023-08-01 01:00:00 | 2023-08-01 01:45:00 | Completed  | Success               | {"batch\_size": "500", "process\_type": "Incremental"}   | 2023-08-01 01:00:00 | 2023-08-01 01:45:00 |


| **job\_id** | **job\_name**                  | **job\_type** | **status** | **start\_time**     | **end\_time**       | **duration** | **error\_message** | **streaming\_source** | **micro\_batch\_id** |
| ----------- | ------------------------------ | ------------- | ---------- | ------------------- | ------------------- | ------------ | ------------------ | --------------------- | -------------------- |
| 1           | Loan\_Application\_Stream\_Job | Streaming     | Completed  | 2023-08-01 00:00:00 | 2023-08-01 01:00:00 | 1 hour       | NULL               | Kafka                 | batch\_12345         |
| 2           | Loan\_Approval\_Batch\_Job     | Batch         | Completed  | 2023-08-01 00:00:00 | 2023-08-01 00:45:00 | 45 minutes   | NULL               | NULL                  | NULL                 |

---

### **2. Airflow\_Metadata Table (For Batch Processing)**

Airflow metadata will capture DAG execution details for batch jobs, including the status of tasks in the DAG.

#### Sample Entries:

| **dag\_id** | **dag\_name**         | **task\_name**      | **status** | **start\_time**     | **end\_time**       | **execution\_time** | **parameters**                                   | **job\_id** | **created\_at**     | **updated\_at**     |
| ----------- | --------------------- | ------------------- | ---------- | ------------------- | ------------------- | ------------------- | ------------------------------------------------ | ----------- | ------------------- | ------------------- |
| 1           | loan\_processing\_dag | extract\_loan\_data | Success    | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 | 10 minutes          | {"source": "CRM", "date\_range": "2023-08-01"}   | 1           | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 |
| 2           | loan\_processing\_dag | approve\_loan\_task | Success    | 2023-08-01 00:15:00 | 2023-08-01 00:30:00 | 15 minutes          | {"approval\_threshold": "50000", "region": "NY"} | 1           | 2023-08-01 00:15:00 | 2023-08-01 00:30:00 |
| 3           | loan\_processing\_dag | disburse\_funds     | Failed     | 2023-08-01 00:30:00 | 2023-08-01 00:40:00 | 10 minutes          | {"loan\_type": "Home", "amount": "100000"}       | 2           | 2023-08-01 00:30:00 | 2023-08-01 00:40:00 |

---

### **3. Batch\_Metadata Table (For Batch Processing)**

Batch jobs like loan disbursement and risk model calculations are logged here.

#### Sample Entries:

| **batch\_id** | **job\_name**               | **status** | **start\_time**     | **end\_time**       | **execution\_time** | **parameters**                                           | **created\_at**     | **updated\_at**     |
| ------------- | --------------------------- | ---------- | ------------------- | ------------------- | ------------------- | -------------------------------------------------------- | ------------------- | ------------------- |
| 1             | Loan\_Disbursement\_Batch   | Completed  | 2023-08-01 00:00:00 | 2023-08-01 01:00:00 | 1 hour              | {"batch\_size": "100", "region": "NY"}                   | 2023-08-01 00:00:00 | 2023-08-01 01:00:00 |
| 2             | Default\_Risk\_Model\_Batch | Failed     | 2023-08-01 01:30:00 | 2023-08-01 02:15:00 | 45 minutes          | {"model\_type": "RandomForest", "dataset": "loan\_data"} | 2023-08-01 01:30:00 | 2023-08-01 02:15:00 |

---

### **4. Streaming\_Metadata Table (For Spark Streaming)**

This table will store metadata for **Spark Structured Streaming** jobs. These are typically used for real-time data streaming.

#### Sample Entries:

| **streaming\_id** | **streaming\_job\_name**            | **status** | **start\_time**     | **end\_time**       | **duration** | **parameters**                                                                                            | **created\_at**     | **updated\_at**     |
| ----------------- | ----------------------------------- | ---------- | ------------------- | ------------------- | ------------ | --------------------------------------------------------------------------------------------------------- | ------------------- | ------------------- |
| 1                 | RealTime\_Loan\_Application\_Stream | Running    | 2023-08-01 00:00:00 | NULL                | Ongoing      | {"source": "Kafka", "topic": "loan\_applications", "checkpoint\_location": "/mnt/checkpoints/loan\_app"}  | 2023-08-01 00:00:00 | NULL                |
| 2                 | RealTime\_Loan\_Approval\_Stream    | Failed     | 2023-08-01 01:00:00 | 2023-08-01 01:15:00 | 15 minutes   | {"source": "Kafka", "topic": "loan\_approvals", "checkpoint\_location": "/mnt/checkpoints/loan\_approve"} | 2023-08-01 01:00:00 | 2023-08-01 01:15:00 |

---

### **5. Job\_Metadata Table (For Batch and Streaming Jobs)**

Captures metadata for all **job executions**, whether batch or streaming.

#### Sample Entries:

| **job\_id** | **job\_name**                    | **job\_type** | **frequency** | **status** | **start\_time**     | **end\_time**       | **created\_at**     | **updated\_at**     |
| ----------- | -------------------------------- | ------------- | ------------- | ---------- | ------------------- | ------------------- | ------------------- | ------------------- |
| 1           | Loan\_Application\_Processing    | Batch         | Daily         | Completed  | 2023-08-01 00:00:00 | 2023-08-01 01:00:00 | 2023-08-01 00:00:00 | 2023-08-01 01:00:00 |
| 2           | RealTime\_Loan\_Approval\_Stream | Streaming     | Real-Time     | Running    | 2023-08-01 00:00:00 | NULL                | 2023-08-01 00:00:00 | NULL                |
| 3           | Default\_Risk\_Model\_Batch      | Batch         | Weekly        | Failed     | 2023-08-01 01:30:00 | 2023-08-01 02:15:00 | 2023-08-01 01:30:00 | 2023-08-01 02:15:00 |

---

### **6. Process\_Metadata Table (For Batch and Streaming Processes)**

Captures metadata for the **individual processes** within each job.

#### Sample Entries:

| **process\_id** | **process\_name** | **status** | **start\_time**     | **end\_time**       | **execution\_time** | **job\_id** | **created\_at**     | **updated\_at**     |
| --------------- | ----------------- | ---------- | ------------------- | ------------------- | ------------------- | ----------- | ------------------- | ------------------- |
| 1               | Data\_Cleansing   | Completed  | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 | 10 minutes          | 1           | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 |
| 2               | Risk\_Assessment  | Failed     | 2023-08-01 00:15:00    | 2023-08-01 00:30:00    | 15 minutes         | 1         | 2023-08-01 00:15:00   | 2023-08-01 00:30:00   |
| 3               | Loan\_Approval\_Evaluation    | Completed  | 2023-08-01 00:30:00    | 2023-08-01 00:45:00    | 15 minutes         | 1         | 2023-08-01 00:30:00   | 2023-08-01 00:45:00   |

---

### **7. Process\_Parameter\_Metadata Table (For Batch and Streaming Process Parameters)**

Captures parameters used in each process.

#### Sample Entries:

| **param\_id** | **process\_id** | **param\_name** | **param\_value** | **created\_at**     | **updated\_at**     |
| ------------- | --------------- | --------------- | ---------------- | ------------------- | ------------------- |
| 1             | 1               | batch\_size     | 100              | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 |
| 2             | 1               | region          | NY               | 2023-08-01 00:05:00 | 2023-08-01 00:15:00 |
| 3             | 2               | model\_type     | RandomForest     | 2023-08-01 00:15:00 | 2023-08-01 00:30:00 |
| 4             | 3               | loan\_type      | Home             | 2023-08-01 00:30:00 | 2023-08-01 00:45:00 |

---

### **8. Metadata\_Logs Table**

Captures any **changes or updates** made to metadata entries for auditing purposes.

#### Sample Entries:

| **log\_id** | **metadata\_type** | **metadata\_id** | **action** | **previous\_value**   | **new\_value**          | **updated\_by** | **updated\_at**     |
| ----------- | ------------------ | ---------------- | ---------- | --------------------- | ----------------------- | --------------- | ------------------- |
| 1           | ADF\_Metadata      | 1                | UPDATE     | {"status": "Running"} | {"status": "Completed"} | admin           | 2023-08-01 01:00:00 |
| 2           | Airflow\_Metadata  | 3                | UPDATE     | {"status": "Pending"} | {"status": "Failed"}    | user2           | 2023-08-01 00:40:00 |

---

