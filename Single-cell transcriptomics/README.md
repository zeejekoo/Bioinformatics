# High-Resolution Single-Cell Transcriptomics: Mouse Brain Analysis
This project implements an end-to-end pipeline for single-cell RNA-seq (scRNA-seq) analysis, focusing on uncovering granular cellular diversity in brain tissue. Using the Scanpy ecosystem, I processed raw expression data into a biologically interpretable map, identifying distinct cell populations through high-resolution clustering.
## 🎯 Project Objectives
- Standardized Preprocessing: Establish a robust QC and normalization workflow to mitigate technical noise.

- Granular Feature Extraction: Identify Highly Variable Genes (HVGs) to focus on biological signals.

- High-Resolution Manifold Learning: Utilize Leiden clustering (Resolution 1.5) to distinguish subtle transcriptomic differences between closely related neural cell types.

- Marker Discovery: Statistically determine cluster-specific biomarkers for cell-type annotation.

##  🛠 Technical Implementation
### 1. Quality Control & Refinement
- Thresholding: Filtered out low-quality cells (<200 genes) and rare genes (<3 cells) to ensure data integrity.

- Mitochondrial Filtering: Assessed cellular stress levels using pct_counts_mt to remove apoptotic cells.

- Regression: Systematically regressed out effects of total counts and mitochondrial percentage to prevent technical bias in downstream clustering.

### 2. Normalization & Feature Selection
- Log-Normalization: Scaled counts to 10k per cell followed by log1p transformation to stabilize variance.

- Feature Selection: Prioritized top variable genes, providing the basis for PCA-driven dimensionality reduction.

### 3. Dimensionality Reduction & Clustering
- PCA & Graph Construction: Reduced dimensionality to 40 PCs and constructed a neighborhood graph (k=10).

- UMAP Visualization: Embedded high-dimensional clusters into 2D space for intuitive exploration.

- Leiden Clustering: Selected a high resolution of 1.5 to capture granular sub-clusters that lower resolutions might overlook.

### 4. Differential Expression (DEG)
- Statistical Ranking: Employed the t-test method within rank_genes_groups to identify the most significant markers for each population.

- Visualization: Generated comprehensive Dot Plots to evaluate the specificity and sensitivity of the top 5 markers per cluster.
### 5. Cell-Type Annotation
- **CellTypist**: Applied pre-trained CellTypist models for automated 
cell-type annotation, enabling biologically interpretable cluster labeling 
beyond manual marker-based approaches.
- Cross-validated annotations against cluster-specific DEGs to ensure 
biological consistency.


### 6. 📈 Key Visualizations
- QC Metrics: Pre- and post-filtering violin plots.

- UMAP Projection: Cellular landscape colored by high-resolution Leiden clusters.

- Marker Heatmap/Dot Plot: Expression profiles of the top-ranked genes.
