# Supplementary information

## Full-set training examples change adaptation rankings in matched tool retrieval

### Supplementary Table S1. Additional retrieval endpoints

All rates are percentages. Each exposure-aligned rate averages the same 128 requests over the 16 assignment/background pairs. Differences are percentage points. Fixed controls use one unchanged ranking per request.

COMP@k is one when all reference tools appear in the first k ranks and zero otherwise. Recall@10 is the fraction of reference tools retrieved among the first ten ranks. NDCG@10 uses binary relevance with discount 1/log2(r + 1) at rank r, divided by the ideal discounted sum for min(10, number of reference tools). Requests receive equal weight.

| Method | Endpoint | Full-set example present | Absent | Difference |
|---|---|---:|---:|---:|
| Frozen encoder | COMP@5 | 47.6562 | 47.6562 | 0.0000 |
| BM25 | COMP@5 | 14.0625 | 14.0625 | 0.0000 |
| 1NN | COMP@5 | 81.6406 | 54.6875 | 26.9531 |
| Linear query adapter | COMP@5 | 82.5684 | 67.1387 | 15.4297 |
| COLT-stage adaptation | COMP@5 | 92.4805 | 61.3770 | 31.1035 |
| Frozen encoder | COMP@10 | 67.1875 | 67.1875 | 0.0000 |
| BM25 | COMP@10 | 22.6562 | 22.6562 | 0.0000 |
| 1NN | COMP@10 | 86.3281 | 73.4375 | 12.8906 |
| Linear query adapter | COMP@10 | 91.7480 | 83.0566 | 8.6914 |
| COLT-stage adaptation | COMP@10 | 96.3867 | 79.2480 | 17.1387 |
| Frozen encoder | COMP@20 | 83.5938 | 83.5938 | 0.0000 |
| BM25 | COMP@20 | 32.8125 | 32.8125 | 0.0000 |
| 1NN | COMP@20 | 93.7500 | 86.3281 | 7.4219 |
| Linear query adapter | COMP@20 | 95.7031 | 91.4551 | 4.2480 |
| COLT-stage adaptation | COMP@20 | 98.4375 | 87.5977 | 10.8398 |
| Frozen encoder | NDCG@10 | 71.4214 | 71.4214 | 0.0000 |
| BM25 | NDCG@10 | 40.4915 | 40.4915 | 0.0000 |
| 1NN | NDCG@10 | 86.3981 | 66.1054 | 20.2927 |
| Linear query adapter | NDCG@10 | 89.0235 | 78.8642 | 10.1592 |
| COLT-stage adaptation | NDCG@10 | 92.7594 | 74.8594 | 17.9000 |
| Frozen encoder | Recall@10 | 81.6406 | 81.6406 | 0.0000 |
| BM25 | Recall@10 | 48.4375 | 48.4375 | 0.0000 |
| 1NN | Recall@10 | 91.9922 | 84.7656 | 7.2266 |
| Linear query adapter | Recall@10 | 94.9707 | 90.1123 | 4.8584 |
| COLT-stage adaptation | Recall@10 | 97.7783 | 88.8184 | 8.9600 |

### Supplementary Table S2. All eight allocation results

Each row averages the two crossed backgrounds. Exposure effects are present-minus-absent COMP@10 differences. Graph-minus-linear comparisons are secondary analyses of the predeclared absolute-performance outputs. These rows describe allocation sensitivity under optimizer seed 17 on one inspected population; they are not independent test populations.

| Assignment seed | Linear exposure effect | COLT-stage exposure effect | 1NN exposure effect | Graph minus linear, present | Graph minus linear, absent |
|---|---:|---:|---:|---:|---:|
| 101 | 8.9844 | 17.1875 | 12.8906 | 4.2969 | -3.9062 |
| 211 | 9.7656 | 17.1875 | 12.8906 | 4.6875 | -2.7344 |
| 307 | 8.2031 | 17.9688 | 12.8906 | 4.6875 | -5.0781 |
| 401 | 8.9844 | 17.5781 | 12.8906 | 4.2969 | -4.2969 |
| 503 | 8.9844 | 16.4062 | 12.8906 | 5.0781 | -2.3438 |
| 601 | 8.5938 | 16.4062 | 12.8906 | 4.6875 | -3.1250 |
| 701 | 8.2031 | 16.4062 | 12.8906 | 4.2969 | -3.9062 |
| 809 | 7.8125 | 17.9688 | 12.8906 | 5.0781 | -5.0781 |

### Supplementary Table S3. Exposure effects by shared background

