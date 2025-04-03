🚀 Agricultural Data Analysis & Visualization Project
📌 Project Overview
This project focuses on Agricultural Production Data Analysis using ICRISAT District Level Data. The objective is to clean, analyze, and visualize agricultural production trends across Indian states and districts. The analysis includes crops like Rice, Wheat, Maize, Oilseeds, Cotton, Groundnut, etc. The insights are visualized using Power BI and queried using MySQL.

📂 Folder Structure
mathematica
Copy
Edit
guvi_project/
├── agricultural.csv                  → Cleaned data file
├── agriculture1.py                   → Python code for data cleaning & MySQL upload
├── ICRISAT-District Level Data.csv   → Raw dataset
├── agriculturdatavisualisation.pbix  → Power BI Visualization File
└── README.md                         → Project Documentation
🔥 Project Steps
1. Data Cleaning
Performed the following cleaning steps using Python and Pandas:

Removed unnecessary characters from column names and standardized them.

Converted production and area units to consistent formats (kg, ha).

Removed negative and zero values.

Saved the cleaned dataset as agricultural.csv.

2. SQL Database Connection & Data Upload
Connected to MySQL Database using SQLAlchemy.

Created a database agridata.

Split data into multiple tables:

ricedata

wheat_states

maize

oilseed

cotton

And others (finger millet, groundnut, pulses, etc.).

Uploaded cleaned datasets to respective MySQL tables.

3. Analysis & SQL Queries
Answered 10 insightful questions using SQL queries:

Query No.	Insight
1	Year-wise Trend of Rice Production Across Top 3 States
2	Top 5 Districts by Wheat Yield Increase (Last 5 Years)
3	States with Highest Growth in Oilseed Production (5-Year Growth Rate)
4	District-wise Correlation Between Area & Production (Rice, Wheat, Maize)
5	Yearly Cotton Production Growth in Top 5 Producing States
6	Districts with Highest Groundnut Production in 2020
7	Annual Average Maize Yield Across All States
8	Total Area Cultivated for Oilseeds in Each State
9	Districts with the Highest Rice Yield
10	Compare Wheat & Rice Production for Top 5 States (Last 10 Years)
The queries are written in agriculture1.py and stored in SQL tables (sqlquery1 - sqlquery10).

4. Power BI Visualization
Connected Power BI to MySQL Database (agridata).

Built interactive dashboards to represent:

Year-wise production trends.

Crop-wise state/district performance.

Correlation between area & production.

Growth percentages.

The .pbix file is named agriculturedatavisualisation.pbix.

⚙️ How to Access & Run
1. Clone the Repository
git clone https://github.com/NarayanSan/guvi_project.git
cd guvi_project
2. Install Required Python Libraries
pip install pandas mysql-connector-python SQLAlchemy
3. Run Python Cleaning & Upload Script
python agriculture1.py
4. Power BI Dashboard
Open agriculturedatavisualisation.pbix in Power BI Desktop.

Ensure your MySQL server is running.

Update the Database Connection settings in Power BI if needed.

🌱 Outcome
✅ Cleaned & normalized agricultural dataset
✅ SQL-based advanced analysis
✅ Interactive Power BI visualization dashboard


