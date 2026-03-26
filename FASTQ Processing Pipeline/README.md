# NGS Data Processing Pipeline

A Python-based automated pipeline for Next-Generation Sequencing (NGS) 
data preprocessing and alignment, integrating FastQC, CutAdapt, BWA-MEM2, 
and SAMtools for end-to-end FASTQ processing.

> Developed as part of Bioinformatics coursework at Pusan National University.  
> Also includes implementations of core sequence analysis algorithms 
> (edit distance, k-mer generation, FM-index).

---

## 📌 Pipeline Overview

```
FASTQ files
    │
    ▼
[1] FastQC          → Quality control report
    │
    ▼
[2] CutAdapt        → Illumina universal adapter trimming
    │
    ▼
[3] BWA-MEM2        → Alignment to reference genome
    │
    ▼
[4] SAMtools markdup → Duplicate marking
    │
    ▼
[5] SAMtools index   → BAI indexing
```

---

## 🚀 Usage

```bash
python ngs_pipeline.py <fastq_directory> <reference_genome>
```

**Arguments**
| Argument | Description |
|---|---|
| `fastq_directory` | Path to the directory containing `.fastq` / `.fastq.gz` files |
| `reference_genome` | Path to the BWA-MEM2 indexed reference genome |

**Example**
```bash
python ngs_pipeline.py ./data/ ./ref/hg38.fa
```

---

## 🛠️ Tools & Dependencies

External tools must be installed and available in `$PATH`:

| Tool | Version | Purpose |
|---|---|---|
| FastQC | ≥ 0.11 | Per-base quality control |
| CutAdapt | ≥ 4.0 | Illumina universal adapter trimming |
| BWA-MEM2 | ≥ 2.0 | Read alignment to reference genome |
| SAMtools | ≥ 1.15 | Duplicate marking and BAI indexing |

---

## 📁 Output Structure

```
fastq_directory/
├── fastqc_results/         # FastQC HTML & zip reports
├── trimmed/                # Adapter-trimmed FASTQ files
└── aligned/
    ├── sample.bam          # Aligned BAM
    ├── sample.markdup.bam  # Duplicate-marked BAM
    └── sample.markdup.bai  # BAI index
```

---

## ⚙️ Pipeline Details

### 1. FastQC
Generates per-sample quality control reports to assess base quality, GC content, and sequence duplication levels.

### 2. CutAdapt — Adapter Trimming
Removes **Illumina universal adapters** (`AGATCGGAAGAGC`) from raw reads. Reads shorter than 20bp after trimming are discarded.

### 3. BWA-MEM2 — Alignment
Aligns trimmed reads to the reference genome using `bwa-mem2 mem`. Output is converted to sorted BAM via SAMtools.

### 4. Duplicate Marking
Marks PCR duplicates using `samtools markdup` to reduce bias in downstream variant calling or quantification.

### 5. BAI Indexing
Generates a `.bai` index file for each final BAM using `samtools index`, enabling random access by genomic coordinate.

---

> ⚠️ **Note:** Raw FASTQ files and BWA index files are not included in this repository due to file size. The pipeline code (`ngs_pipeline.py`) is provided for reference.