Values are COMP@10 percentage points, averaged over the eight assignments. Backgrounds 71 and 97 contain larger reference sets including 25 and 32 of the 128 evaluated tool pairs, respectively. Those background examples are identical within each paired comparison.

| Background seed | Linear | COLT-stage | 1NN |
|---|---:|---:|---:|
| 71 | 8.0078 | 14.8438 | 10.1562 |
| 97 | 9.3750 | 19.4336 | 15.6250 |

### S4. Interpretation of the exposure label

The exposure label is computed from evaluation reference sets for offline scoring and analysis. At inference, each retriever receives the request without its reference set. The preference reversal characterizes conditional evaluation of the two recorded recipes; deployment-time selection between them was not evaluated.

### S5. Reproducibility scope and retained materials

The retained workspace contains cohort-construction code, selected source IDs and references, frozen embedding arrays, fitted states, full catalogue scores and rankings, and the original metrics. The source benchmark is COLT ToolBenchG3 at commit `bbec292c38cabe3fbae098f50cc31b2e9f7e8fca`; the encoder is `Lux1997/Tool-Embed-0.6B` at revision `103d16d3593dec6c6f2217be620febb846932f6a`. The main manuscript links to the public files for replaying the main tables and checking the plotted data.

The recorded comparison used Python 3.13.9, NumPy 2.3.5 and PyTorch 2.12.1, with four CPU threads for adaptation. Encoding used the Metal Performance Shaders (MPS) backend; no encoder parameters were trained. The comparison completed 64 fits and 12,800 optimizer updates. Independent NumPy replay checked stored-state inference and reported metrics, not optimizer trajectories or a fresh environment installation.

From the workspace root, `python -B research/tool-actions/projects/TOOL-COMBINATION-EVAL/manuscript/build_supplement.py` regenerates the original EXP003/004 supplement without fitting a model. Section S10 reports the later post hoc analysis. Numerical replay uses `audit_formal_result.py --run <retained EXP003 run directory> --output <new audit JSON path>` with NumPy available. The audit rejects an existing output path. Code and vectors needed by its retained relative paths must be present; it is not a standalone public release.

The original COLT source copies have no licence file in the inspected tree. They are retained as local audit sources. Redistribution permission for upstream code and data must be established separately from citation and numerical reproducibility.

### Supplementary Table S4. Identities of the source records

Paths are relative to the research project. Hashes identify the actual records used to generate this supplement.

| Record | SHA-256 |
|---|---|
| `experiments/EXP-TOOL-COMBINATION-EVAL-003/runs/2026-10-31--run-001/metrics.json` | `488c99afaf285545178b57ff7c5bfdc074417adf83a8a0fd3ecf64957d1411f9` |
| `experiments/EXP-TOOL-COMBINATION-EVAL-003/runs/2026-10-31--run-001/receipt.json` | `2c6ac6e4302b65b84f033d56b7299c93754a5a99e5734f28f76745c1646869a2` |
| `reviews/secondary-method-comparison--2026-10-31--v01.json` | `8630bc2dc83339a08d66be24f4ef70b729ab62b073a329f69ab899544270da79` |
| `design/formal-pairs--2026-10-31--v01.json` | `aebccf8b6748e792b75fafdff81ca973e12ba5b28e5d5b10d82336e26d73fbd3` |
| `experiments/EXP-TOOL-COMBINATION-EVAL-003/protocol.json` | `94d7839b64ff4a13caa80bf552e03fa9c9946b593f754fe1908d5111ac6ac17a` |

### S6. Confirmation retrieval endpoints

**Supplementary Table S5. Five retrieval endpoints for the history-excluded confirmation subset.** Rates are percentages, averaged over the same 84 requests and eight assignment/background pairs. Each request is evaluated in both exposure conditions; differences are percentage points. These are EXP004 results and are kept separate from the EXP003 results in Tables S1–S3.

