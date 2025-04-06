# hulu-data-clustering

This project applies clustering analysis to Hulu's movie content based on metadata such as **release year**, **duration**, **rating**, and **genre diversity**. The goal is to identify content patterns that can inform personalization, content curation, and user recommendations.

---

## Project Overview

- ✅ Performed KMeans clustering on cleaned metadata
- ✅ Identified 3 distinct content groups:
  - **Cluster 0:** Diverse, mid-length modern content
  - **Cluster 1:** Hulu’s standard, recent, algorithm-friendly core
  - **Cluster 2:** Classic or long-form historical/documentary content
- ✅ Generated an **interactive scatter plot** showing clusters by Release Year vs Duration

---

## Interactive Visualization

👉 [**Click here to view the interactive HTML chart**](https://xyi-123.github.io/hulu-data-clustering/Hulu-Movies.html)

*(Built using [Pyecharts](https://github.com/pyecharts/pyecharts) and hosted with GitHub Pages)*

---

## Technologies

- `pandas`, `numpy`, `re` – data wrangling
- `scikit-learn` – clustering (KMeans)
- `pyecharts` – interactive visualization
- `matplotlib` – exploratory plotting

---

## 📁 Files in This Repo

- `Hulu-Movies.py` – Python code for clustering and chart generation
- `Hulu-Movies.html` – Interactive result (hosted online)
- `hulu-Movies(raw data).xlsx` – Raw dataset (optional/private)
- `README.md` – You’re reading it!
