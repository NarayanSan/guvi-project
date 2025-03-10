import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_option_menu import option_menu

# Set page configuration with wide layout
st.set_page_config(page_title="Business Insights", page_icon="📊",layout="wide")

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Connection"

# Create the navigation bar using streamlit-option-menu
selected_page = option_menu(
    menu_title=None,
    options=[
        "Data Cleaning", 
        "Connection", 
        "Business Insights", 
        "General Insights",
        "General Insights Part 2"  # New page added here
    ],
    icons=[
        "broom", 
        "plug", 
        "bar-chart-line", 
        "graph-up-arrow",
        "bar-chart"  # Add an appropriate icon for the new page
    ],
    menu_icon="cast",
    default_index=[
        "Data Cleaning", 
        "Connection", 
        "Business Insights", 
        "General Insights",
        "General Insights Part 2"  # Make sure the default index handles the new page
    ].index(st.session_state.get("selected_page", "Data Cleaning")),
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1f2a3c"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {
            "font-size": "18px",
            "text-align": "center",
            "margin": "0px",
            "color": "white",
        },
        "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
    },
)
def connection_string():
    try:
        connection = mysql.connector.connect(host = "localhost",
                                             user = "root",
                                             password = "")
        if connection.is_connected():
             st.session_state.connected = True
             
             #st.session_state.page = "page2"
             #mycursor = connection.cursor()
             #mycursor.execute("SHOW DATABASES")
             #databases = mycursor.fetchall()
             #st.subheader("Available Databases:")
             #for db in databases:
                #st.write(db[0])
        
        else:
            st.error("Failed to connect to the database.")
            st.session_state.connected = False
    except Exception as e:
        st.error(f"Connection failed: {e}")
        st.session_state.connected= False
        connection.close()



# Check for the selected page and navigate accordingly
if selected_page == "Connection":
    st.title("Welcome to my Project")
    st.header("I have established my connection to the sql server for the retail project")
    if st.button("Connect to MySQL Database"):
        connection_string()
        st.subheader("Connected to the sql server local server")
        #if st.button("Go to Business Insights"):
            #st.session_state.selected_page = "Business Insights"

