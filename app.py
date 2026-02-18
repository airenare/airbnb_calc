import streamlit as st
import numpy as np
import plotly.graph_objects as go
import default_values


# Enable wide mode
st.set_page_config(layout="wide", page_title="Airbnb Profit Calculator", page_icon="🏠")

# SIDEBAR
sidebar = st.sidebar
sidebar.header("Parameters not changed often")
## Mortgage
sidebar.subheader("Mortgage")
side_col1, side_col2 = sidebar.columns(2)
with side_col1:
    mortgage_rate = st.number_input("Mortgage Rate", value=default_values.mortgage_rate, step=0.005, format="%.3f")
with side_col2:
    mortgage_term_years = st.number_input("Mortgage Term", value=default_values.mortgage_term_years, step=1, format="%d")

sidebar.divider()

## AirBnB
sidebar.subheader("AirBnB")
sidebar.write("Fees are either 3% or 15.5% depending on the host's choice. The default is 15.5% (0.155).")
airbnb_fee_rate = sidebar.number_input("Airbnb Fee", value=default_values.airbnb_fee_rate, format="%.3f", step = 0.005)

sidebar.divider()

## Management
sidebar.subheader("Management")
sidebar.write("Management fees are typically around 20% (0.20) of the revenuenue.")
management_fee_rate = sidebar.number_input("Management Fee", value=default_values.management_fee_rate, format="%.2f", step=0.005)

sidebar.divider()

## Property tax
sidebar.subheader("Property Tax")
sidebar.write("Average is around 0.8% of the property value annually.")
tax_rate = sidebar.number_input("Property Tax Rate", value=default_values.tax_rate, format="%.3f", step=0.005)

sidebar.divider()

## Utilities and other costs
sidebar.subheader("Utilities and Other Costs")
electricity_cost = sidebar.number_input("Monthly Electricity Cost", value=default_values.electricity_cost)
water_cost = sidebar.number_input("Monthly Water Cost", value=default_values.water_cost)
gas_cost = sidebar.number_input("Monthly Gas Cost", value=default_values.gas_cost)
internet_cost = sidebar.number_input("Monthly Internet Cost", value=default_values.internet_cost)
garbage_collection_cost = sidebar.number_input("Monthly Garbage Collection Cost", value=default_values.garbage_collection_cost)
hoa_fee = sidebar.number_input("Monthly HOA Fee", value=default_values.hoa_fee)

sidebar.divider()

## Insurance
sidebar.subheader("Insurance")
insurance_cost = sidebar.number_input("Monthly Insurance Cost", value=default_values.insurance_cost)



# MAIN PAGE
#st.title("Airbnb Profit Calculator")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Property")
    scol1, scol2 = st.columns(2)
    with scol1:
        property_price = st.number_input("Price ($)", value=default_values.property_price, min_value=10000, max_value=1000000, step=10000)
    with scol2:
        downpayment = st.number_input("Down ($)", value=default_values.downpayment, min_value=0, max_value=property_price, step=10000)

    
    with scol1:
        # Calculate monthly mortgage payment
        mortgage_amount = property_price - downpayment
        monthly_mortgage_payment = (mortgage_amount * mortgage_rate / 12) / (1 - (1 + mortgage_rate / 12) ** (-mortgage_term_years * 12))
        annual_mortgage_payment = (mortgage_amount * mortgage_rate) / (1 - (1 + mortgage_rate) ** (-mortgage_term_years))

        st.write(f"Monthly Mortgage: ${monthly_mortgage_payment:,.0f}")
        st.write(f"Annual Mortgage: ${annual_mortgage_payment:,.0f}")
    
    with col2:
        st.subheader("Renovation and Furnishing")
        
        scol1, scol2, scol3 = st.columns(3)
        with scol1:
            renovation_costs = st.number_input("Costs ($)", value=default_values.renovation_cost, min_value=0, step=5000)
        with scol2:
            renovation_loan_years = st.number_input("Length of loan", value=default_values.renovation_loan_years, min_value=1, max_value=50, step=1)
        with scol3:
            renovation_loan_rate = st.number_input("Renovation Loan Rate", value=default_values.renovation_loan_rate, step=0.005, format="%.3f")
        monthly_renovation_payment = renovation_costs * renovation_loan_rate / 12 / (1 - (1 + renovation_loan_rate / 12) ** (-renovation_loan_years * 12))
        annual_renovation_payment = renovation_costs * renovation_loan_rate / (1 - (1 + renovation_loan_rate) ** (-renovation_loan_years))
        
        st.write(f"Monthly Renovation Loan: ${monthly_renovation_payment:,.0f}")
        st.write(f"Annual Renovation Loan: ${annual_renovation_payment:,.0f}")
    
st.divider()
col1, col2 = st.columns([3, 4])
with col1:
    st.subheader("Airbnb")
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        nightly_rate = st.number_input("Nightly Rate ($)", value=default_values.nightly_rate, step=10)

    with s_col2:
        occupancy_rate = st.number_input("Occupancy Rate", value=default_values.occupancy_rate)
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
total_annual_expenses = (
    annual_mortgage_payment +
    annual_renovation_payment +
    annual_tax +
    electricity_cost * 12 +
    water_cost * 12 +
    gas_cost * 12 +
    garbage_collection_cost * 12 +
    insurance_cost * 12 +
    hoa_fee * 12 +
    annual_airbnb_fee +
    annual_management_fee
)
total_monthly_expenses = total_annual_expenses / 12

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


