# -*- coding: utf-8 -*-
import os

import yaml

local_env_path = os.path.join(os.path.dirname(__file__), ".env.yaml")

if os.path.exists(local_env_path):
    with open(local_env_path) as fl:
        os.environ.update(yaml.load(fl) or {})

if os.environ.get("PROJECT_ENV") == "production":
    from .prod import ProdConfig as config
elif os.environ.get("PROJECT_ENV") == "staging":
    from .staging import StagingConfig as config
else:
    from .dev import DevConfig as config
