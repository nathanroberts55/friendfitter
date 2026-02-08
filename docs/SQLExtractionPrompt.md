"Please act as a data entry specialist. Analyze the attached image of a sewing pattern envelope (the filename is [INSERT FILENAME HERE]) and extract the body measurements and fabric requirements to generate a SQL script for a PostgreSQL database.

Please follow these strict requirements:

Structure: For each view (View A, B, C, D, E), create a separate record in the core_pattern table.

Naming Convention: Base the name on the filename provided. Use the format: '[FILENAME] - [Category] ([View Letter])'.

Data Extraction & Conversion:

Extract the corresponding size measurements (Bust, Waist, Hip) and fabric requirements for every size available for that specific view.

Conversion Rule: Convert all fabric yardage measurements into inches (multiply yards by 36) before inserting them into the database.

Body Measurement Nuance: Sizes may be listed as numbers (4, 6) or letters (S, M, L). If a size is listed as a range (e.g., '14-16'), use the highest measurements for that specific size range.

SQL Syntax: Use PostgreSQL BEGIN; and COMMIT; to make it a single transaction. Use a DO $$ DECLARE ... BEGIN block to capture the currval() of the core_pattern table's serial ID to accurately link the size requirements to the correct pattern record.

Data Format: Use numeric types for measurements.

Formatting: Remove any single quotes (apostrophes) from names (e.g., use 'Womens' instead of 'Women's') to prevent syntax errors."
