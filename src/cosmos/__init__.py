from .logging import log
from inspect import trace
import os
import os.path
import traceback
from subprocess import check_output

try:
    VERSION = __import__("pkg_resources").get_distribution("cosmos").version
except Exception:
    VERSION = "unknown"

# fix is in the works see: https://github.com/mpdavis/python-jose/pull/207
import warnings

warnings.filterwarnings("ignore", message="int_from_bytes is deprecated")


def _get_git_revision(path):
    if not os.path.exists(os.path.join(path, ".git")):
        return None
    try:
        revision = check_output(["git", "rev-parse", "HEAD"], cwd=path, env=os.environ)
    except Exception:
        # binary didn't exist, wasn't on path, etc
        return None
    return revision.decode("utf-8").strip()


def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    if "COSMOS_BUILD" in os.environ:
        return os.environ["COSMOS_BUILD"]
    package_dir = os.path.dirname(__file__)
    checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir, os.pardir))
    path = os.path.join(checkout_dir)
    if os.path.exists(path):
        return _get_git_revision(path)
    return None


def get_version():
    if __build__:
        return f"{__version__}.{__build__}"
    return __version__


def is_docker():
    # One of these environment variables are guaranteed to exist
    # from our official docker images.
    # DISPATCH_VERSION is from a tagged release, and DISPATCH_BUILD is from a
    # a git based image.
    return "COSMOS_VERSION" in os.environ or "COSMOS_BUILD" in os.environ


__version__ = VERSION
__build__ = get_revision()
