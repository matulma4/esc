# $ cat << EOF > run_lambdamart.py
# -*- coding: utf-8 -*-

import numpy as np

import logging

from rankpy.queries import Queries
from rankpy.models import LambdaMART
from rankpy.metrics import *

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

# Prepare metric for this set of queries.
# metric = NormalizedDiscountedCumulativeGain(10, queries=[train_queries, valid_queries, test_queries])
# metric = SeznamRank(10, queries=[train_queries, valid_queries, test_queries])
# metric = DiscountedCumulativeGain(10, queries=[train_queries, valid_queries, test_queries])
metric = WinnerTakesAll(10, queries=[train_queries, valid_queries, test_queries])
# metric = ExpectedReciprocalRank(10, queries=[train_queries, valid_queries, test_queries])
# Initialize LambdaMART model and train it.
model = LambdaMART(n_estimators=50000, max_depth=4, shrinkage=0.1, estopping=100, n_jobs=-1)
model.fit(metric, train_queries, validation=valid_queries)

logging.info('================================================================================')

# Print out the performance on the test set.
logging.info('%s on the test queries: %.8f' % (metric, metric.evaluate_queries(test_queries, model.predict(test_queries, n_jobs=-1))))
#EOF