import os
import sys

import inject

from liexpress.domain.ports import Repository


def dev_config(binder):
    from liexpress.adapters.data_provider.in_memory import InMemoryRepository

    binder.bind(Repository, InMemoryRepository())


def configure_inject():
    env = os.environ.get("ENV", "dev")
    config_name = f"{env.lower()}_config"
    this_module = sys.modules[__name__]
    config_fn = getattr(this_module, config_name)
    inject.configure_once(config_fn)
