# $ cat << EOF > run_lambdamart.py
# -*- coding: utf-8 -*-

import numpy as np

import logging,argparse

from rankpy.queries import Queries
from rankpy.models import LambdaMART
from rankpy.metrics import *

parser = argparse.ArgumentParser(description="Rank py.")
parser.add_argument("metric",help="metric",type=int)
parser.add_argument("iter",help="iterations",type=int)
args = parser.parse_args()

# Turn on logging.
logging.basicConfig(format='%(asctime)s : %(message)s', level=logging.INFO)

# Load the query datasets.
train_queries = Queries.load_from_text('data/train.txt')
valid_queries = Queries.load_from_text('data/vali.txt')
test_queries = Queries.load_from_text('data/test.txt')

logging.info('================================================================================')

# Save them to binary format ...
train_queries.save('data/fold2_train')
valid_queries.save('data/fold2_vali')
test_queries.save('data/fold2_test')

# ... because loading them will be then faster.
train_queries = Queries.load('data/fold2_train')
valid_queries = Queries.load('data/fold2_vali')
test_queries = Queries.load('data/fold2_test')

logging.info('================================================================================')

# Print basic info about query datasets.
logging.info('Train queries: %s' % train_queries)
logging.info('Valid queries: %s' % valid_queries)
logging.info('Test queries: %s' %test_queries)

logging.info('================================================================================')
metrics = {}
# Prepare metric for this set of queries.
metrics[0] = NormalizedDiscountedCumulativeGain(10, queries=[train_queries, valid_queries, test_queries])
# metrics[1] = SeznamRank(10, queries=[train_queries, valid_queries, test_queries])
metrics[1] = DiscountedCumulativeGain(10, queries=[train_queries, valid_queries, test_queries])
metrics[2] = WinnerTakesAll(10, queries=[train_queries, valid_queries, test_queries])
# metrics[4] = ExpectedReciprocalRank(10, queries=[train_queries, valid_queries, test_queries])
# Initialize LambdaMART model and train it.
model = LambdaMART(n_estimators=50000, max_depth=4, shrinkage=0.1, estopping=args.iter, n_jobs=-1)
metric = metrics(args.metric)
model.fit(metric, train_queries, validation=valid_queries)

logging.info('================================================================================')

# Print out the performance on the test set.
logging.info('%s on the test queries: %.8f' % (metric, metric.evaluate_queries(test_queries, model.predict(test_queries, n_jobs=-1))))
#EOF