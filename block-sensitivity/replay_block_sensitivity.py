"""Replay the evaluation-block sensitivity and weighting results from two CSV files.

Run: python3 replay_block_sensitivity.py RANKINGS.csv REQUEST_TO_CYCLE.csv
The first input is the saved top-20 rankings CSV linked in Data and code
availability. The second contains study, request_id and block_id. Block numbers
follow the ascending frozen block IDs in each study. Output is JSON.
The procedure only removes evaluation rows.
It requires no model, training data, third-party package or network access.
"""
import argparse
from collections import Counter, defaultdict
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

INPUT_HASHES = (
    '832be830af10c922a8936046f1f14a186b50439899db9c1e1a89be0ad68726a5',
    '95c2d982fbafdc8b6e82f376248d2ad791a5eefada50bd0de3ec3ffb28504000',
)
DESIGNS = {
    '003': ((101, 211, 307, 401, 503, 601, 701, 809), (71, 97), 32),
    '004': ((1103, 1201, 1301, 1409), (151, 163), 21),
}
METHODS = ('query_only', 'colt_stage')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def input_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_blocks(path):
    requests = defaultdict(dict)
    with path.open(newline='', encoding='utf-8') as stream:
        rows = csv.DictReader(stream)
        require(rows.fieldnames == ['study', 'request_id', 'block_id'], 'unexpected mapping columns')
        for row in rows:
            study, request, block = (row[k] for k in rows.fieldnames)
            require(study in DESIGNS and request and block, 'invalid request-to-cycle mapping')
            require(request not in requests[study], 'duplicate study/request ID in cycle mapping')
            requests[study][request] = block
    for study, (_, _, expected_blocks) in DESIGNS.items():
        block_sizes = Counter(requests[study].values())
        require(len(block_sizes) == expected_blocks and set(block_sizes.values()) == {4},
                f'incorrect number or size of blocks in study {study}')
    return requests


def read_scores(path, requests):
    scores = defaultdict(dict)
    with path.open(newline='', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            method = row['method']
            if method not in METHODS:
                continue
            study, request = row['study'], row['request_id']
            require(request in requests[study], 'ranked request is missing from the cycle mapping')
            orientation, background = int(row['orientation']), int(row['background'])
            orientations, backgrounds, _ = DESIGNS[study]
            require(orientation in orientations and background in backgrounds, 'unexpected design setting')
            require(row['arm'] in ('A', 'B') and row['seen_arm'] in ('A', 'B'), 'invalid exposure arm')
            condition = 'present' if row['arm'] == row['seen_arm'] else 'absent'
            cell = scores[study, request]
            key = (orientation, background, condition, method)
            require(key not in cell, 'duplicate prediction for a study/request/method/setting/condition')
            gold = set(map(int, row['gold_tool_indices'].split()))
            ranks = list(map(int, row['top20_tool_indices'].split()))
            require(len(gold) == 2 and len(ranks) == len(set(ranks)) == 20, 'invalid gold or top-20 ranks')
            cell[key] = int(gold.issubset(ranks[:10]))
    return scores


def count_by_block(study, requests, scores):
    orientations, backgrounds, _ = DESIGNS[study]
    cells = [(o, b, c) for o in orientations for b in backgrounds for c in ('present', 'absent')]
    blocks = defaultdict(Counter)
    for request, block in requests[study].items():
        values = scores[study, request]
        require(len(values) == len(cells) * len(METHODS), 'incomplete matched request prediction')
        for key in cells:
            blocks[block][key] += values[(*key, 'colt_stage')] - values[(*key, 'query_only')]
    return blocks


def average(values):
    return sum(values) / len(values)


def format_points(rate):
    return f'{float(rate) * 100:.4f}'


def pairs_by_setting(orientations, backgrounds, counts, n):
    return {(o, b): (Fraction(counts[o, b, 'present'], n), Fraction(counts[o, b, 'absent'], n))
            for o in orientations for b in backgrounds}


def reversals(pairs):
    return sum(present > 0 and absent < 0 for present, absent in pairs)


def calculate(study, n, counts):
    orientations, backgrounds, _ = DESIGNS[study]
    pairs = pairs_by_setting(orientations, backgrounds, counts, n)
    assignments = {o: tuple(average([pairs[o, b][i] for b in backgrounds]) for i in (0, 1))
                   for o in orientations}
    present, absent = (average([pair[i] for pair in assignments.values()]) for i in (0, 1))
    assignment_reversals = reversals(assignments.values())
    return {
        'retained_requests': n,
        'present_pp': format_points(present), 'absent_pp': format_points(absent),
        'present_exact_rate_difference': str(present), 'absent_exact_rate_difference': str(absent),
        'assignment_reversals': assignment_reversals, 'pair_reversals': reversals(pairs.values()),
        'original_confirmation_criterion': (
            present >= Fraction(2, 100) and absent <= Fraction(-2, 100) and assignment_reversals >= 3
        ) if study == '004' else None,
        'assignments': [[o, *(format_points(x) for x in pair)] for o, pair in assignments.items()],
        'assignment_background_pairs': [[o, b, *(format_points(x) for x in pair)] for (o, b), pair in pairs.items()],
    }


def replay(study, requests, scores):
    n = len(requests[study])
    blocks = count_by_block(study, requests, scores)
    cells = next(iter(blocks.values()))
    counts = {key: sum(block[key] for block in blocks.values()) for key in cells}
    full = calculate(study, n, counts)
    folds = [
        {'block_number': number, 'block_id': block, **calculate(
            study, n - 4, {key: count - subtotal[key] for key, count in counts.items()})}
        for number, (block, subtotal) in enumerate(sorted(blocks.items()), 1)
    ]
    present, absent = (Fraction(full[f'{c}_exact_rate_difference']) for c in ('present', 'absent'))
    zero = -absent / (present - absent)
    equal = (present + absent) / 2
    return {
        'full_sample': full, 'block_deletions': folds,
        'reweighting': {
            'zero_crossing_present_weight': str(zero), 'zero_crossing_present_percent': format_points(zero),
            'equal_weight_exact_rate_difference': str(equal), 'equal_weight_difference_pp': format_points(equal),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rankings', type=Path)
    parser.add_argument('request_to_cycle', type=Path)
    parser.add_argument('--output', type=Path, help='write a new JSON file instead of stdout')
    args = parser.parse_args()
    hashes = tuple(input_hash(p) for p in (args.rankings, args.request_to_cycle))
    require(hashes == INPUT_HASHES, 'input checksum mismatch; use the archived rankings and mapping CSVs')
    requests = read_blocks(args.request_to_cycle)
    scores = read_scores(args.rankings, requests)
    result = {
        'rankings_sha256': hashes[0], 'request_to_cycle_sha256': hashes[1],
        'studies': {study: replay(study, requests, scores) for study in DESIGNS},
    }
    if args.output:
        with args.output.open('x', encoding='utf-8') as target:
            json.dump(result, target, indent=2)
            target.write('\n')
    else:
        json.dump(result, sys.stdout, indent=2)
        print()


if __name__ == '__main__':
    main()
