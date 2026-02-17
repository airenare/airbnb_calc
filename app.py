import streamlit as st

# Enable wide mode
st.set_page_config(layout="wide")

# SIDEBAR
sidebar = st.sidebar
sidebar.header("Parameters not changed often")
## Mortgage
sidebar.subheader("Mortgage")
side_col1, side_col2 = sidebar.columns(2)
with side_col1:
    mortgage_rate = st.number_input("Mortgage Rate", value=0.080, step=0.005, format="%.3f")
with side_col2:
    mortgage_term_years = st.number_input("Mortgage Term", value=30)

sidebar.divider()

## AirBnB
sidebar.subheader("AirBnB")
sidebar.write("Fees are either 3% or 15.5% depending on the host's choice. The default is 15.5% (0.155).")
airbnb_fee_rate = sidebar.number_input("Airbnb Fee", value=0.155, format="%.3f", step = 0.005)

sidebar.divider()

## Management
sidebar.subheader("Management")
sidebar.write("Management fees are typically around 20% (0.20) of the revenuenue.")
management_fee_rate = sidebar.number_input("Management Fee", value=0.20, format="%.2f", step=0.005)

sidebar.divider()

## Property tax
sidebar.subheader("Property Tax")
sidebar.write("Average is around 0.8% of the property value annually.")
tax_rate = sidebar.number_input("Property Tax Rate", value=0.008, format="%.3f", step=0.005)

sidebar.divider()

## Utilities and other costs
sidebar.subheader("Utilities and Other Costs")
electricity_cost = sidebar.number_input("Monthly Electricity Cost", value=100)
water_cost = sidebar.number_input("Monthly Water Cost", value=50)
gas_cost = sidebar.number_input("Monthly Gas Cost", value=0)
garbage_collection_cost = sidebar.number_input("Monthly Garbage Collection Cost", value=30)
hoa_fee = sidebar.number_input("Monthly HOA Fee", value=150)

sidebar.divider()

## Insurance
sidebar.subheader("Insurance")
insurance_cost = sidebar.number_input("Monthly Insurance Cost", value=200)



# MAIN PAGE
#st.title("Airbnb Profit Calculator")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Property")
    scol1, scol2 = st.columns(2)
    with scol1:
        property_price = st.number_input("Price ($)", value=400000, min_value=10000, max_value=1000000, step=10000)
    with scol2:
        downpayment = st.number_input("Down ($)", value=0, min_value=0, max_value=property_price, step=10000)

    
    with scol1:
        # Calculate monthly mortgage payment
        mortgage_amount = property_price - downpayment
        monthly_mortgage_payment = (mortgage_amount * mortgage_rate / 12) / (1 - (1 + mortgage_rate / 12) ** (-mortgage_term_years * 12))
        annual_mortgage_payment = (mortgage_amount * mortgage_rate) / (1 - (1 + mortgage_rate) ** (-mortgage_term_years))

        st.write(f"Monthly Mortgage: ${monthly_mortgage_payment:,.0f}")
        st.write(f"Annual Mortgage: ${annual_mortgage_payment:,.0f}")
    
    st.divider()
    st.subheader("Renovation and Furnishing")
    with col1:
        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            renovation_costs = st.number_input("Costs ($)", value=45000, min_value=0, step=5000)
        with scol2:
            renovation_loan_years = st.number_input("Length of loan", value=5, min_value=1, max_value=50, step=1)
        with scol3:
            renovation_loan_rate = st.number_input("Renovation Loan Rate", value=0.080, step=0.005, format="%.3f")
    monthly_renovation_payment = renovation_costs * renovation_loan_rate / 12 / (1 - (1 + renovation_loan_rate / 12) ** (-renovation_loan_years * 12))
    annual_renovation_payment = renovation_costs * renovation_loan_rate / (1 - (1 + renovation_loan_rate) ** (-renovation_loan_years))
    
    st.write(f"Monthly Renovation Loan: ${monthly_renovation_payment:,.0f}")
    st.write(f"Annual Renovation Loan: ${annual_renovation_payment:,.0f}")
    
    