def calculate_annual_profit(rate, occupancy_fraction):
    annual_revenue = rate * occupancy_fraction * 365

    annual_fixed_expenses = (
        annual_mortgage_payment +
        annual_renovation_payment +
        annual_tax +
        electricity_cost * 12 +
        water_cost * 12 +
        gas_cost * 12 +
        garbage_collection_cost * 12 +
        insurance_cost * 12 +
        hoa_fee * 12
    )

    all_expenses = annual_airbnb_fee + annual_management_fee + annual_fixed_expenses
    
    profit = (annual_revenue - all_expenses)
    
    return profit


# Net profit
net_annual_profit = calculate_annual_profit(nightly_rate, occupancy_rate)
net_monthly_profit = net_annual_profit / 12

with col2:

    # ==============================
    # BUILD A CONTOUR PLOT OF PROFIT AS A FUNCTION OF NIGHTLY RATE AND OCCUPANCY
    # ==============================

    rate_range = np.linspace(nightly_rate * 0.5, nightly_rate * 1.5, 80)
    occupancy_range = np.linspace(0.10, 0.95, 80)
    R, O = np.meshgrid(rate_range, occupancy_range)
    profit_surface = calculate_annual_profit(R, O)

    # PLOTTING
    fig = go.Figure()

    # Profit contours
    fig.add_trace(
        go.Contour(
            x=rate_range,
            y=occupancy_range * 100,  # show as %
            z=profit_surface,
            colorscale="RdYlGn",
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12)
            ),
            hovertemplate=
                "Nightly Rate: $%{x:.0f}<br>" +
                "Occupancy: %{y:.1f}%<br>" +
                "Annual Profit: $%{z:,.0f}<extra></extra>"
        )
    )

    # Break-even line (Profit = 0)
    fig.add_trace(
        go.Contour(
            x=rate_range,
            y=occupancy_range * 100,
            z=profit_surface,
            contours=dict(
                start=0,
                end=0,
                size=1,
                coloring='lines'
            ),
            line=dict(width=3),
            showscale=False
        )
    )

    # Current position marker
    marker_color = "blue" if net_annual_profit >= 0 else "red"
    fig.add_trace(
        go.Scatter(
            x=[nightly_rate],
            y=[occupancy_rate * 100],
            mode="markers+text",
            text=[f"You are here\n${net_annual_profit:,.0f}/yr"],
            # text color based on profit
            textfont=dict(color=marker_color),
            textposition="top center",
            marker=dict(size=12, color=marker_color),
            hovertemplate=
                "Nightly Rate: $%{x:.0f}<br>" +
                "Occupancy: %{y:.1f}%<br>" +
                f"Annual Profit: ${net_annual_profit:,.0f}<extra></extra>"
        )
    )

    # Layout
    fig.update_layout(
        xaxis_title="Nightly Rate ($)",
        yaxis_title="Occupancy (%)",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    st.plotly_chart(fig, width='stretch')



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

# ==========================================================
# TRUE BREAK-EVEN CURVES (ANALYTICAL)
# ==========================================================

st.divider()
st.subheader("Break-Even Curves by Home Price")

import numpy as np
import plotly.graph_objects as go

home_prices = [150000, 200000, 250000, 300000, 350000, 400000, 450000, 475000, 500000, 550000]

rate_range = np.linspace(nightly_rate * 0.5,
                         nightly_rate * 1.5,
                         300)

fig = go.Figure()

for price in home_prices:

    # --- Mortgage calculation ---
    loan_amount = price - downpayment
    monthly_rate = mortgage_rate / 12
    n_payments = mortgage_term_years * 12

    monthly_payment = (
        loan_amount *
        (monthly_rate * (1 + monthly_rate)**n_payments) /
        ((1 + monthly_rate)**n_payments - 1)
    )

    annual_mortgage_payment = monthly_payment * 12

    # --- Fixed expenses ---
    annual_fixed_expenses = (
        annual_mortgage_payment +
        annual_renovation_payment +
        annual_tax +
        electricity_cost * 12 +
        water_cost * 12 +
        gas_cost * 12 +
        garbage_collection_cost * 12 +
        insurance_cost * 12 +
        hoa_fee * 12
    )

    # --- Break-even occupancy formula ---
    effective_revenue_multiplier = 365 * rate_range * (
        1 - airbnb_fee_rate - management_fee_rate
    )

    break_even_occupancy = annual_fixed_expenses / effective_revenue_multiplier

    # Convert to %
    break_even_occupancy_percent = break_even_occupancy * 100

    fig.add_trace(
        go.Scatter(
            x=rate_range,
            y=break_even_occupancy_percent,
            mode="lines",
            name=f"${price:,.0f}",
            hovertemplate=
                f"Home Price: ${price:,.0f}<br>" +
                "Nightly Rate: $%{x:.0f}<br>" +
                "Break-Even Occupancy: %{y:.1f}%<extra></extra>"
        )
    )

# --- Add current strategy marker ---
fig.add_trace(
    go.Scatter(
        x=[nightly_rate],
        y=[occupancy_rate * 100],
        mode="markers+text",
        text=["Current Strategy"],
        textposition="top center",
        showlegend=False
    )
)

fig.update_layout(
    xaxis_title="Nightly Rate ($)",
    yaxis_title="Break-Even Occupancy (%)",
    height=750,
    legend_title="Home Price",
)

st.plotly_chart(fig, use_container_width=True)


# add copyright notice at the bottom "© 2026 Anton B. All rights reserved."
st.markdown("""<div style="text-align: center; margin-top: 20px;">
    <p style="font-size: 12px; color: #888;">© 2026 Anton Bakulin. All rights reserved.</p>
</div>""", unsafe_allow_html=True)