elif selected_page == "Business Insights":
    st.title("Business Insights")

    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    mycursor = connection.cursor()

    # Define business insight options
    insight_options = [
        "Select a business insight...",
        "Top-Selling Products: Identify products with the highest revenue.",
        "Monthly Sales Analysis: Compare year-over-year sales trends.",
        "Product Performance: Rank products by revenue, profit margin, etc.",
        "Regional Sales Analysis: Identify best-performing sales regions.",
        "Discount Analysis: Evaluate the impact of discounts on sales."
    ]

    # Dropdown to select a business insight
    selected_insights = st.selectbox("Choose a business insight to explore", insight_options)

    # Handle selection and display relevant data
    if selected_insights == "Top-Selling Products: Identify products with the highest revenue.":
        st.subheader("Top Selling Products")
        mycursor.execute("""
            SELECT CATEGORY, SUM(SALE_PRICE) AS TOTAL_REVENUE 
            FROM retail_analysis.DF_ORDERS2
            GROUP BY CATEGORY
            ORDER BY TOTAL_REVENUE DESC
        """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

    elif selected_insights == "Monthly Sales Analysis: Compare year-over-year sales trends.":
        st.subheader("Monthly Sales Analysis")
        mycursor.execute("""
            SELECT DATE_FORMAT(ORDER_DATE, '%Y-%m') AS MONTH, SUM(SALE_PRICE) AS TOTAL_SALES 
            FROM RETAIL_ANALYSIS.DF_ORDERS2 
            GROUP BY MONTH 
            ORDER BY MONTH ASC
        """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

    elif selected_insights == "Regional Sales Analysis: Identify best-performing sales regions.":
        st.subheader("Regional Sales Analysis")
        mycursor.execute("""
            SELECT DF1.REGION AS REGION, SUM(DF2.SALE_PRICE) AS TOTAL_SALES 
            FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1
            INNER JOIN RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 ON DF1.ORDER_ID = DF2.ORDER_ID
            GROUP BY REGION
            ORDER BY TOTAL_SALES DESC
        """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

    elif selected_insights == "Product Performance: Rank products by revenue, profit margin, etc.":
        st.subheader("Product Performance Analysis")
        mycursor.execute("""
            SELECT 
                DF1.CATEGORY,
                SUM(DF2.SALE_PRICE) AS TOTAL_REVENUE,
                DF2.PROFIT, 
                ROW_NUMBER() OVER (ORDER BY DF2.SALE_PRICE DESC) AS REVENUE_RANK, 
                CASE 
                    WHEN DF2.PROFIT > 0.2 THEN 'HIGH MARGIN' 
                    ELSE 'LOW MARGIN' 
                END AS MARGIN_CATEGORY
            FROM 
                RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 
            INNER JOIN 
                RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 
            ON 
                DF1.ORDER_ID = DF2.ORDER_ID
            GROUP BY CATEGORY 
            ORDER BY TOTAL_REVENUE DESC
        """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

    elif selected_insights == "Discount Analysis: Evaluate the impact of discounts on sales.":
        st.subheader("Discount Analysis")
        mycursor.execute("""
            SELECT 
                DF1.CATEGORY, 
                DF2.SALE_PRICE, 
                DF2.DISCOUNT_PERCENT, 
                CASE 
                    WHEN DF2.DISCOUNT_PERCENT > 2 THEN 'HIGH DISCOUNT' 
                    ELSE 'LOW DISCOUNT' 
                END AS DISCOUNT_CATEGORY 
            FROM 
                RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 
            INNER JOIN 
                RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 
            ON DF1.ORDER_ID = DF2.ORDER_ID
        """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

elif selected_page == "General Insights":
    st.title("General Insights")
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    mycursor = connection.cursor()

    insight_options = [
    "Select a general insight...",
    "Top 10 Highest Revenue Generating Products",
    "Top 5 Cities with Highest Profit Margins",
    "Total Discount Given for Each Category",
    "Average Sale Price per Product Category",
    "Region with the Highest Average Sale Price",
    "Total Profit per Category",
    "Top 3 Segments with the Highest Quantity of Orders",
    "Average Discount Percentage Given per Region",
    "Product Category with the Highest Total Profit",
    "Total Revenue Generated per Year"]

    selected_insights = st.selectbox("Choose a general insight to explore", insight_options)

    if selected_insights == "Top 10 Highest Revenue Generating Products":
        st.header("Top 10 Highest Revenue Generating products")
        mycursor.execute("""
            SELECT PRODUCT_ID,CATEGORY,SUM(SALE_PRICE) AS TOTAL_REVENUE
            FROM RETAIL_ANALYSIS.DF_ORDERS2
            GROUP BY PRODUCT_ID
            ORDER BY TOTAL_REVENUE DESC
            LIMIT 10;""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Top 5 Cities with Highest Profit Margins":
        st.subheader("Top 5 Cities with Highest Profit Margins")
        mycursor.execute("""
            SELECT DF1.CITY, AVG(DF2.PROFIT) AS PROFIT_MARGIN
            FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 INNER JOIN 
            RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 ON DF1.ORDER_ID = DF2.ORDER_ID
            GROUP BY DF1.CITY
            ORDER BY PROFIT_MARGIN DESC
            LIMIT 5;""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Total Discount Given for Each Category":
        st.subheader("Total Discount Given for Each category")
        mycursor.execute("""SELECT CATEGORY, SUM(DISCOUNT_PERCENT) AS DISCOUNTED_CATEGORY
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY DISCOUNTED_CATEGORY DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Average Sale Price per Product Category":
        st.subheader("Average sale price per product category")
        mycursor.execute(""" SELECT CATEGORY, AVG(SALE_PRICE) AS AVG_SALE_PRICE
                         FROM RETAIL_ANALYSIS.DF_ORDERS1 
                         GROUP BY CATEGORY""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Region with the Highest Average Sale Price":
        st.subheader("Region with the Highest Average Sale Price")
        mycursor.execute("""SELECT DF1.REGION, AVG(DF2.SALE_PRICE) AS AVG_SALE_PRICE
                         FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 INNER JOIN
                         RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 ON DF1.ORDER_ID=DF2.ORDER_ID
                         GROUP BY DF1.REGION
                         ORDER BY AVG_SALE_PRICE DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Total Profit per Category":
        st.subheader("Total profit per category")
        mycursor.execute("""SELECT CATEGORY, SUM(PROFIT) AS TOTAL_PROFIT
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY TOTAL_PROFIT DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Top 3 Segments with the Highest Quantity of Orders":
        st.subheader("Top 3 Segments with the Highest Quantity of Orders")
        mycursor.execute("""SELECT SEGMENT, SUM(QUANTITY) AS HIGHEST_QUANTITY
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY SEGMENT
                         ORDER BY HIGHEST_QUANTITY DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Average Discount Percentage Given per Region":
        st.subheader("Average discount percentage given per region")
        mycursor.execute("""SELECT DF1.REGION, AVG(DF2.DISCOUNT_PERCENT) AS AVERAGE_DISCOUNT_PERCENTAGE FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1
                         INNER JOIN RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 ON DF1.ORDER_ID = DF2.ORDER_ID 
                         GROUP BY DF1.REGION
                         ORDER BY AVERAGE_DISCOUNT_PERCENTAGE DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Product Category with the Highest Total Profit": 
        st.subheader("Product category with the Highest total profit")
        mycursor.execute("""SELECT CATEGORY,SUM(PROFIT) AS TOTAL_PROFIT
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY 
                         ORDER BY TOTAL_PROFIT DESC
                         LIMIT 1 """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Total Revenue Generated per Year": 
        st.subheader("Total Revenue Generated per Year")
        mycursor.execute("""SELECT DATE_FORMAT(ORDER_DATE, '%Y') AS YEAR, SUM(SALE_PRICE) AS REVENUE_GENERATED
                         FROM RETAIL_ANALYSIS.DF_ORDERS2
                         GROUP BY YEAR
                         ORDER BY YEAR""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)

elif selected_page == "Data Cleaning":
    df=pd.read_csv("orders.csv")
    df_clean=df.dropna()
    df_clean= df_clean.rename(columns={'Order Id': 'order_id', 'Order Date': 'order_date','Ship Mode':'ship_mode','Segment':'segment','Country':'country','City':'city','State':'state','Region':'region','Category':'category','Postal Code':'postal_code','Sub Category':'sub_category','Product Id':'product_id','cost price':'cost_price','List Price':'list_price','Quantity':'quantity','Discount Percent':'discount_percent'})
    df_clean=df_clean.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df_clean['discount'] = (df_clean['discount_percent'] /100)*df_clean['list_price']
    df_clean['discounted_price'] = df_clean['list_price']-df_clean['discount']
    df_clean['sale_price']=df_clean['list_price']*(1-(df_clean['discount_percent'])/100)
    df_clean['profit'] = df_clean['sale_price'] - df_clean['cost_price']
    column_list1 = ["order_id","order_date","ship_mode","segment","country","city","state","postal_code","region","category","sub_category","product_id"]
    column_list2 = ['order_id',"order_date","ship_mode","segment","category","sub_category",'product_id','cost_price',"list_price","quantity","discount_percent","discount","discounted_price","sale_price","profit"]
    df_clean1 = df_clean[column_list1]
    df_clean2 = df_clean[column_list2]
    st.subheader("Cleaned dataset part 1")
    st.dataframe(df_clean1)
    st.subheader("Cleaned dataset part 2")
    st.dataframe(df_clean2)
elif selected_page== "General Insights Part 2":
    st.title("General Insights Part 2")
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    mycursor = connection.cursor()

    insight_options = ["Select an additional insight...",
    "Top 10 Most Profitable Products",
    "Sales by Shipping Mode",
    "Average Discount per Product Category",
    "Month with the Highest Sales",
    "Average Profit Margin per Region",
    "Top 5 States with the Highest Order Quantity",
    "Category with the Highest Average Sale Price",
    "Average Profit Obtained by Each Product Category",
    "Average Order Value per Segment",
    "Products with the Highest Repeat Orders"]

    selected_insights = st.selectbox("Choose a general insight to explore", insight_options)

    if selected_insights == "Top 10 Most Profitable Products":
        st.subheader("Top 10 Most Profitable Products")
        mycursor.execute("""SELECT PRODUCT_ID, SUM(PROFIT) AS TOTAL_PROFIT 
                         FROM retail_analysis.DF_ORDERS2 
                         GROUP BY PRODUCT_ID 
                         ORDER BY TOTAL_PROFIT DESC 
                         LIMIT 10; """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights =="Sales by Shipping Mode":
        st.subheader("Sales by shipping mode")
        mycursor.execute("""SELECT SHIP_MODE, SUM(SALE_PRICE) AS SALES_SHIPPING
                         FROM RETAIL_ANALYSIS.DF_ORDERS2
                         GROUP BY SHIP_MODE
                         ORDER BY SALES_SHIPPING DESC """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Average Discount per Product Category":
        st.subheader("Average Discount per product category ")
        mycursor.execute("""SELECT CATEGORY, AVG(DISCOUNT_PERCENT) AS DISCOUNT_PERCENT
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY DISCOUNT_PERCENT""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Top 5 States with the Highest Order Quantity":
        st.subheader("Top 5 states with the highest order quantity ")
        mycursor.execute("""SELECT DF1.STATE, SUM(DF2.QUANTITY) AS QUANTITY_TOTAL
                         FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 INNER JOIN 
                         RETAIL_ANALYSIS.DF_ORDERS2 AS DF2 ON DF1.ORDER_ID = DF2.ORDER_ID
                         GROUP BY DF1.STATE
                         ORDER BY QUANTITY_TOTAL DESC
                         LIMIT 5;  """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Month with the Highest Sales":
        st.subheader("Month with Highest sales ")
        mycursor.execute("""SELECT DATE_FORMAT(ORDER_DATE, '%M') AS ORDER1, SUM(SALE_PRICE) AS HIGHEST_SALES
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY ORDER1
                         ORDER BY ORDER1 DESC """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Average Profit Margin per Region":
        st.subheader("Average profit margin per region ")
        mycursor.execute("""SELECT DF1.REGION, AVG(DF2.PROFIT/DF2.SALE_PRICE*100) AS AVG_PROFIT_MARGIN
                         FROM RETAIL_ANALYSIS.DF_ORDERS1 AS DF1 INNER JOIN RETAIL_ANALYSIS.DF_ORDERS2 AS DF2
                         ON DF1.ORDER_ID=DF2.ORDER_ID
                         GROUP BY REGION""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Category with the Highest Average Sale Price":
        st.subheader("Category with the Highest Average Sale Price ")
        mycursor.execute("""SELECT CATEGORY, AVG(SALE_PRICE) AS AVG_SALE_PRICE
                        FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY AVG_SALE_PRICE
                         LIMIT 1; """)
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    
    elif selected_insights == "Average Order Value per Segment":
        st.subheader("Average Order Value per Segment")
        mycursor.execute("""SELECT SEGMENT, AVG(SALE_PRICE) AS ORDER_VALUE
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY SEGMENT
                         ORDER BY ORDER_VALUE DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Products with the Highest Repeat Orders":
        st.subheader("Products with the Highest Repeat orders")
        mycursor.execute("""SELECT CATEGORY, COUNT(QUANTITY) AS REPEAT_ORDERS
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY REPEAT_ORDERS DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)
    elif selected_insights == "Average Profit Obtained by Each Product Category":
        st.subheader("PAverage Profit Obtained by Each Product Category")
        mycursor.execute("""SELECT CATEGORY, AVG(PROFIT) AS AVG_PROFIT
                         FROM RETAIL_ANALYSIS.DF_ORDERS2 
                         GROUP BY CATEGORY
                         ORDER BY AVG_PROFIT DESC""")
        out = mycursor.fetchall()
        column = [i[0] for i in mycursor.description]
        df = pd.DataFrame(out, columns=column)
        st.dataframe(df)