with col2:
    st.subheader("Airbnb")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        nightly_rate = st.number_input("Nightly Rate ($)", value=400, step=10)

    with s_col2:
        occupancy_rate = st.number_input("Occupancy Rate", value=0.45)
    st.write(f"Gross Monthly: ${nightly_rate * occupancy_rate * 30:,.0f}")
    st.write(f"Gross Annual: ${nightly_rate * occupancy_rate * 365:,.0f}")

st.divider()
# Calculate monthly revenue
days_in_month = 30
monthly_revenue = nightly_rate * occupancy_rate * days_in_month
annual_revenue = nightly_rate * occupancy_rate * 365

# Calculate monthly AirBnB fee
monthly_airbnb_fee = monthly_revenue * airbnb_fee_rate
annual_airbnb_fee = annual_revenue * airbnb_fee_rate

# Calculate monthly tax
monthly_tax = property_price * tax_rate / 12
annual_tax = property_price * tax_rate

# Calculate monthly management fee
monthly_management_fee = monthly_revenue * management_fee_rate
annual_management_fee = annual_revenue * management_fee_rate

# Total monthly expenses
total_monthly_expenses = monthly_mortgage_payment + monthly_renovation_payment +monthly_tax + monthly_management_fee + electricity_cost + water_cost + gas_cost+ garbage_collection_cost + insurance_cost + hoa_fee
total_annual_expenses = annual_mortgage_payment + annual_renovation_payment + annual_tax + annual_management_fee + electricity_cost * 12 + water_cost * 12 + gas_cost * 12 + garbage_collection_cost * 12 + insurance_cost * 12 + hoa_fee * 12
# Dictionary of expenses
expenses = {
    "Mortgage Payment": [monthly_mortgage_payment, annual_mortgage_payment],
    "Renovation Loan Payment": [monthly_renovation_payment, annual_renovation_payment],
    "Property Tax": [monthly_tax, annual_tax],
    "Management Fee": [monthly_management_fee, annual_management_fee],
    "AirBnB Fee": [monthly_airbnb_fee, annual_airbnb_fee],
    "Electricity": [electricity_cost, electricity_cost * 12],
    "Water": [water_cost, water_cost * 12],
    "Gas": [gas_cost, gas_cost * 12],
    "Garbage Collection": [garbage_collection_cost, garbage_collection_cost * 12],
    "Insurance": [insurance_cost, insurance_cost * 12],
    "HOA Fee": [hoa_fee, hoa_fee * 12]
}

# Net monthly profit
net_monthly_profit = monthly_revenue - total_monthly_expenses
net_annual_profit = annual_revenue - total_annual_expenses


## RESULTS
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.header("Expenses")
    st.write(f"\${total_monthly_expenses:,.0f} per month")
    st.subheader(f"\${total_annual_expenses:,.0f}")


with col2:
    st.header("Revenue")
    st.write(f"\${monthly_revenue:,.0f} per month")
    st.subheader(f"\${annual_revenue:,.0f}")

with col3:
    st.header("Profit")
    st.write(f"\${net_monthly_profit:,.0f} per month")
    st.subheader(f"\${net_annual_profit:,.0f}")

with col4:
    st.header("Margin")
    if monthly_revenue > 0:
        margin_monthly = (net_monthly_profit / monthly_revenue) * 100
        margin_annual = (net_annual_profit / annual_revenue) * 100
        st.write(f"{margin_monthly:.0f}% per month")
        st.subheader(f"{margin_annual:.0f}%")
    else:
        st.write("N/A")
        st.subheader("N/A")

with col5:
    st.header("ROI")
    total_investment = downpayment + renovation_costs
    if total_investment > 0:
        roi_monthly = (net_monthly_profit * 12) / total_investment * 100
        roi_annual = (net_annual_profit) / total_investment * 100
        st.write(f"{roi_monthly:.0f}% per month")
        st.subheader(f"{roi_annual:.0f}%")
    else:
        st.write("N/A")
        st.subheader("N/A")
st.divider()
# Expense breakdown from the dictionary
st.subheader("Expense Breakdown")
expense_df = {
    "Expense": list(expenses.keys()),
    "Monthly Cost": [f"${cost[0]:,.0f}" for cost in expenses.values()],
    "Annual Cost": [f"${cost[1]:,.0f}" for cost in expenses.values()]
}
st.table(expense_df)