from masonite.providers import (
    RouteProvider,
    FrameworkProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    SessionProvider,
    QueueProvider,
    CacheProvider,
    EventProvider,
    StorageProvider,
    HelpersProvider,
    BroadcastProvider,
    AuthenticationProvider,
)
from masoniteorm.providers import ORMProvider

# register local package
from src.masonite.backups import BackupsProvider

PROVIDERS = [
    FrameworkProvider,
    HelpersProvider,
    RouteProvider,
    ViewProvider,
    WhitenoiseProvider,
    ExceptionProvider,
    MailProvider,
    SessionProvider,
    CacheProvider,
    QueueProvider,
    EventProvider,
    StorageProvider,
    BroadcastProvider,
    AuthenticationProvider,
    ORMProvider,
    BackupsProvider,
]
