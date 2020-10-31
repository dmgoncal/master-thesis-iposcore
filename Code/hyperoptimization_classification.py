# -*- coding: utf-8 -*-
"""OPT

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n0PPHiXiy-fE5nHPdMWn3ouunz61DjxS
"""

import math
import numpy as np
import pandas as pd
import global_variables
import load_and_run

import xgboost
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from hyperopt import STATUS_OK
from hyperopt import tpe
from hyperopt import Trials
from hyperopt import fmin
from hyperopt import hp

MAX_EVALS = 100
OUTPUT = global_variables.outputs[3]            # CHANGE ACCORDINGLY
variables = global_variables.binarias+global_variables.categoricas+global_variables.numericas
# variables = ['pneumonia (%)', 'complicações sérias (%)', 'qualquer complicação (%)', 'ACS - previsão dias internamento', 'readmissão (%)', 'Discharge to Nursing or Rehab Facility (%)', '% morbilidade P-Possum', 'reoperação (%)', 'morte (%)', '% mortalidade P-Possum', 'tromboembolismo venoso (%)', 'Score fisiológico P-Possum', 'Score gravidade cirúrgica P-Possum', 'complicações cardíacas (%)', 'falência renal (%)', 'ITU (%)']
dataset = load_and_run.load_data(OUTPUT,variables)

headers = dataset.columns
to_dummify = []
for i in range(0,len(headers)):
  if headers[i] in global_variables.categoricas:
    to_dummify.append(i)

dataset = dataset.to_numpy()
# for x in dataset:
#   print(x)
dataset[:,-1] = [str(x) for x in dataset[:,-1]]  # Unknown target type error solved!

