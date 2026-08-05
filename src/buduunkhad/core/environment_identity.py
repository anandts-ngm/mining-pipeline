"""Secret-free runtime identities used to bind resumable scientific outputs."""

from __future__ import annotations

import platform
import sys
from importlib.metadata import PackageNotFoundError, version

from buduunkhad import __version__

_DISTRIBUTIONS = (
    "fiona",
    "geopandas",
    "numpy",
    "pydantic",
    "pyproj",
    "rasterio",
    "shapely",
    "whitebox",
)


def execution_environment() -> dict[str, str]:
    """Return stable software identities without paths, host names, users, or credentials."""

    values = {
        "architecture": platform.machine() or "unknown",
        "buduunkhad": __version__,
        "gdal": _module_attribute("rasterio", "__gdal_version__"),
        "geos": _module_attribute("shapely", "geos_version_string"),
        "operating_system": platform.system() or "unknown",
        "operating_system_release": platform.release() or "unknown",
        "proj": _module_attribute("pyproj", "proj_version_str"),
        "python_implementation": sys.implementation.name,
        "python_version": platform.python_version(),
    }
    for distribution in _DISTRIBUTIONS:
        values[f"package:{distribution}"] = _distribution_version(distribution)
    return dict(sorted(values.items()))


def _distribution_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not-installed"


def _module_attribute(module_name: str, attribute: str) -> str:
    try:
        module = __import__(module_name)
    except ImportError:
        return "not-installed"
    value = getattr(module, attribute, None)
    return str(value) if value else "unknown"
