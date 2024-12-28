## ETL vs ELT
ETL or ELT is composed of three main stages - extract, transform, and load. 
### ETL
1. Slight more stable and compliant data analysis
2. Higher storage and compute costs

### ELT
1. Faster and more flexible data analysis
2. Lower cost and lower maintenance.

## Dimensisonal Modeling
### Elements of Dimensional Modeling
Facts table  
Dimension table
### Architecture of Dimensional Modeling
Stage area
Processing area
Presentation area

## DBT
dbt (data build tool) is designed to tranform raw data to ready-to-use data using SQL. dbt also provides functionalities, like deployment (version control and CI/CD), test and document, and development

### Materializations
1. Ephemeral
   It's a temporary view and only exist during a single dbt run
2. View
   View is a query-based table built on the top of the real table
3. Table
   Table is physical representation of data that are created and stored in the database
4. Incremental
   Incremental materialization decribe a process of incrementally loading new data to the existing table without dropping the whole table and recreate it again.

### Macro
Macro is a function acted like def function in python

There are two ways to define or call a macro function
```dbt
{{ macro_statement }} <-- double curly brackets
{% macro_statement %} <-- single curly brackets with a symbol
```

### Packages
Packages is dbt's libraries, including models and macros

### Variables
Variable defines value used across the project. It can be defined in two ways:
1. In `dbt_project.yml` file
2. On command line
```dbt
{{ var('variable_value') }}
```

### Build Table
```dbt
dbt build
```

### Install Packages
```dbt
dbt deps
```