#KNN
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['n_neighbors']=int(params['n_neighbors'])
    res = load_and_run.k_fold(KNeighborsClassifier(**params),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'n_neighbors': hp.quniform('n_neighbors', 2, 50, 2),
         'weights': hp.choice('weights', ['distance', 'uniform'])}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#Decision Tree
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['max_depth']=int(params['max_depth'])
    params['min_samples_split']=int(params['min_samples_split'])
    params['min_samples_leaf']=int(params['min_samples_leaf'])
    # params['max_features']=int(params['max_features'])
    res = load_and_run.k_fold(tree.DecisionTreeClassifier(**params),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'criterion': hp.choice('criterion', ['gini', 'entropy']),
'splitter': hp.choice('splitter', ['best', 'random']),
'max_depth': hp.quniform('max_depth', 3, 105, 3),
'min_samples_split': hp.quniform('min_samples_split', 2, 20, 2),
'min_samples_leaf': hp.quniform('min_samples_leaf', 2, 20, 2),
'min_weight_fraction_leaf': hp.loguniform('min_weight_fraction_leaf', np.log(0.0001), np.log(0.5)),
# 'max_features': hp.quniform('max_features', 10, 100, 10),
'ccp_alpha': hp.loguniform('ccp_alpha', np.log(0.0001), np.log(0.2))}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#Random Forest
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['n_estimators']=int(params['n_estimators'])
    # params['max_depth']=int(params['max_depth'])
    params['min_samples_split']=int(params['min_samples_split'])
    params['min_samples_leaf']=int(params['min_samples_leaf'])
    # params['max_features']=int(params['max_features'])
    res = load_and_run.k_fold(RandomForestClassifier(**params),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'n_estimators': hp.quniform('n_estimators', 20, 200, 10),
'criterion': hp.choice('criterion', ['gini', 'entropy']),
# 'max_depth': hp.quniform('max_depth', 1, 100, 5),
'min_samples_split': hp.quniform('min_samples_split', 2, 20, 2),
'min_samples_leaf': hp.quniform('min_samples_leaf', 2, 20, 2),
'min_weight_fraction_leaf': hp.loguniform('min_weight_fraction_leaf', np.log(0.0001), np.log(0.5)),
# 'max_features': hp.quniform('max_features', 10, 100, 10),
#bootstrap
'ccp_alpha': hp.loguniform('ccp_alpha', np.log(0.0001), np.log(0.2))}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#SVM
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['degree']=int(params['degree'])
    res = load_and_run.k_fold(svm.SVC(**params,probability=True,cache_size=7000),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'kernel': hp.choice('kernel', ['linear', 'poly', 'rbf', 'sigmoid']),
'C': hp.uniform('C', 0.0, 2.0),
'degree': hp.quniform('degree', 3, 5, 1),
'gamma': hp.choice('gamma', ['scale', 'auto']),
'shrinking': hp.choice('shrinking', [True, False]),
'tol': hp.loguniform('tol', np.log(0.001), np.log(0.1)),
'decision_function_shape': hp.choice('decision_function_shape', ['ovo', 'ovr'])}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#   LOGISTIC
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    print(params)
    temp = params['solver']
    params['solver']=temp['solver']
    if(isinstance(temp['penalty'],dict)):
      temp2 = temp['penalty']
      params['penalty']=temp2['penalty']
      if('dual' in temp2.keys()):
        params['dual']=temp2['dual']
      elif ('l1_ratio' in temp2.keys()):
        params['l1_ratio']=temp2['l1_ratio']
    else:
      params['penalty']=temp['penalty']
    res = load_and_run.k_fold(LogisticRegression(**params, max_iter=1000,random_state=0),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'fit_intercept': hp.choice('fit_intercept', [True,False]),
         'C': hp.uniform('C', 0.0, 2.0),
         'solver': hp.choice('solver', 
                            [{'solver': 'liblinear', 
                                'penalty': hp.choice('penalty',
                                    [{'penalty':'l1'},
                                     {'penalty': 'l2',
                                          'dual': hp.choice('l2_dual', [True,False])}])},
                            {'solver': 'newton-cg',
                                'penalty': hp.choice('newton_penalty', ['l2','none'])},
                            {'solver': 'sag',
                                'penalty': hp.choice('sag_penalty', ['l2','none'])},
                            {'solver': 'lbfgs',
                                'penalty': hp.choice('lbfgs_penalty', ['l2','none'])},
                            {'solver': 'saga',
                                'penalty': hp.choice('saga_penalty',
                                    [{'penalty':'l2'},
                                     {'penalty':'none'},
                                     {'penalty': 'elasticnet',
                                          'l1_ratio': hp.uniform('l1_ratio', 0.0, 1.0)}])}])}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#XGB
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['n_estimators']=int(params['n_estimators'])
    params['max_depth']=int(params['max_depth'])
    res = load_and_run.k_fold(XGBClassifier(**params,objective='binary:logistic'),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'max_depth': hp.quniform('max_depth', 3, 45, 3),
'learning_rate': hp.loguniform('learning_rate', np.log(0.0001), np.log(0.9)),
'booster': hp.choice('booster', ['gbtree', 'gblinear', 'dart']),
'reg_alpha': hp.loguniform('reg_alpha', np.log(0.0001), np.log(0.1)),
'gamma': hp.loguniform('gamma', np.log(0.0001), np.log(5.0)),
'n_estimators': hp.quniform('n_estimators', 20, 500, 10)}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))

#MLP
tpe_algorithm = tpe.suggest
bayes_trials = Trials()

def objective(params):
    params['batch_size']=int(params['batch_size'])
    res = load_and_run.k_fold(MLPClassifier(**params,max_iter=2000),dataset,headers,to_dummify)
    return {'loss': res, 'params': params, 'status': STATUS_OK}

space = {'activation': hp.choice('activation', ['identity', 'logistic', 'tanh', 'relu']),
'solver': hp.choice('solver', ['lbfgs', 'sgd', 'adam']),
'alpha': hp.loguniform('alpha', np.log(0.0001), np.log(0.2)),
'learning_rate_init': hp.loguniform('learning_rate_init', np.log(0.001), np.log(0.2)),
'batch_size': hp.quniform('batch_size', 50, 300, 50),
'early_stopping': hp.choice('early_stopping', [True,False]),
'learning_rate': hp.choice('learning_rate', ['constant', 'invscaling', 'adaptive']),
'hidden_layer_sizes': hp.choice('hidden_layer_sizes', [(50,50,50,), (50,100,50,), (100,100,),(50,50,),(50,25,),(50,),(25)])}

print(fmin(fn = objective, space = space, algo = tpe.suggest, max_evals = MAX_EVALS, trials = bayes_trials))