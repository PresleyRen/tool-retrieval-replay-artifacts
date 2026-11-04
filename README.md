# Tool retrieval replay artifacts

Saved-ranking reproduction for the two main tables

Keep the CSV unchanged. A spreadsheet can display the data, but re-saving it can change leading zeroes and invalidate the hash. From the folder containing both files, run:

    python3 -B replay_main_tables_from_csv.py supporting-rankings-for-main-table-replay--2026-11-04--v01.csv

The Python standard library is sufficient. Output should report PASS_SAVED_TOP20_TO_MAIN_TABLES with 16,744 predictions, 117,208 row metric comparisons, 50 main-table values and a true confirmation gate. No neural inference or training is run.

The CSV has one row per saved prediction. Gold and ranked tool indices are space-separated. Blank orientation, background, arm and seen_arm values identify fixed retrievers. A/B exposure labels apply to adaptive comparisons. ToolBenchG3 request IDs and zero-based tool indices use the evaluation's fixed catalogue. Upstream benchmark provenance is ToolBenchG3 by Tool-COLT, source COLT commit bbec292c38cabe3fbae098f50cc31b2e9f7e8fca (https://github.com/quchangle1/COLT/tree/bbec292c38cabe3fbae098f50cc31b2e9f7e8fca). The ToolBenchG3 dataset card states CC BY 4.0 (https://huggingface.co/datasets/Tool-COLT/ToolBenchG3). Cite Qu et al., CIKM 2024, https://doi.org/10.1145/3627673.3679847. This extract contains selected saved prediction fields and no upstream code, native request text, model weights or tokenizers.

832be830af10c922a8936046f1f14a186b50439899db9c1e1a89be0ad68726a5  supporting-rankings-for-main-table-replay--2026-11-04--v01.csv
6650e3ebfac56c813426b6d051b376f2435c2826c72f4b6406e56c1343ca0d22  replay_main_tables_from_csv.py

The separate figure CSV contains the plotted values for the paired exposure and adaptation performance figure. It is not required by the table replay.