| Method | Endpoint | Full-set example present | Absent | Difference |
|---|---|---:|---:|---:|
| Frozen encoder | COMP@5 | 52.3810 | 52.3810 | 0.0000 |
| BM25 | COMP@5 | 17.8571 | 17.8571 | 0.0000 |
| 1NN | COMP@5 | 84.6726 | 54.4643 | 30.2083 |
| Linear query adapter | COMP@5 | 84.5238 | 64.7321 | 19.7917 |
| COLT-stage adaptation | COMP@5 | 94.4940 | 61.4583 | 33.0357 |
| Frozen encoder | COMP@10 | 75.0000 | 75.0000 | 0.0000 |
| BM25 | COMP@10 | 27.3810 | 27.3810 | 0.0000 |
| 1NN | COMP@10 | 91.0714 | 76.7857 | 14.2857 |
| Linear query adapter | COMP@10 | 91.0714 | 80.8036 | 10.2679 |
| COLT-stage adaptation | COMP@10 | 96.4286 | 78.2738 | 18.1548 |
| Frozen encoder | COMP@20 | 85.7143 | 85.7143 | 0.0000 |
| BM25 | COMP@20 | 33.3333 | 33.3333 | 0.0000 |
| 1NN | COMP@20 | 95.2381 | 88.6905 | 6.5476 |
| Linear query adapter | COMP@20 | 95.6845 | 91.0714 | 4.6131 |
| COLT-stage adaptation | COMP@20 | 97.7679 | 88.2440 | 9.5238 |
| Frozen encoder | NDCG@10 | 75.8609 | 75.8609 | 0.0000 |
| BM25 | NDCG@10 | 45.7316 | 45.7316 | 0.0000 |
| 1NN | NDCG@10 | 88.1807 | 66.3159 | 21.8648 |
| Linear query adapter | NDCG@10 | 88.5995 | 78.5813 | 10.0182 |
| COLT-stage adaptation | NDCG@10 | 93.6851 | 74.7027 | 18.9824 |
| Frozen encoder | Recall@10 | 86.3095 | 86.3095 | 0.0000 |
| BM25 | Recall@10 | 50.5952 | 50.5952 | 0.0000 |
| 1NN | Recall@10 | 94.0476 | 86.9048 | 7.1429 |
| Linear query adapter | Recall@10 | 94.8661 | 89.8065 | 5.0595 |
| COLT-stage adaptation | Recall@10 | 97.3214 | 88.0952 | 9.2262 |

### S7. Confirmation allocation and paired-background results

**Supplementary Table S6. All four confirmation allocations.** Exposure effects are present-minus-absent COMP@10 differences. Graph-minus-linear contrasts use the same exposure-aligned requests and average both backgrounds within each allocation. All differences are percentage points.

| Assignment seed | Linear exposure effect | COLT-stage exposure effect | 1NN exposure effect | Graph minus linear, present | Graph minus linear, absent | Strict sign reversal |
|---|---:|---:|---:|---:|---:|---|
| 1103 | 10.7143 | 17.8571 | 14.2857 | 5.3571 | -1.7857 | Yes |
| 1201 | 8.9286 | 19.6429 | 14.2857 | 5.3571 | -5.3571 | Yes |
| 1301 | 11.3095 | 16.6667 | 14.2857 | 5.3571 | 0.0000 | No |
| 1409 | 10.1190 | 18.4524 | 14.2857 | 5.3571 | -2.9762 | Yes |

The prespecified aggregate contrasts were 5.3571 points with a full-set example and -2.5298 points without one; their interaction was 7.8869 points. Strict sign reversal occurred in 3/4 allocation means. Assignment 1301 had an absent-condition tie and is retained. The prespecified rule required aggregate differences of at least +2 and at most −2 points and sign reversal in at least three allocations; these are practical investment criteria, not a significance test.

**Supplementary Table S7. All eight paired-background comparisons.** These show the variation hidden by the allocation means. The primary rule applies to the allocation means, not to a requirement that every background show reversal.

| Assignment seed | Background seed | Linear exposure effect | COLT-stage exposure effect | Graph minus linear, present | Graph minus linear, absent | Strict sign reversal |
|---|---|---:|---:|---:|---:|---|
| 1103 | 151 | 10.7143 | 14.2857 | 5.9524 | 2.3810 | No |
| 1103 | 163 | 10.7143 | 21.4286 | 4.7619 | -5.9524 | Yes |
| 1201 | 151 | 7.1429 | 16.6667 | 7.1429 | -2.3810 | Yes |
| 1201 | 163 | 10.7143 | 22.6190 | 3.5714 | -8.3333 | Yes |
| 1301 | 151 | 11.9048 | 15.4762 | 5.9524 | 2.3810 | No |
| 1301 | 163 | 10.7143 | 17.8571 | 4.7619 | -2.3810 | Yes |
| 1409 | 151 | 8.3333 | 15.4762 | 7.1429 | 0.0000 | No |
| 1409 | 163 | 11.9048 | 21.4286 | 3.5714 | -5.9524 | Yes |

Strict sign reversal occurred in 5/8 individual background pairs. The four allocations and two crossed backgrounds are design-sensitivity settings on the same 84 requests, rather than independent population or optimizer-seed replications.

### S8. Confirmation sources, construction and interpretation

