# etl_pipeline_transform

**Overview**

I designed a dual-path data transformation workflow to support both local development and production needs. For local testing, I implemented JSON normalization routines leveraging Python pandas and json package file to quickly validate raw data structure and logic before deployment. 

For production, I built a scalable and modular dbt pipeline with Snowflake as the target warehouse. This included configuring secure dbt-Snowflake integration, structuring the project with `dbt_project.yml`, and developing clean source and staging models. I followed best practices to build fact and dimension tables, implemented reusable macros for consistency, and applied both generic and custom tests to ensure data quality. This approach allowed rapid iteration in development while maintaining rigorous standards in production.
