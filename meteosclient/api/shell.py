# Copyright 2013 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import inspect
import json
import sys

from meteosclient.openstack.common import cliutils as utils


def _print_list_field(field):
    return lambda obj: ', '.join(getattr(obj, field))


def _filter_call_args(args, func, remap={}):
    """Filter args according to func's parameter list.

    Take three arguments:
     * args - a dictionary
     * func - a function
     * remap - a dictionary
    Remove from dct all the keys which are not among the parameters
    of func. Before filtering, remap the keys in the args dict
    according to remap dict.
    """

    for name, new_name in remap.items():
        if name in args:
            args[new_name] = args[name]
            del args[name]

    valid_args = inspect.getargspec(func).args
    for name in args.keys():
        if name not in valid_args:
            print('WARNING: "%s" is not a valid parameter and will be '
                  'discarded from the request' % name)
            del args[name]


def _show_dict(dict, wrap=0):
    utils.print_dict(dict._info, wrap=wrap)


#
# Templates
# ~~~~~~~~
# template-list
#
# template-show <template_id>
#
# template-create [--json <file>]
#
# template-delete <template_id>
#

def do_template_list(cs, args):
    """Print a list of available templates."""
    templates = cs.templates.list()

    columns = ('id',
               'name',
               'status',
               'master_nodes',
               'worker_nodes',
               'spark_version')
    utils.print_list(templates, columns)


@utils.arg('id',
           metavar='<template_id>',
           help='ID of the template to show.')
def do_template_show(cs, args):
    """Show details of a template."""
    template = cs.templates.get(args.id)
    _show_dict(template)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of template.')
def do_template_create(cs, args):
    """Create a template."""
    template = json.loads(args.json.read())

    _filter_call_args(template, cs.templates.create)
    _show_dict(cs.templates.create(**template))


@utils.arg('id',
           metavar='<template_id>',
           help='ID of the template to delete.')
def do_template_delete(cs, args):
    """Delete a template."""
    cs.templates.delete(args.id)


#
# Experiments
# ~~~~~~~~
# experiment-list
#
# experiment-show <experiment_id>
#
# experiment-create [--json <file>]
#
# experiment-delete <experiment_id>
#

def do_experiment_list(cs, args):
    """Print a list of available experiments."""
    experiments = cs.experiments.list()

    columns = ('id',
               'name',
               'status',
               'created_at')
    utils.print_list(experiments, columns)


@utils.arg('id',
           metavar='<experiment_id>',
           help='ID of the experiment to show.')
def do_experiment_show(cs, args):
    """Show details of a experiment."""
    experiment = cs.experiments.get(args.id)
    _show_dict(experiment)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of experiment.')
def do_experiment_create(cs, args):
    """Create a experiment."""
    experiment = json.loads(args.json.read())

    _filter_call_args(experiment, cs.experiments.create)
    _show_dict(cs.experiments.create(**experiment))


@utils.arg('id',
           metavar='<experiment_id>',
           help='ID of the experiment to delete.')
def do_experiment_delete(cs, args):
    """Delete a experiment."""
    cs.experiments.delete(args.id)

#
# Datasets
# ~~~~~~~~
# dataset-list
#
# dataset-show <dataset_id>
#
# dataset-create [--json <file>]
#
# dataset-delete <dataset_id>
#


def do_dataset_list(cs, args):
    """Print a list of available datasets."""
    datasets = cs.datasets.list()

    columns = ('id',
               'name',
               'status',
               'source_dataset_url')
    utils.print_list(datasets, columns)


@utils.arg('id',
           metavar='<dataset_id>',
           help='ID of the dataset to show.')
def do_dataset_show(cs, args):
    """Show details of a dataset."""
    dataset = cs.datasets.get(args.id)
    _show_dict(dataset, wrap=50)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of dataset.')
def do_dataset_create(cs, args):
    """Create a dataset."""
    dataset = json.loads(args.json.read())

    _filter_call_args(dataset, cs.datasets.create)
    _show_dict(cs.datasets.create(**dataset))


@utils.arg('id',
           metavar='<dataset_id>',
           help='ID of the dataset to delete.')
def do_dataset_delete(cs, args):
    """Delete a dataset."""
    cs.datasets.delete(args.id)

