import logging
import sys

from . import hooks
from .context import EventContext
from .client import ContextClient

ctx: EventContext = EventContext()

logging.getLogger().setLevel(logging.DEBUG)
context_log = logging.getLogger("discord.ext.context")
context_log.setLevel(logging.INFO)


# set log formatting
log_format = logging.Formatter(
    '%(asctime)s %(name)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
    '%(message)s',
    datefmt="[%d/%m/%Y %H:%M]"
)

# create console handler
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(log_format)
context_log.addHandler(console)