EXP004 uses 84 requests and 84 distinct two-tool reference sets in 21 native four-cycle blocks from the same COLT ToolBenchG3 source and the same 1,419-tool catalogue. The history exclusion covers earlier recorded ToolBenchG3 training, development and evaluation reference sets, together with MFTR history mapped exactly into the native namespace. Evaluation and anchor requests also exclude known previously used IDs and normalized texts. This establishes the recorded local-history boundary, not absence from the encoder's opaque pretraining. Thirty-eight participating tool identities overlap the earlier 128-request population.

Each new training arm contains 512 examples: 42 exchange anchors and 470 common background examples. The earlier design used 64 anchors and 448 common examples. Consequently, EXP004 is a separately constructed, history-excluded confirmation from the same source. Its training mixture differs from the earlier design, and its participating tools partly overlap the earlier population. Within every new pair, tool frequencies, reference-set cardinalities, distinct-set counts and repetition profiles remain matched. Background reuse is permitted and documented.

In backgrounds 151 and 163, 14 and 11 evaluated tool pairs occur inside larger shared reference sets, respectively. Exact full-set exemplar absence therefore does not imply absence of all pair co-occurrence. The native exemplar intervention changes reference-set coverage and language familiarity together. These data do not isolate pure symbolic composition, validate equivalent-tool substitutions, or measure API execution success.

The confirmation completed 32 fits in 178.44 seconds on 4 CPU threads, with 0 new human labels and 0 paid calls. The fixed encoder and the two recorded adaptation recipes were retained. The numerical replay report records 10,480 checks, no failures and a maximum absolute score discrepancy of 1.49e-06 under the prespecified 2e-05 tolerance. It checks stored-state inference and reported rankings, metrics and gates; it does not replay optimizer trajectories.

**Supplementary Table S8. Confirmation source identities.** Paths are relative to the research project. The public replay files are listed in the main manuscript.

| Record | SHA-256 |
|---|---|
| `experiments/EXP-TOOL-COMBINATION-EVAL-004/runs/2026-10-31--run-001/metrics.json` | `301c9106ee60cd43c5f2873743bf9efe582ce3f9392439d9a9e520f647e1cb47` |
| `experiments/EXP-TOOL-COMBINATION-EVAL-004/runs/2026-10-31--run-001/receipt.json` | `97682b81e66bde05966b20f4b29b60b66d05a2c1295ebb8f488edf7fa5ab9283` |
| `experiments/EXP-TOOL-COMBINATION-EVAL-004/protocol.json` | `359d9081b5486f2aed43ac018b53cee2beef87e5dba5a556e5a2fe0bc98c03da` |
| `design/independent-pairs--2026-10-31--v01.json` | `95a1212e7a5d08b045286316ca915512a46276b20f867be115849abc21b6785c` |
| `design/independent-data-audit--2026-10-31--v01.json` | `6535f3afa236cc059dabaf709624ebf12364bd05cd8585de137944e97ac74b55` |
| `reviews/confirmation-result-audit--2026-10-31--v01.json` | `31a964f3bac9e4a5e196c2db599de6bee7c4e676cb756df3f43774243c3094b8` |

### S9. Saved-ranking table reproduction and access boundaries

For the internal audit, the standard-library script `manuscript/reproduce_tables.py` recomputes seven request-level retrieval metrics from the retained top-twenty rankings, aligns outcomes using each allocation's exposure labels, and checks all 50 displayed values in main Tables 1 and 2. It retains all 128 initial and 84 confirmation requests in every planned cell. It also checks the confirmation's three allocation-level reversals, five paired-background reversals and prespecified continuation decision. This path does not require model weights, embeddings, fitted states, neural inference or an optimizer.

The internal audit uses each study’s protocol, cohort data, output manifest, predictions, and metrics, along with the script and main manuscript. Public replay uses the rankings CSV and Python script linked in the main manuscript. The README supplies the command and data attribution.

### S10. Post hoc sensitivity to evaluation composition

Each row removes one matched four-cycle block from evaluation, leaving the fitted models and training cohorts unchanged. Blocks are numbered in ascending order of their frozen identifiers within each study; blocks contain four evaluation requests each. The supplementary file `request-to-cycle--2026-11-07--v01.csv` provides this mapping for all 212 requests. Run `python3 replay_block_sensitivity.py <saved-rankings.csv> request-to-cycle--2026-11-07--v01.csv --output <new-result.json>` to reproduce every deletion using only the Python standard library. The saved-ranking CSV is available from the public repository cited in the main text. All retained requests are scored under both exposure conditions. Differences are graph-minus-linear COMP@10 in percentage points, averaged across all assignments and backgrounds. The practical criterion is the original confirmation rule applied descriptively to a post hoc subset; it was not a prespecified deletion-analysis criterion. The paired outputs are correlated and these are influence checks, not independent trials.

