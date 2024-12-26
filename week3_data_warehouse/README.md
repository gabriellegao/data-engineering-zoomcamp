## OLTP and OLAP
### OLTP (Online Transaction Processing)
OLTP refers to systems designed to handle a large number of short, real-time transactions. These sytems are optimized for fast insert, update and delete operations, and they prioritize data integrity and consistency.

1. Purpose: manage day-to-day transactional data
1. Operations: read and write (e.g. insert, update, delete)
1. Data Volume: handles small amount of data per transactions but processes a large number of transations. 
1. Speed: prioritize fast, real-time processing
1. Normalization: highly normalized to avoid data redundancy and ensure data consistency

### OLAP (Online Analytics Processing)
OLAP refers to systems designed for complex analytical queries and reporting. These systems aggregate large volumes of historical data to provide insights and support decision-making.

1. Purpose: analyze data for business intelligence and decision-making
2. Operations: handle complex read-heavy queries (e.g. aggregations, joins, and data slicing)
3. Data Volume: Processes large volumes of historical data
4. Speed: prioritize query performance
5. Denormalization: apply denormalized structures like star or snowflake schemas for faster queries.

## Normalization and Denormalization 
### Normalization
Data is split into multiple realted tables. Each table focuses on a single subject
1. Reduced redundancy: avoid duplications across tables
2. Improved consistency

### Denormalization
Data from multiple tables is consolidated into fewer tables or a single table, often including duplicated data to reduce the need for complex joins and improve query performance.
1. Faster Reads
2. Simpler Queries: data is stored in a flat structure, making it easier to query.
