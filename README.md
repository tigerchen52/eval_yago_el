# eval_yago_el
This repo contains code and data for an extrinsic evaluation of YAGO-4.5. To show the value of the new YAGO 4.5 over YAGO 4, we applied it to the task of entity disambiguation (also called entity linking).

## A quick reproduction of Table 3
We provide ready-to-use result files so that you can reproduce results easily.

**To get the results for YAGO-4**
```python
python eval_result.py -result_file data/yago_old.result -candidate_file data/yago_old.candidate

# expected outputs
# group [1] 13971 0.7693078519790996
# group [2] 3452 0.5903823870220162
# group [3] 1374 0.5269286754002911
# group [4] 203 0.2019704433497537
# Macro 19000 0.5221473394377901

```
**To get the results for YAGO-4.5**
```python
python eval_result.py -result_file data/yago_new.result -candidate_file data/yago_new.candidate


# expected outputs
# group [1] 13971 0.7999427385298118
# group [2] 3452 0.6410776361529548
# group [3] 1374 0.5786026200873362
# group [4] 203 0.31527093596059114
# Macro 19000 0.5837234826826735

```

## To re-run entity disambiguation
We use the end-to-end entity linking system [ExtEnD](https://github.com/SapienzaNLP/extend) in this experiment.
You should follow the official instructions to install ExtEnD (spaCy version).
After that, run the following code to reproduce the *.result files.

```python
# YAGO-4
# The file yago_old.candidate contains all candidates, and the class names from respective YAGO version
python run_extend.py -dataset_file data/blink_test.json -result_file data/yago_old.result -candidate_file data/yago_old.candidate

# YAGO-4.5
# The file yago_old.candidate contains all candidates, and the class names from respective YAGO version
python run_extend.py -dataset_file data/blink_test.json -result_file data/yago_new.result -candidate_file data/yago_new.candidate

