"""
DEPRECATED.
This module is not used.
Kept for historical reference only.
"""

from typing import Dict, Any


class ProviderSchema:
    def __init__(
        self,
        request_builder,
        response_parser,
    ):
        self.request_builder = request_builder
        self.response_parser = response_parser
