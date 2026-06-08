"""
The ICARUS Complex System Core.

Drivers
-------
The `drivers` directory manages system drivers, like ... .

Engines
-------
The `engines` directory contains the three main systems of ICARUS. These are the communicative, intent, and execution engines.

Models
------
The `models` directory manages system models, like speech models and LLMs.

Utilities
---------
The `utilities` directory manages system utilities and dependencies.
"""

import drivers, utilities

from engines import intent_engine, execution_engine, communicative_engine

__all__ = ["drivers", "engines", "models", "utilities"]