"""
lab_9_streamlit.py
--------------------
Lab 9: Statistical Analysis + NumPy Operations on a Domain Dataset
Domain: DevTrack Pro — Project Analytics

Covers: Computation with NumPy, Aggregations, Computation on Arrays,
Comparisons/Masks/Boolean Arrays, Fancy Indexing, Sorting Arrays,
and Data Visualization (5 different plot types).
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="DevTrack Pro | NumPy Analytics", page_icon="📈", layout="wide")

CSV_PATH = os.path.join(os.path.dirname(__file__), "devtrack_analytics.csv")

PALETTE = ["#7C5DF5", "#4ADE80", "#38BDF8", "#F472B6", "#FBBF24", "#FB923C", "#A78BFA"]


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)
    ax.tick_params(axis="both", labelsize=10)


df = load_data()

# NumPy arrays pulled straight from the DataFrame columns
names = df["ProjectName"].to_numpy()
categories = df["Category"].to_numpy()
hours = df["HoursLogged"].to_numpy()
revenue = df["Revenue"].to_numpy()
rate = df["HourlyRate"].to_numpy()
bugs = df["BugsFixed"].to_numpy()
rating = df["ClientRating"].to_numpy()
completion = df["CompletionPercent"].to_numpy()

st.title("📈 DevTrack Pro — Project Analytics (NumPy)")

tabs = st.tabs([
    "📋 Dataset",
    "➕ Computation & Aggregations",
    "🎭 Masks & Boolean Arrays",
    "🎯 Fancy Indexing & Sorting",
    "📊 Visualizations",
])

# =================================================================
# TAB 1: DATASET
# =================================================================
with tabs[0]:
    st.header("Project Dataset")
    st.dataframe(df, use_container_width=True)
    st.metric("Total Projects", len(df))

# =================================================================
# TAB 2: COMPUTATION WITH NUMPY + AGGREGATIONS
# =================================================================
with tabs[1]:
    st.header("Computation with NumPy")

    revenue_per_hour = np.where(hours > 0, revenue / hours, 0)
    bonus = revenue * 0.10
    revenue_after_tax = revenue * 0.82  # broadcasting: array * scalar

    comp_df = pd.DataFrame({
        "ProjectName": names,
        "Revenue": revenue,
        "Revenue/Hour": np.round(revenue_per_hour, 2),
        "Bonus (10%)": np.round(bonus, 2),
        "Revenue After Tax (82%)": np.round(revenue_after_tax, 2),
    })
    st.dataframe(comp_df, use_container_width=True)
    st.caption("Revenue/Hour computed element-wise; Bonus and Tax columns computed using NumPy broadcasting (array × scalar).")

    st.divider()
    st.header("Aggregations")

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Total Revenue", f"${np.sum(revenue):,.0f}")
    a2.metric("Mean Hours Logged", f"{np.mean(hours):.1f}")
    a3.metric("Median Client Rating", f"{np.median(rating):.2f}")
    a4.metric("Std. Dev. of Revenue", f"${np.std(revenue):,.0f}")

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Min Revenue", f"${np.min(revenue):,.0f}")
    b2.metric("Max Revenue", f"${np.max(revenue):,.0f}")
    b3.metric("Total Bugs Fixed", int(np.sum(bugs)))
    b4.metric("Mean Completion %", f"{np.mean(completion):.1f}%")

# =================================================================
# TAB 3: COMPARISONS, MASKS, AND BOOLEAN ARRAYS
# =================================================================
with tabs[2]:
    st.header("Comparisons, Masks & Boolean Arrays")

    high_revenue_mask = revenue > np.mean(revenue)
    st.subheader(f"Projects earning above average revenue (> ${np.mean(revenue):,.0f})")
    st.dataframe(df[high_revenue_mask], use_container_width=True)
    st.caption(f"Boolean mask: `revenue > revenue.mean()` → {np.sum(high_revenue_mask)} of {len(df)} projects match.")

    st.divider()

    top_rated_mask = rating >= 4.5
    st.subheader("Top-rated projects (Client Rating ≥ 4.5)")
    st.dataframe(df[top_rated_mask], use_container_width=True)

    st.divider()

    combined_mask = (hours > 50) & (rating >= 4.0)
    st.subheader("High-effort AND well-rated projects (Hours > 50 AND Rating ≥ 4.0)")
    st.dataframe(df[combined_mask], use_container_width=True)
    st.caption("Combined boolean mask using `&` to demonstrate compound conditions on NumPy arrays.")

# =================================================================
# TAB 4: FANCY INDEXING & SORTING
# =================================================================
with tabs[3]:
    st.header("Sorting Arrays")

    sorted_revenue = np.sort(revenue)[::-1]
    st.write("Revenue values sorted in descending order:")
    st.code(sorted_revenue.tolist())

    st.divider()
    st.header("Fancy Indexing")

    top_n = st.slider("Select how many top projects to view (by Revenue)", min_value=3, max_value=10, value=5)

    top_indices = np.argsort(revenue)[::-1][:top_n]   # indices of highest revenue
    top_names = names[top_indices]                    # fancy indexing
    top_revenue = revenue[top_indices]                # fancy indexing
    top_ratings = rating[top_indices]                 # fancy indexing

    fancy_df = pd.DataFrame({
        "ProjectName": top_names,
        "Revenue": top_revenue,
        "ClientRating": top_ratings
    })
    st.dataframe(fancy_df, use_container_width=True)
    st.caption("`np.argsort(revenue)[::-1][:n]` gets the index positions of the top-N revenue values, then those indices are used to fancy-index into the Names, Revenue, and Rating arrays simultaneously.")

    st.divider()
    st.subheader("Explicit Fancy Indexing Example")
    custom_indices = np.array([0, 3, 7, 11])
    st.write("Selecting specific projects at index positions `[0, 3, 7, 11]`:")
    st.dataframe(pd.DataFrame({
        "ProjectName": names[custom_indices],
        "Category": categories[custom_indices],
        "Revenue": revenue[custom_indices]
    }), use_container_width=True)

# =================================================================
# TAB 5: DATA VISUALIZATION — 5 DIFFERENT PLOT TYPES
# =================================================================
with tabs[4]:
    st.header("Data Visualization")

    plot_choice = st.radio(
        "Choose a visualization",
        [
            "Bar Chart — Total Revenue by Category",
            "Histogram — Client Rating Distribution",
            "Scatter Plot — Hours vs Revenue",
            "Box Plot — Revenue Spread by Category",
            "Pie Chart — Project Share by Category",
        ]
    )

    if plot_choice == "Bar Chart — Total Revenue by Category":
        cat_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(cat_revenue.index, cat_revenue.values,
                       color=PALETTE[:len(cat_revenue)], edgecolor="white", linewidth=1.5, width=0.55, zorder=3)
        for bar, val in zip(bars, cat_revenue.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, f"${val:,.0f}",
                     ha="center", va="bottom", fontsize=11, fontweight="bold")
        ax.set_title("Total Revenue by Category", fontsize=16, fontweight="bold", pad=15)
        ax.set_ylabel("Revenue ($)")
        style_axes(ax)
        st.pyplot(fig)

    elif plot_choice == "Histogram — Client Rating Distribution":
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(rating, bins=8, color="#7C5DF5", edgecolor="white", linewidth=1.2, zorder=3)
        ax.set_title("Distribution of Client Ratings", fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("Client Rating")
        ax.set_ylabel("Number of Projects")
        style_axes(ax)
        st.pyplot(fig)

    elif plot_choice == "Scatter Plot — Hours vs Revenue":
        fig, ax = plt.subplots(figsize=(8, 5.5))
        unique_cats = df["Category"].unique()
        color_map = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(unique_cats)}
        for cat in unique_cats:
            subset = df[df["Category"] == cat]
            ax.scatter(subset["HoursLogged"], subset["Revenue"], s=130, color=color_map[cat],
                       edgecolor="white", linewidth=1.2, label=cat, zorder=3)
        ax.set_title("Hours Logged vs Revenue", fontsize=16, fontweight="bold", pad=15)
        ax.set_xlabel("Hours Logged")
        ax.set_ylabel("Revenue ($)")
        ax.legend(title="Category", frameon=False, fontsize=9)
        style_axes(ax)
        st.pyplot(fig)

    elif plot_choice == "Box Plot — Revenue Spread by Category":
        fig, ax = plt.subplots(figsize=(8, 5.5))
        cats_ordered = df["Category"].unique()
        data_by_cat = [df[df["Category"] == c]["Revenue"].values for c in cats_ordered]
        bp = ax.boxplot(data_by_cat, labels=cats_ordered, patch_artist=True, widths=0.5)
        for patch, color in zip(bp["boxes"], PALETTE):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax.set_title("Revenue Spread by Category", fontsize=16, fontweight="bold", pad=15)
        ax.set_ylabel("Revenue ($)")
        style_axes(ax)
        st.pyplot(fig)

    elif plot_choice == "Pie Chart — Project Share by Category":
        cat_counts = df["Category"].value_counts()
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        wedges, texts, autotexts = ax.pie(
            cat_counts.values, labels=cat_counts.index, autopct="%1.0f%%", startangle=90,
            colors=PALETTE[:len(cat_counts)], wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 12, "fontweight": "bold"}
        )
        for at in autotexts:
            at.set_color("white")
        ax.set_title("Project Share by Category", fontsize=16, fontweight="bold", pad=15)
        ax.axis("equal")
        st.pyplot(fig)