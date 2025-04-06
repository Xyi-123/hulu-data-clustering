# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 20:03:57 2025

@author: Lenovo
"""

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from pyecharts.charts import Scatter
from pyecharts import options as opts

# 1. data import
data = pd.read_excel(r"D:\\桌面\\BA\\聚类作业\\hulu-Movies(raw data).xlsx")
print("Dataset Size：", data.shape)
print(data.head())

# 2. Feature Engineering
# Extract duration values
def extract_duration(duration_str):
    if pd.isnull(duration_str):
        return np.nan
    if "min" in duration_str:
        match = re.search(r'(\d+)', duration_str)
        if match:
            return int(match.group(1))
    elif "Season" in duration_str:
        match = re.search(r'(\d+)', duration_str)
        if match:
            return int(match.group(1))
    return np.nan

data['duration_num'] = data['duration'].apply(extract_duration)

rating_mapping = {
    'G': 1,
    'PG': 2,
    'PG-13': 3,
    'R': 4,
    'TV-MA': 5
}
data['rating_num'] = data['rating'].map(rating_mapping)
data['rating_num'] = data['rating_num'].fillna(0)
data['release_year'] = pd.to_numeric(data['release_year'], errors='coerce')
data['genre_count'] = data['listed_in'].apply(lambda x: len(x.split(',')) if pd.notnull(x) else 0)

# Select features for clustering
features = ['duration_num','rating_num', 'release_year', 'genre_count']
data_clean = data.dropna(subset=features)
print("Cleaned Dataset Size：", data_clean.shape)

X = data_clean[features].values

# 3. Standard
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. K-Means Clustering
# setting k=3
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
data_clean['cluster'] = clusters

print("Cluster Sample Counts：")
print(data_clean['cluster'].value_counts())

# 5. Visualization
data_clean = data_clean.reset_index(drop=True)
x_data = data_clean['release_year'].tolist()

# Create Scatter
scatter = (
    Scatter(init_opts=opts.InitOpts(width="800px", height="600px"))
    .add_xaxis(xaxis_data=x_data)
)

color_list = ["#EE6666", "#73C0DE","#91CC75"]

unique_clusters = sorted(data_clean['cluster'].unique())
for i, c_id in enumerate(unique_clusters):
    y_array = []
    for idx, row in data_clean.iterrows():
        if row['cluster'] == c_id:
            y_array.append(row['duration_num'])
        else:
            y_array.append(None)

    scatter.add_yaxis(
        series_name=f"Cluster {c_id}",
        y_axis=y_array,
        symbol_size=8,
        label_opts=opts.LabelOpts(is_show=False),
        color=color_list[i % len(color_list)]
    )

# setting
scatter.set_global_opts(
    # 1) 
    title_opts=opts.TitleOpts(
        title="Clusters of Hulu Movies: Release Year vs. Duration",
        pos_left="center", 
        pos_top="0%"   
    ),
    # 2)
    legend_opts=opts.LegendOpts(
        pos_left="90%", 
        pos_top="30%", 
        orient="vertical"
    ),
    # 3) X
    xaxis_opts=opts.AxisOpts(
        name="Release Year",
        name_gap=5,       
        type_="value",
        min_=data_clean['release_year'].min() - 5,
        max_=data_clean['release_year'].max() + 5,
        interval=10,
        splitline_opts=opts.SplitLineOpts(is_show=True),
        axislabel_opts=opts.LabelOpts(rotate=0)
    ),
    # 4) Y
    yaxis_opts=opts.AxisOpts(
        name="Duration (Min)",
        name_gap=10,  
        type_="value",
        min_=0,
        splitline_opts=opts.SplitLineOpts(is_show=True),
        axislabel_opts=opts.LabelOpts(rotate=0)
    )
)
scatter.render("Hulu-Movies.html")