**Supplementary Table S9. Initial population**

| Block removed | Requests retained | Present | Absent | Assignment reversals | Pair reversals | Original confirmation criterion |
|---|---:|---:|---:|---:|---:|---|
| 1 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 2 | 124 | 4.7883 | -3.1250 | 8/8 | 12/16 | Not applicable |
| 3 | 124 | 4.7883 | -3.8306 | 8/8 | 13/16 | Not applicable |
| 4 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 5 | 124 | 4.7883 | -4.5867 | 8/8 | 16/16 | Not applicable |
| 6 | 124 | 5.1915 | -3.6290 | 8/8 | 12/16 | Not applicable |
| 7 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 8 | 124 | 3.9819 | -4.6875 | 8/8 | 15/16 | Not applicable |
| 9 | 124 | 4.0827 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 10 | 124 | 4.7883 | -3.4274 | 8/8 | 13/16 | Not applicable |
| 11 | 124 | 4.7883 | -3.7802 | 8/8 | 13/16 | Not applicable |
| 12 | 124 | 4.4355 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 13 | 124 | 4.3851 | -4.4355 | 8/8 | 13/16 | Not applicable |
| 14 | 124 | 4.9899 | -2.7218 | 8/8 | 12/16 | Not applicable |
| 15 | 124 | 4.7883 | -3.5786 | 8/8 | 12/16 | Not applicable |
| 16 | 124 | 4.7883 | -3.1250 | 8/8 | 13/16 | Not applicable |
| 17 | 124 | 3.6794 | -4.2843 | 8/8 | 14/16 | Not applicable |
| 18 | 124 | 3.9819 | -4.2339 | 8/8 | 16/16 | Not applicable |
| 19 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 20 | 124 | 4.4859 | -4.6875 | 8/8 | 16/16 | Not applicable |
| 21 | 124 | 4.7883 | -3.7802 | 8/8 | 13/16 | Not applicable |
| 22 | 124 | 3.9819 | -2.7218 | 8/8 | 13/16 | Not applicable |
| 23 | 124 | 4.7883 | -4.6371 | 8/8 | 13/16 | Not applicable |
| 24 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 25 | 124 | 4.7883 | -3.1250 | 8/8 | 12/16 | Not applicable |
| 26 | 124 | 4.3851 | -4.1331 | 8/8 | 16/16 | Not applicable |
| 27 | 124 | 4.7883 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 28 | 124 | 4.6875 | -3.9315 | 8/8 | 13/16 | Not applicable |
| 29 | 124 | 4.7883 | -3.3770 | 8/8 | 12/16 | Not applicable |
| 30 | 124 | 4.7883 | -3.1250 | 8/8 | 12/16 | Not applicable |
| 31 | 124 | 4.7883 | -3.5282 | 8/8 | 13/16 | Not applicable |
| 32 | 124 | 5.1915 | -3.9315 | 8/8 | 13/16 | Not applicable |

**Supplementary Table S10. Confirmation population**

| Block removed | Requests retained | Present | Absent | Assignment reversals | Pair reversals | Original confirmation criterion |
|---|---:|---:|---:|---:|---:|---|
| 1 | 80 | 5.6250 | -3.5937 | 4/4 | 6/8 | Met |
| 2 | 80 | 5.6250 | -1.5625 | 3/4 | 4/8 | Not met |
| 3 | 80 | 5.6250 | -2.0312 | 3/4 | 5/8 | Met |
| 4 | 80 | 5.6250 | -4.6875 | 4/4 | 6/8 | Met |
| 5 | 80 | 5.6250 | -2.0312 | 3/4 | 5/8 | Met |
| 6 | 80 | 5.6250 | -0.1562 | 2/4 | 3/8 | Not met |
| 7 | 80 | 5.3125 | -3.2812 | 4/4 | 6/8 | Met |
| 8 | 80 | 5.6250 | -2.8125 | 4/4 | 5/8 | Met |
| 9 | 80 | 5.6250 | -2.0312 | 3/4 | 5/8 | Met |
| 10 | 80 | 5.6250 | -1.8750 | 3/4 | 5/8 | Not met |
| 11 | 80 | 4.5312 | -1.5625 | 3/4 | 4/8 | Not met |
| 12 | 80 | 4.3750 | -3.9062 | 4/4 | 6/8 | Met |
| 13 | 80 | 5.6250 | -2.6562 | 3/4 | 5/8 | Met |
| 14 | 80 | 5.0000 | -2.1875 | 3/4 | 5/8 | Met |
| 15 | 80 | 5.0000 | -3.5937 | 4/4 | 6/8 | Met |
| 16 | 80 | 4.3750 | -2.8125 | 3/4 | 5/8 | Met |
| 17 | 80 | 5.1562 | -2.6562 | 3/4 | 5/8 | Met |
| 18 | 80 | 5.6250 | -2.6562 | 3/4 | 5/8 | Met |
| 19 | 80 | 5.6250 | -2.3438 | 3/4 | 4/8 | Met |
| 20 | 80 | 5.6250 | -2.5000 | 4/4 | 5/8 | Met |
| 21 | 80 | 5.6250 | -2.1875 | 3/4 | 5/8 | Met |

