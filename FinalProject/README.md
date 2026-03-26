# Spatial Transcriptomics: Mouse Brain Atlas — Age & Inflammation Analysis

## 🔬 Project Overview
This project analyzes spatial transcriptomics data from a mouse brain 
atlas to investigate age-related and inflammation-induced transcriptomic 
changes using MERFISH data.

Based on: [Cell — Mouse Brain Spatial Atlas](https://www.sciencedirect.com/article/pii/S0092867422015239)

---

## 🛠 Analytical Workflow

### 1. Data Preprocessing & Cell-Type Mapping
- Identified individual slides using `adata_c.obs['donor']` 
  across two h5ad datasets
- Generated per-sample Cell-type Maps for spatial visualization

### 2. Leiden Clustering & Anatomical Validation
- Performed Leiden clustering and evaluated spatial alignment 
  with known brain anatomical structures (e.g., Cortex layers)
- Assessed concordance between Leiden clusters and ground truth 
  `obs['cell_type']` annotations; analyzed discordant clusters

### 3. Age-Stratified Spatial Analysis
- Compared young vs aged mouse brain using `obs['age']` metadata
- Quantified spatial distribution and cluster proportion changes 
  of specific cell types (e.g., Microglia) between age groups

### 4. Cross-Condition Gene Expression Comparison
- Identified commonly dysregulated genes between naturally aged 
  and LPS-induced acute inflammation samples
- Visualized shared gene expression patterns on Cell-type Maps

---

## 💻 Tech Stack
* **Spatial Analysis:** Scanpy, Squidpy
* **Visualization:** Matplotlib, Seaborn

---

> Developed as Bioinformatics Final Project  
> Pusan National University, Data Science, 2025
