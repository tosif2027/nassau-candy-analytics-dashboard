import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Nassau Candy Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

div[data-testid="metric-container"]{
    background:linear-gradient(135deg,#1A1A1A,#222B36);
    border:2px solid #00E5FF;
    padding:18px;
    border-radius:18px;
    box-shadow:0px 0px 15px rgba(0,229,255,0.35);
}

button[data-baseweb="tab"]{
    font-size:16px;
    font-weight:bold;
}

button[data-baseweb="tab"][aria-selected="true"]{
    color:#00E5FF;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #141A22,
        #1D2633
    );
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

section[data-testid="stSidebar"]{
    background-color:#161A23;
}

</style>
""", unsafe_allow_html=True)

sns.set_theme(
    style="darkgrid",
    context="notebook"
)

plt.style.use("dark_background")

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df.columns = df.columns.str.strip()

    df["Margin %"] = (
        df["Gross Profit"] /
        df["Sales"]
    ) * 100

    df["Profit Per Unit"] = (
        df["Gross Profit"] /
        df["Units"]
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
)

    return df

df = load_data()


st.markdown("""
<h1 style='text-align:center;
color:#00E5FF;
text-shadow:0px 0px 20px #00E5FF;'>
📊 Nassau Candy Analytics Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center;
font-size:18px;
color:white;'>
Product Line Profitability & Margin Performance Analysis
</p>
""", unsafe_allow_html=True)

with st.expander("Project Objective"):
    st.write("""
Analyze profitability, margin performance,
division contribution and product performance
for Nassau Candy Distributor.
""")

st.sidebar.header("Dashboard Filters")

division_filter = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Division"].isin(division_filter))
    &
    (df["Region"].isin(region_filter))
]


total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Gross Profit"].sum()

total_cost = filtered_df["Cost"].sum()

avg_margin = filtered_df["Margin %"].mean()

st.markdown("## 📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"${total_sales:,.0f}"
)

col2.metric(
    "📈 Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "💸 Cost",
    f"${total_cost:,.0f}"
)

col4.metric(
    "📊 Avg Margin",
    f"{avg_margin:.2f}%"
)

st.markdown("---")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
[
    "📈 Overview",
    "📦 Products",
    "🏢 Divisions",
    "📊 Pareto",
    "📋 Data Explorer"
]
)


with tab1:

    st.subheader("Revenue by Division")

    division_sales = (
        filtered_df.groupby("Division")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6,3))

    sns.barplot(
    x=division_sales.values,
    y=division_sales.index,
    ax=ax
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Margin Distribution")

    fig, ax = plt.subplots(figsize=(6,3))

    sns.histplot(
        filtered_df["Margin %"],
        bins=25,
        kde=True,
        ax=ax
    )

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Revenue by Region")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.barplot(
    x=region_sales.values,
    y=region_sales.index,
    ax=ax
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)


with tab2:

    st.subheader("🏆 Top 10 Profitable Products")

    top_products = (
        filtered_df.groupby("Product Name")
        ["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.barplot(
        x=top_products.values,
        y=top_products.index,
        ax=ax
    )

    ax.set_xlabel("Gross Profit")
    ax.set_ylabel("")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("⚠️ Bottom 10 Products")

    bottom_products = (
        filtered_df.groupby("Product Name")
        ["Gross Profit"]
        .sum()
        .sort_values()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.barplot(
        x=bottom_products.values,
        y=bottom_products.index,
        ax=ax
    )

    ax.set_xlabel("Gross Profit")
    ax.set_ylabel("")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("💰 Top 10 Products by Sales")

    top_sales_products = (
        filtered_df.groupby("Product Name")
        ["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.barplot(
        x=top_sales_products.values,
        y=top_sales_products.index,
        ax=ax
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)


with tab3:

    st.subheader("🏢 Division Wise Profit")

    division_profit = (
        filtered_df.groupby("Division")
        ["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.barplot(
        x=division_profit.values,
        y=division_profit.index,
        ax=ax
    )

    ax.set_xlabel("Profit")
    ax.set_ylabel("")

    plt.xticks(rotation=15)

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("💸 Cost vs Profit Analysis")

    fig, ax = plt.subplots(figsize=(4,2.5))

    sns.scatterplot(
        data=filtered_df,
        x="Cost",
        y="Gross Profit",
        hue="Division",
        ax=ax
    )

    ax.set_xlabel("Cost")
    ax.set_ylabel("Gross Profit")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)


with tab4:

    st.subheader("📊 Pareto Analysis (80/20 Rule)")

    pareto = (
        filtered_df.groupby("Product Name")
        ["Gross Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto["Cumulative Profit"] = (
        pareto["Gross Profit"].cumsum()
    )

    pareto["Cumulative %"] = (
        pareto["Cumulative Profit"]
        /
        pareto["Gross Profit"].sum()
    ) * 100

    fig, ax = plt.subplots(figsize=(6,3))

    ax.plot(
        pareto.index,
        pareto["Cumulative %"],
        linewidth=3
    )

    ax.axhline(
        y=80,
        linestyle="--"
    )

    ax.set_ylabel(
        "Cumulative Profit %"
    )

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
        st.pyplot(fig)

    top20 = max(
        1,
        int(len(pareto) * 0.2)
    )

    profit_share = (
        pareto.head(top20)
        ["Gross Profit"]
        .sum()
        /
        pareto["Gross Profit"].sum()
    ) * 100

    st.success(
        f"Top 20% products contribute approximately {profit_share:.2f}% of total profit."
    )


with tab5:

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )

    st.write(
        f"Total Records: {len(filtered_df)}"
    )


st.markdown("""
<h2 style='color:#00E5FF;'>
📌 Business Insights & Recommendations
</h2>
""", unsafe_allow_html=True)

top_division = (
    filtered_df.groupby("Division")
    ["Gross Profit"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Gross Profit"]
    .sum()
    .idxmax()
)

top_product = (
    filtered_df.groupby("Product Name")
    ["Gross Profit"]
    .sum()
    .idxmax()
)

st.success(
f"""
🏆 Top Division: {top_division}

🌎 Top Region: {top_region}

📦 Best Product: {top_product}

📈 Average Margin: {avg_margin:.2f}%

Recommendations:

• Focus on high-margin products

• Increase inventory of top-selling products

• Optimize cost-heavy products

• Improve low-profit product lines

• Invest more in top-performing divisions and regions
"""
)

st.markdown("---")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_nassau_data.csv",
    mime="text/csv"
)