For the reporting-mixture calculation in Section 5, the exact full-sample contrasts are d+ = 95/2048 and d− = −39/1024 initially, and d+ = 3/56 and d− = −17/672 in confirmation. Solving p d+ + (1 − p) d− = 0 yields p = 78/173 (45.0867%) and p = 17/53 (32.0755%). At p = 1/2 the respective differences are 17/4096 (0.4150 percentage points) and 19/1344 (1.4137 points). These are algebraic reweightings of the saved conditional averages, without new observations.

### S11. Detailed construction, adaptation and computational checks

Citation numbers refer to the main manuscript. Sections S1–S10 retain the study results and provenance inventories.

**S11.1. Data source and initial cohort construction.**

We use the ToolBenchG3 data distributed with COLT at commit `bbec292c38cabe3fbae098f50cc31b2e9f7e8fca` [2,3]. The fixed catalogue contains 1,419 tools. Requests and references are drawn from the training partition released by the authors. The catalogue, training references and selected requests are identified by checksums in the retained protocol. The full public query file was downloaded and JSON-decoded during preparation. Only reference IDs from the authors' training partition were used to construct these cohorts. Official test relevance files were not used.

The original population construction excluded 285 reference sets previously used for evaluation and required an eligible evaluation example outside the 2,250 request IDs and normalized texts encountered in earlier development. This left 1,321 eligible two-tool edges and 2,945 native four-cycles. Cycles were sorted by SHA-256 of their canonical serialized edge list, then greedily accepted when their tools and reference sets were disjoint from previously accepted cycles. This produced 39 blocks; the first 32 were retained. Evaluation examples were selected by the minimum of a fixed salted hash over eligible IDs and normalized text. A separate salted-hash rule selected a training example with different normalized text for each set. These selection rules preceded evaluation of this population; the formal study reuses the resulting population as described below.

The fixed evaluation population contains 32 tool-disjoint exchange blocks, four reference sets per block and one request per set, giving 128 requests involving 128 distinct participating tools. Each training arm contains 64 exchange examples and 448 common background examples. Thus, both arms contain 512 distinct reference sets, with one example per set. Their total query count, per-tool reference frequencies, reference cardinality distribution, distinct-set count and repetition profile are identical. Normalized training texts and IDs are disjoint from the fixed evaluation requests.

Two new background settings, identified by seeds 71 and 97, are crossed with eight new exposure assignments. Assignment bits are selected by a deterministic SHA-256 rule for seeds 101, 211, 307, 401, 503, 601, 701 and 809. An assignment and its global complement merely exchange the names of the two arms, so complements and the earlier development assignment are excluded. Each assignment flips the disjoint-pair allocation within selected blocks. These settings produce 16 paired cohorts and a union of 1,006 training requests.

The common backgrounds can contain larger reference sets that include an evaluated tool pair. This occurs for 25 of the 128 evaluation pairs in background 71 and 32 in background 97. Those examples are shared exactly between the two arms. We retain all requests and measure the incremental presence of a full-set exemplar, rather than absence of all prior tool-pair co-occurrence.

**S11.2. Encoder, controls and adaptation recipes.**

All formal comparisons use `Lux1997/Tool-Embed-0.6B`, revision `103d16d3593dec6c6f2217be620febb846932f6a` [13]. The loaded encoder has 595,776,512 backbone parameters and produces 1,024-dimensional normalized vectors. We use its saved query instruction, last-token pooling, left padding and a 512-token limit. The catalogue vectors and evaluation vectors are identical across all conditions. The checkpoint's earlier exposure to ToolBench is unknown; the controlled intervention is restricted to the current adaptation stage.

The frozen retriever ranks tools by query–tool cosine similarity. BM25 [14] uses the fixed tool text corpus, k1 = 1.5 and b = 0.75, with the pinned implementation's tokenization and inverse-document-frequency handling. Both rankings are invariant to exposure assignment and provide zero-effect controls.

