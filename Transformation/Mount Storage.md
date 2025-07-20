
### **Steps to Mount ADLS Gen2 Storage with Unity Catalog in Databricks**

#### **1. Create a Unity Catalog Metastore (if not already done)**

Before proceeding, ensure that you've set up the **Unity Catalog** for your Databricks workspace. Unity Catalog provides a central governance layer for all data assets in your Databricks environment.

* Go to the **Databricks Workspace**.
* In the **Admin Console**, navigate to **Unity Catalog**.
* Create a **Metastore** (if you don’t have one already) for your data.

#### **2. Mount ADLS Gen2 Storage using Unity Catalog**

Now, you can mount your **ADLS Gen2** container to your **Databricks workspace** through the **Unity Catalog**. This allows you to reference data stored in **ADLS Gen2** and manage it through Unity Catalog.

You will need to create a **Mount** of ADLS Gen2 through **Databricks**, with Unity Catalog applied.

Here’s how to mount your **ADLS Gen2** with Unity Catalog.

---

### **Mount ADLS Gen2 in Databricks with Unity Catalog**

#### **Step 1: Configure Unity Catalog in Databricks**

Unity Catalog integration with **ADLS Gen2** is done at the **catalog** level. You must create a catalog that points to your **ADLS Gen2** storage. Once the catalog is created, you can access the data as if it were stored natively in Databricks.

#### **Step 2: Define Permissions and Access Control**

Unity Catalog provides access control mechanisms for the data, allowing you to manage who can access the data in the **ADLS Gen2**.

Here’s how to define a catalog in Unity:

```python
# Create a Unity Catalog Table (Catalog and Schema creation should happen within Unity Catalog)
spark.sql("CREATE CATALOG IF NOT EXISTS loan_data USING DELTA LOCATION 'abfss://<container_name>@<storage_account_name>.dfs.core.windows.net/loan_data/'")
```

This SQL command creates a **Unity Catalog** catalog called **loan\_data** that points to the location on **ADLS Gen2**.

* Replace `<container_name>` with your container in ADLS Gen2.
* Replace `<storage_account_name>` with your Azure storage account name.

#### **Step 3: Configure and Access the Catalog in Databricks**

After the **catalog** is created, you can create **schemas** and **tables** within the catalog.

```python
# Create schema inside Unity Catalog
spark.sql("CREATE SCHEMA IF NOT EXISTS loan_data.loan_applications")
```

This command creates a **schema** inside the **loan\_data** catalog, called **loan\_applications**.

#### **Step 4: Access Data from the Catalog in PySpark**

After setting up the catalog, you can read and write data to the mounted storage from your notebooks and jobs.

```python
# Access data from Unity Catalog (Bronze Layer)
df = spark.read.format("delta").table("loan_data.loan_applications.loan_data_table")
df.show()
```

Here, you are reading data from the **loan\_data** catalog, **loan\_applications** schema, and **loan\_data\_table** Delta table.

---

### **Step-by-Step PySpark Code for Mounting ADLS Gen2 and Using Unity Catalog**

Let’s go step by step to set up **ADLS Gen2** and **Unity Catalog** integration using **PySpark**.

---

### **1. Setup Azure Key Vault for Authentication (Optional, Recommended)**

You can store your secrets, such as storage account credentials, securely in **Azure Key Vault**. Then, access those credentials via **Databricks secrets**.

```bash
# Create a Databricks secret scope for Azure Key Vault secrets
databricks secrets create-scope --scope <scope_name> --scope-backend-type AZURE_KEYVAULT --resource-id <resource_id> --vault-name <key_vault_name>
```

---

### **2. Set Up Spark to Access ADLS Gen2 via Unity Catalog**

Once the **catalog** and **schema** are created, you can mount the ADLS Gen2 storage and access the **Bronze Layer** data.

Here’s the step-by-step code in **PySpark** to mount the storage:

```python
# Mount the ADLS Gen2 Storage to Unity Catalog using DBFS
dbutils.fs.mount(
  source = "abfss://<container_name>@<storage_account_name>.dfs.core.windows.net/",
  mount_point = "/mnt/<mount_name>",  # Mount point in DBFS
  extra_configs = {"<conf-key>":dbutils.secrets.get(scope = "<scope_name>", key = "<key_name>")}
)
```

* Replace `<container_name>`, `<storage_account_name>`, `<mount_name>`, and the **secret configurations** with your actual values.

---

