import importlib

from django.apps import AppConfig


class DatasetConfig(AppConfig):
    name = 'dataset'

    def ready(self):
        post_delete_question = getattr(importlib.import_module("dataset.signals"), "post_delete_question")
        post_delete_answer = getattr(importlib.import_module("dataset.signals"), "post_delete_answer")