The one-nearest-neighbor (1NN) control searches only the current arm's 512 training-query vectors. It places tools referenced by the highest-cosine training query first, ordered by frozen query–tool similarity, then appends the remaining tools in frozen order. Ties follow the fixed training order and numeric catalogue order. Evaluation reference sets are used for scoring after retrieval, and are not supplied to this control.

### 3.5 Linear query adapter

The linear recipe learns a 1,024 × 1,024 matrix W, initialized to the identity. A request vector is transformed by W and normalized; tool vectors remain fixed. Training uses normalized multi-reference cross-entropy over the complete 1,419-tool catalogue, with temperature 0.05. Each positive tool receives target mass 1/|R(q)|.

A fixed geometry term penalizes changes in within-query score differences. If Z and Z0 are the adapted and frozen score matrices, respectively, subtract each row's mean to obtain Zc and Z0c. The penalty is MSE(Zc,Z0c)/mean(Z0c²), weighted by 0.1. These settings were retained from development rather than selected on the formal assignments. Adam uses learning rate 0.001, a full batch of 512 examples, seed 17 and 200 updates. This recipe is a controlled linear adapter; the multi-reference target is related to the distributional construction in COLT [3], while the complete objective and architecture differ from COLT's graph stage.

### 3.6 COLT collaborative-stage adaptation

The graph recipe follows the reviewed collaborative-stage operations in the fixed COLT implementation [3]. It is initialized with the same frozen query and tool vectors. Its trainable parameters are the current arm's query table Q0 and catalogue table T0. Training scenes are identified by canonical full reference sets. The initial scene tensor S0 is computed once from the original scene–tool mean-pooling matrix and T0; following the source implementation, its values remain fixed while its retained gradient path reaches T0. It is not a separate trainable scene table.

Training uses query–tool and query–scene bipartite block graphs. Directed nonzero entries undergo independent edge dropout with probability 0.2, after which row and column degree square-root normalization is recomputed with the source's epsilon placement. Scene–tool pooling entries are independently dropped and row-normalized. The original scene–tool mean pool supplies S0; the dropped pool is used for the tool-view scene representation. All three dropout graphs are refreshed on each full-batch update.

One propagation layer retains the initial node features, computes the graph message divided by two, normalizes each message row and adds it to the initial features. The two views share Q0. For each training query, all positive tools are included in a candidate list of total length ten and the remaining positions are filled uniformly without replacement from non-positive tools. Candidate scores sum the tool-view and scene-view cosine scores. A softmax over that list is trained with fractional-target binary cross-entropy, including both the positive and complementary terms, averaged over queries and candidate positions. The source's task softmax has no extra temperature.

Single-direction tool-view-to-scene-view contrastive losses are calculated for queries and scenes, with temperature 0.05. Their mean is weighted by 0.04 and added to the candidate-list objective. Adam uses learning rate 0.001 and weight decay 10⁻⁷. We retain 200 full-batch updates and seed 17. Local Torch random streams replace the source's NumPy/DataLoader streams, and stable logarithmic expressions implement the same objectives. We adapt the stage to a 512-query batch; the original loader's batch size of 2,048 with dropped tails would otherwise produce no update on these cohorts. Original semantic-encoder fine-tuning and validation/test selection are omitted.

For a new query with no training graph edges, both propagated query views equal its original vector. Its score is consequently twice the cosine between that vector and the final no-drop tool-view tool vector. This cold-query expression supplies inference without evaluation reference edges. The experiment therefore evaluates a frozen-encoder COLT collaborative-stage adaptation, rather than a reproduction of the complete two-stage COLT benchmark results.

**S11.3. Initial fit and numerical replay.**

The initial formal comparison comprised 32 linear and 32 graph-stage fits. Within each arm, both recipes used the same training cohort. For each recipe, settings and update counts were held fixed across the paired arms. The families differ in objective, trainable parameters and computational work, which are reported separately. Fixed controls, 1NN outputs, all fitted states, full catalogue rankings, metrics and input/output checksums were retained. A separately written NumPy replay checked all 12,544 physical prediction rows and the reported aggregates. Its prospectively specified absolute score tolerance was 2 × 10⁻⁵. The maximum observed discrepancy was 1.37 × 10⁻⁶; top-five and top-ten orders were unchanged, and two near-tied top-twenty orders changed without changing their membership.

**S11.4. Confirmation design and numerical replay.**