#
# Models
# ~~~~~~~~
# model-list
#
# model-show <model_id>
#
# model-create [--json <file>]
#
# model-recreate [--json <file>]
#
# model-delete <model_id>
#
# model-load <model_id>
#
# model-unload <model_id>
#


def do_model_list(cs, args):
    """Print a list of available models."""
    models = cs.models.list()

    columns = ('id',
               'name',
               'status',
               'type',
               'source_dataset_url')
    utils.print_list(models, columns)


@utils.arg('id',
           metavar='<model_id>',
           help='ID of the model to show.')
def do_model_show(cs, args):
    """Show details of a model."""
    model = cs.models.get(args.id)
    _show_dict(model)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of model.')
def do_model_create(cs, args):
    """Create a model."""
    model = json.loads(args.json.read())

    _filter_call_args(model, cs.models.create)
    _show_dict(cs.models.create(**model))


@utils.arg('id',
           metavar='<model_id>',
           help='ID of the model to recreate.')
@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of model.')
def do_model_recreate(cs, args):
    """Recreate a model."""
    model = json.loads(args.json.read())

    _filter_call_args(model, cs.models.recreate)
    cs.models.recreate(args.id, **model)


@utils.arg('id',
           metavar='<model_id>',
           help='ID of the model to delete.')
def do_model_delete(cs, args):
    """Delete a model."""
    cs.models.delete(args.id)


@utils.arg('id',
           metavar='<model_id>',
           help='ID of the model to load.')
def do_model_load(cs, args):
    """Load a model for online prediction."""
    cs.models.load(args.id)


@utils.arg('id',
           metavar='<model_id>',
           help='ID of the model to unload.')
def do_model_unload(cs, args):
    """Unload a model."""
    cs.models.unload(args.id)


#
# Model_Evaluations
# ~~~~~~~~
# model_evaluation-list
#
# model_evaluation-show <model_evaluation_id>
#
# model_evaluation-create [--json <file>]
#
# model_evaluation-delete <model_evaluation_id>
#

def do_model_evaluation_list(cs, args):
    """Print a list of available model_evaluations."""
    model_evaluations = cs.model_evaluations.list()

    columns = ('id',
               'name',
               'status',
               'model_id',
               'model_type',
               'source_dataset_url',
               'stdout')
    utils.print_list(model_evaluations, columns)


@utils.arg('id',
           metavar='<model_evaluation_id>',
           help='ID of the model_evaluation to show.')
def do_model_evaluation_show(cs, args):
    """Show details of a model_evaluation."""
    model_evaluation = cs.model_evaluations.get(args.id)
    _show_dict(model_evaluation)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of model_evaluation.')
def do_model_evaluation_create(cs, args):
    """Create a model_evaluation."""
    model_evaluation = json.loads(args.json.read())

    _filter_call_args(model_evaluation, cs.model_evaluations.create)
    _show_dict(cs.model_evaluations.create(**model_evaluation))


@utils.arg('id',
           metavar='<model_evaluation_id>',
           help='ID of the model_evaluation to delete.')
def do_model_evaluation_delete(cs, args):
    """Delete a model_evaluation."""
    cs.model_evaluations.delete(args.id)


#
# Learnings
# ~~~~~~~~
# learning-list
#
# learning-show <learning_id>
#
# learning-create [--json <file>]
#
# learning-delete <learning_id>
#

def do_learning_list(cs, args):
    """Print a list of available learnings."""
    learnings = cs.learnings.list()

    columns = ('id',
               'name',
               'status',
               'args',
               'stdout')
    utils.print_list(learnings, columns)


@utils.arg('id',
           metavar='<learning_id>',
           help='ID of the learning to show.')
def do_learning_show(cs, args):
    """Show details of a learning."""
    learning = cs.learnings.get(args.id)
    _show_dict(learning)


@utils.arg('--json',
           default=sys.stdin,
           type=argparse.FileType('r'),
           help='JSON representation of learning.')
def do_learning_create(cs, args):
    """Create a learning."""
    learning = json.loads(args.json.read())

    _filter_call_args(learning, cs.learnings.create)
    _show_dict(cs.learnings.create(**learning))


@utils.arg('id',
           metavar='<learning_id>',
           help='ID of the learning to delete.')
def do_learning_delete(cs, args):
    """Delete a learning."""
    cs.learnings.delete(args.id)
