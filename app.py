import kagglehub
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    path = kagglehub.dataset_download("mehmettahiraslan/customer-shopping-dataset")
    df = pd.read_csv(path + "/customer_shopping_data.csv")
    return df

df = get_data_from_excel()

df['total_price'] = df['quantity'] * df['price']

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
shopping_mall = st.sidebar.multiselect(
    "Select the Shopping Mall:",
    options=df["shopping_mall"].unique(),
    default=df["shopping_mall"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

df_selection = df.query(
    "shopping_mall == @shopping_mall & Gender == @gender"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = round(df_selection["total_price"].sum())
average_sale_by_transaction = round(df_selection["total_price"].mean(), 2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"{total_sales:,} TL")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"{average_sale_by_transaction} TL")

st.markdown("""---""")

# SALES BY Category [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["category"])[["total_price"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="total_price",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Category</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


left_column, right_column = st.columns(2)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)