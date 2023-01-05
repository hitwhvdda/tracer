import os

PROJECT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
GLOBAL_RESULT_DIR = os.path.join('/data', 'pattern', 'result')

INFER_DIR = os.path.join(PROJECT_HOME, 'infer')
BUG_BENCH_DIR = os.path.join(PROJECT_HOME, 'bug-bench')
BENCHMARK_DIR = os.path.join(BUG_BENCH_DIR, 'benchmark')
RESULT_DIR = os.path.join(PROJECT_HOME, 'result')
JULIET_TESTCASE_DIR = os.path.join(PROJECT_HOME, 'juliet-test-suite-c',
                                   'testcases')

INFER_BIN = os.path.join(INFER_DIR, 'infer', 'bin', 'infer')
