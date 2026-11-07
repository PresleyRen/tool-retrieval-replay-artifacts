# Tool retrieval replay artifacts

Saved-ranking reproduction for the two main tables

Keep the CSV unchanged. A spreadsheet can display the data, but re-saving it can change leading zeroes and invalidate the hash. From the folder containing both files, run:

    python3 -B replay_main_tables_from_csv.py supporting-rankings-for-main-table-replay--2026-11-04--v01.csv

The Python standard library is sufficient. Output should report PASS_SAVED_TOP20_TO_MAIN_TABLES with 16,744 predictions, 117,208 row metric comparisons, 50 main-table values and a true confirmation gate. No neural inference or training is run.

The CSV has one row per saved prediction. Gold and ranked tool indices are space-separated. Blank orientation, background, arm and seen_arm values identify fixed retrievers. A/B exposure labels apply to adaptive comparisons. ToolBenchG3 request IDs and zero-based tool indices use the evaluation's fixed catalogue. Upstream benchmark provenance is ToolBenchG3 by Tool-COLT, source COLT commit bbec292c38cabe3fbae098f50cc31b2e9f7e8fca (https://github.com/quchangle1/COLT/tree/bbec292c38cabe3fbae098f50cc31b2e9f7e8fca). The ToolBenchG3 dataset card states CC BY 4.0 (https://huggingface.co/datasets/Tool-COLT/ToolBenchG3). Cite Qu et al., CIKM 2024, https://doi.org/10.1145/3627673.3679847. This extract contains selected saved prediction fields and no upstream code, native request text, model weights or tokenizers.

832be830af10c922a8936046f1f14a186b50439899db9c1e1a89be0ad68726a5  supporting-rankings-for-main-table-replay--2026-11-04--v01.csv
6650e3ebfac56c813426b6d051b376f2435c2826c72f4b6406e56c1343ca0d22  replay_main_tables_from_csv.py

The separate figure CSV contains the plotted values for the paired exposure and adaptation performance figure. It is not required by the table replay.

## Supplementary analyses (7 November 2026)

The [supplementary information](supplementary-information--2026-11-07--v01.md) includes the original sensitivity tables, all 53 post hoc evaluation-block deletions, and implementation details. The new analysis removes one four-request evaluation block at a time from saved predictions; it does not refit models or supply an independent population or confidence interval. All deletions preserve the aggregate contrast signs, but four of 21 confirmation deletions fail the original two-percentage-point absent-condition margin. This unfavorable sensitivity is retained.

Download the two files in `block-sensitivity/` alongside the original rankings CSV. From the repository root, run:

```sh
python3 -I -S -B block-sensitivity/replay_block_sensitivity.py supporting-rankings-for-main-table-replay--2026-11-04--v01.csv block-sensitivity/request-to-cycle--2026-11-07--v01.csv --output new-block-results.json
```

The script checks both input hashes and refuses to overwrite an existing output. The request mapping contains only benchmark request IDs and cycle IDs; it includes no request text or contact information. All results use the same two constructed ToolBenchG3 populations. The supplementary material is a research artifact, not a notice of journal acceptance.
