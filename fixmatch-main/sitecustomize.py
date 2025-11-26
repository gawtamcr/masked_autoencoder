"""
Compatibility shim for NumPy 2.x removing ``numpy.lib.arraysetops``.

Some dependencies still import ``numpy.lib.arraysetops`` directly. NumPy now
exposes the implementation as ``numpy.lib._arraysetops_impl`` instead, so we
create a small module that forwards the public symbols to keep those imports
working without pinning an older NumPy version.
"""
import sys
import types

import numpy as np


def _install_arraysetops_shim() -> None:
    """Register numpy.lib.arraysetops if the module is missing."""
    if "numpy.lib.arraysetops" in sys.modules:
        return

    import numpy.lib as nplib
    import numpy.lib._arraysetops_impl as impl

    shim = types.ModuleType("numpy.lib.arraysetops")
    for name in dir(impl):
        if name.startswith("_"):
            continue
        setattr(shim, name, getattr(impl, name))

    sys.modules["numpy.lib.arraysetops"] = shim
    # Attach as an attribute for callers doing ``np.lib.arraysetops``.
    setattr(nplib, "arraysetops", shim)


_install_arraysetops_shim()