After the secondary ranking pattern was observed, we fixed a separate confirmation protocol before encoding or fitting new examples. When selecting the new evaluation requests and their paired training exemplars, we excluded requests previously used in local adaptation, development or evaluation, their normalized texts, and complete reference sets encountered in those uses. Common backgrounds could reuse earlier training material. The provenance audit covered nine native and local-history inputs. It additionally mapped an earlier tool-retrieval evaluation corpus into the native API namespace, requiring exact canonical API identities and agreement of the mapped references. This produced a recorded-use exclusion inventory of 4,365 native request IDs and 3,340 complete reference sets. The exclusion covers the recorded ToolBenchG3 uses and exactly mapped external history; unmapped external labels were not assigned invented catalogue identities. The public source JSON had already been decoded, and encoder pretraining exposure remains unknown.

The remaining native data yielded 673 eligible two-tool edges, 144 four-cycles and 21 blocks accepted by the fixed hash-sorted, tool-disjoint greedy rule. We retained all 21 accepted blocks, yielding 84 evaluation requests and 84 separate training exemplars. Their IDs, normalized texts and full reference sets were absent from the recorded-use exclusion inventory. The catalogue remained the same, and 38 of the 84 participating tools also occurred in the initial population. These are new evaluation requests and reference sets within ToolBenchG3, rather than a new benchmark or tool universe.

Each arm contained 42 exchange examples and 470 common background examples. Four non-complementary assignments, identified by seeds 1103, 1201, 1301 and 1409, were crossed with backgrounds 151 and 163. Training size, per-tool frequency, reference cardinality, distinct-set counts and repetition remained exactly matched within every pair. Larger common-background sets contained 14 of the 84 target pairs in background 151 and 11 in background 163. All requests remained in the denominator. The exchange/background mixture differs from the initial 64/448 mixture, making this confirmation an extension of the paired design under the same total training size.

The two recipes, encoder, optimizer seed, objectives and 200-update schedules were unchanged. The experiment allowed 16 fits per method, with no additional tuning or outcome-dependent fits. Let d+ denote graph-minus-linear COMP@10 with full-set examples and d− the corresponding difference without them. The prospective practical continuation rule required mean d+ ≥ 0.02, mean d− ≤ −0.02, and positive d+ with negative d− in at least three of four assignments. Each assignment first averaged its two backgrounds. The two-point margins were investment thresholds fixed before the new results, not statistical significance criteria. Assignment settings remained correlated through shared requests, training data and fitted states.

Numerical replay used the same prespecified absolute score tolerance of 2 × 10⁻⁵, zero relative tolerance and a 4 × 10⁻⁵ limit for ranking inversions near ties. The metrics computed from stored rankings and the aggregates of those metrics had to be reproduced exactly. We also checked whether independently sorted rankings changed the primary decision. The independent NumPy auditor was implemented without inspecting the new scores, then fixed by checksum before its native execution. It reconstructs inference from saved states and does not replay optimizer trajectories.

**S11.5. Confirmation metrics and computational resources.**

Both fixed controls retained exactly zero exposure differences. The 1NN control again showed exposure sensitivity, with a 14.2857-point difference. Independent numerical replay reproduced all 4,200 prediction rows and original-rank aggregates, with 10,480 checks and no failures. The maximum score discrepancy was 1.49 × 10⁻⁶. Some full-catalogue orders differed near numerical ties; all top-five, top-ten and top-twenty orders, reported metrics and the primary continuation decision remained unchanged.

The full 64-fit comparison, including setup, scoring, serialization and output hashing, completed in 361.04 seconds on an Apple M5 system with 16 GiB unified memory. PyTorch used four CPU threads. The process peak resident memory was 874,135,552 bytes. Summed reported fit times were 68.01 seconds for the 32 linear fits and 286.43 seconds for the 32 graph-stage fits, averaging 2.13 and 8.95 seconds per fit, respectively. The retained linear state occupied 4,194,570 bytes per fit; graph checkpoints containing the raw query and tool tables occupied 7,909,924 bytes. These are retained fit-state sizes rather than a measurement of deployment memory.

Generating the additional 720 training-query vectors required 22.66 seconds using the Metal Performance Shaders (MPS) backend. We reused 286 training vectors together with all catalogue and evaluation vectors from development. Earlier encoding and development costs are retained in the provenance records. The formal comparison performed no encoder fine-tuning, paid model calls or new human evaluation.


The later confirmation completed all 32 fits, scoring and serialization in 178.44 seconds on four CPU threads, with peak process resident memory of 981,958,656 bytes. Its 16 linear fits took 33.17 seconds in total and its 16 graph fits took 141.62 seconds. Encoding 1,015 new query vectors, including all 84 evaluation requests, took 29.77 seconds on MPS with peak resident memory of 2,362,458,112 bytes. The confirmation reused 72 training vectors and all 1,419 catalogue vectors. It required no new model download, encoder fine-tuning, paid calls or new human annotation.
