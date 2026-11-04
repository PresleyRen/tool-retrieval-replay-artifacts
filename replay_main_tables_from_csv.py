"""Recompute this paper's tables from saved top-20 rankings; standard library only.

This checks reported outcomes, not neural inference or optimizer trajectories.
This companion reads a flat CSV with row-level ranks, gold labels, and exposure labels.
No files are downloaded, fitted, or overwritten. Inputs remain subject to their
recorded licences; this script does not publish or grant rights to them.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
METHODS = ('frozen', 'BM25', '1NN', 'query_only', 'colt_stage')
ENDPOINTS = ('COMP@5', 'COMP@10', 'COMP@20', 'NDCG@10', 'Recall@5', 'Recall@10', 'Recall@20')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def scores(ranks, gold, catalogue_size):
    require(len(ranks) == len(set(ranks)) == 20, 'incomplete_or_duplicate_top20')
    require(all(type(i) is int and 0 <= i < catalogue_size for i in ranks), 'invalid_rank_index')
    require(len(gold) == len(set(gold)) > 0, 'empty_or_duplicate_gold')
    require(all(type(i) is int and 0 <= i < catalogue_size for i in gold), 'invalid_gold_index')
    refs = set(gold)
    result = {}
    for k in (5, 10, 20):
        hits = len(refs.intersection(ranks[:k]))
        result[f'COMP@{k}'] = float(hits == len(refs))
        result[f'Recall@{k}'] = hits / len(refs)
    dcg = sum(1 / math.log2(i + 2) for i, tool in enumerate(ranks[:10]) if tool in refs)
    ideal = sum(1 / math.log2(i + 2) for i in range(min(10, len(refs))))
    result['NDCG@10'] = dcg / ideal
    return result



STUDIES = {'003': {'catalogue_size': 1419, 'orientations': [101, 211, 307, 401, 503, 601, 701, 809], 'backgrounds': [71, 97], 'queries': 128, 'row_count': 12544}, '004': {'catalogue_size': 1419, 'orientations': [1103, 1201, 1301, 1409], 'backgrounds': [151, 163], 'queries': 84, 'row_count': 4200, 'gate': {'d_present_min': 0.02, 'd_absent_max': -0.02, 'min_reversal_directions': 3, 'direction_sign_rule': 'd_present>0 and d_absent<0', 'meaning': '2pp is a prespecified minimum practical recipe-selection difference/investment threshold, not a statistical test, journal rule or acceptance forecast.', 'pass': 'REPLICATED_CONFIRMATORY_CROSSOVER', 'scientific_fail': 'STOP_CONFIRMATORY_CROSSOVER', 'incomplete': 'INCOMPLETE_OR_INVALID_NOT_SCIENTIFIC_REFUTATION'}}}
EXPECTED_TABLES = [['67.1875', '67.1875', '0.0000', '71.4214', '71.4214'], ['22.6562', '22.6562', '0.0000', '40.4915', '40.4915'], ['86.3281', '73.4375', '12.8906', '86.3981', '66.1054'], ['91.7480', '83.0566', '8.6914', '89.0235', '78.8642'], ['96.3867', '79.2480', '17.1387', '92.7594', '74.8594'], ['75.0000', '75.0000', '0.0000', '75.8609', '75.8609'], ['27.3810', '27.3810', '0.0000', '45.7316', '45.7316'], ['91.0714', '76.7857', '14.2857', '88.1807', '66.3159'], ['91.0714', '80.8036', '10.2679', '88.5995', '78.5813'], ['96.4286', '78.2738', '18.1548', '93.6851', '74.7027']]
CSV_SHA256 = '832be830af10c922a8936046f1f14a186b50439899db9c1e1a89be0ad68726a5'

def replay(csv_path, number):
    study = STUDIES[number]
    orientations = study['orientations']
    backgrounds = study['backgrounds']
    exposures, gold, cells = {}, {}, {}
    rows = comparisons = 0
    with csv_path.open(newline='', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            require(row['study'] in STUDIES, 'unknown_study')
            if row['study'] != number:
                continue
            query = row['request_id']
            targets = [int(i) for i in row['gold_tool_indices'].split()]
            require(gold.setdefault(query, targets) == targets, 'inconsistent_gold')
            orientation = int(row['orientation']) if row['orientation'] else None
            background = int(row['background']) if row['background'] else None
            arm, seen = row['arm'] or None, row['seen_arm'] or None
            if orientation is None:
                require(background is None and arm is None and seen is None, 'unexpected_fixed_exposure')
            else:
                require(arm in ('A', 'B') and seen in ('A', 'B'), 'invalid_exposure')
                pair_exposures = exposures.setdefault((orientation, background), {})
                require(pair_exposures.setdefault(query, seen) == seen, 'inconsistent_exposure')
            key = (row['method'], orientation, background, arm)
            cell = cells.setdefault(key, {})
            require(query not in cell, 'duplicate_prediction')
            ranks = [int(i) for i in row['top20_tool_indices'].split()]
            values = scores(ranks, targets, study['catalogue_size'])
            for metric in ENDPOINTS:
                require(abs(values[metric] - float(row[metric])) < 1e-12, 'stored_row_metric_mismatch')
                comparisons += 1
            cell[query] = values
            rows += 1
    ids = list(gold)
    require(len(ids) == study['queries'], 'wrong_query_denominator')
    pair_keys = [(o, b) for o in orientations for b in backgrounds]
    require(set(exposures) == set(pair_keys), 'missing_or_extra_pair')
    require(all(set(v) == set(ids) for v in exposures.values()), 'wrong_exposure_denominator')
    data = {'pairs': [{'orientation_seed': o, 'background_seed': b,
                       'seen_conditions': [exposures[o, b][q] for q in ids]} for o, b in pair_keys],
            'orientations': [{'orientation_seed': o} for o in orientations]}
    expected = {(m, None, None, None) for m in METHODS[:2]} | {
        (m, o, b, arm) for m in METHODS[2:] for o, b in pair_keys for arm in ('A', 'B')}
    require(set(cells) == expected, 'missing_or_extra_prediction_cell')
    require(all(set(cell) == set(ids) for cell in cells.values()), 'wrong_cell_denominator')
    require(rows == study['row_count'], 'wrong_row_denominator')
    pair_results = []
    aggregate = {}
    for method in METHODS:
        aligned = {metric: [] for metric in ENDPOINTS}
        for pair in data['pairs']:
            orientation, background = pair['orientation_seed'], pair['background_seed']
            if method in METHODS[:2]:
                a = b = cells[method, None, None, None]
            else:
                a, b = (cells[method, orientation, background, arm] for arm in ('A', 'B'))
            present, absent = {}, {}
            require(len(pair['seen_conditions']) == len(ids), 'wrong_exposure_denominator')
            for metric in ENDPOINTS:
                exposed, unexposed = [], []
                for query_id, arm in zip(ids, pair['seen_conditions']):
                    require(arm in ('A', 'B'), 'invalid_exposure_label')
                    exposed.append((a if arm == 'A' else b)[query_id][metric])
                    unexposed.append((b if arm == 'A' else a)[query_id][metric])
                present[metric] = sum(exposed) / len(ids)
                absent[metric] = sum(unexposed) / len(ids)
                aligned[metric].append((present[metric], absent[metric]))
            pair_results.append(dict(method=method, orientation=orientation, background=background,
                                     present=present['COMP@10'], absent=absent['COMP@10']))
        aggregate[method] = {metric: dict(present=sum(v[0] for v in values) / len(values),
                                         absent=sum(v[1] for v in values) / len(values))
                             for metric, values in aligned.items()}
    table = []
    for method in METHODS:
        comp, ndcg = aggregate[method]['COMP@10'], aggregate[method]['NDCG@10']
        values = [comp['present'], comp['absent'], comp['present'] - comp['absent'], ndcg['present'], ndcg['absent']]
        table.append([f'{100 * value:.4f}' for value in values])
    directions = []
    for assignment in data['orientations']:
        orientation = assignment['orientation_seed']
        selected = {m: [r for r in pair_results if r['method'] == m and r['orientation'] == orientation]
                    for m in ('query_only', 'colt_stage')}
        d = {field: sum(r[field] for r in selected['colt_stage']) / len(selected['colt_stage'])
             - sum(r[field] for r in selected['query_only']) / len(selected['query_only']) for field in ('present', 'absent')}
        directions.append(dict(orientation=orientation, **d, reversal=d['present'] > 0 and d['absent'] < 0))
    paired = {(r['orientation'], r['background']): {} for r in pair_results}
    for row in pair_results:
        paired[row['orientation'], row['background']][row['method']] = row
    pair_reversals = sum(v['colt_stage']['present'] > v['query_only']['present'] and
                         v['colt_stage']['absent'] < v['query_only']['absent'] for v in paired.values())
    return dict(experiment=number, queries=len(ids), physical_rows=rows, cells=len(cells),
                row_metric_checks=comparisons, table=table, directions=directions,
                pair_reversals=pair_reversals, aggregate=aggregate)


def self_check():
    r = list(range(20))
    require(scores(r, [0, 1], 25)['NDCG@10'] == 1, 'ideal_test')
    require(scores(r, [0, 24], 25)['COMP@10'] == 0, 'missing_reference_test')
    require(scores(r, [0, 24], 25)['Recall@10'] == .5, 'partial_recall_test')
    require(scores(r, [19], 25)['COMP@10'] == 0 and scores(r, [19], 25)['COMP@20'] == 1, 'cutoff_test')
    for ranks, gold in [(r[:-1], [0]), ([0] * 20, [0]), (r, []), (r, [0, 0]), (r, [25]), ([-1] + r[1:], [0])]:
        try:
            scores(ranks, gold, 25)
        except ValueError:
            continue
        raise AssertionError('invalid_input_accepted')
    print('PASS: 4 scoring cases and 6 invalid-input cases')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    args = parser.parse_args()
    require(digest(args.csv) == CSV_SHA256, 'csv_hash_changed')
    self_check()
    results = [replay(args.csv, number) for number in STUDIES]
    require([row for study in results for row in study['table']] == EXPECTED_TABLES,
            'main_table_display_mismatch')
    independent = results[1]
    directions = independent['directions']
    reversals = sum(d['reversal'] for d in directions)
    require(reversals == 3 and independent['pair_reversals'] == 5, 'confirmation_reversal_count')
    gate = STUDIES['004']['gate']
    present = sum(d['present'] for d in directions) / len(directions)
    absent = sum(d['absent'] for d in directions) / len(directions)
    passed = (present >= gate['d_present_min'] and absent <= gate['d_absent_max']
              and reversals >= gate['min_reversal_directions'])
    require(passed, 'continuation_gate_mismatch')
    print(json.dumps(dict(status='PASS_SAVED_TOP20_TO_MAIN_TABLES', main_table_values=50,
                          predictions=sum(x['physical_rows'] for x in results),
                          row_metric_comparisons=sum(x['row_metric_checks'] for x in results),
                          confirmation_gate=passed, confirmation_reversals=reversals,
                          confirmation_pair_reversals=independent['pair_reversals'],
                          tables=[x['table'] for x in results]), indent=2))


if __name__ == '__main__':
    main()
