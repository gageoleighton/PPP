from fbs_runtime import PUBLIC_SETTINGS
from fbs_runtime.application_context.PySide6 import ApplicationContext
from fbs_runtime.application_context import cached_property, is_frozen
from fbs_runtime.excepthook.sentry import SentryExceptionHandler
from perseverance import Perseverance

class AppContext(ApplicationContext):
    @cached_property
    def exception_handlers(self):
        result = super().exception_handlers
        if is_frozen():
            result.append(self.sentry_exception_handler)
        return result
    
    @cached_property
    def sentry_exception_handler(self):
        return SentryExceptionHandler(
            PUBLIC_SETTINGS['sentry_dsn'],
            PUBLIC_SETTINGS['version'],
            PUBLIC_SETTINGS['environment'],
            callback=self._on_sentry_init
        )
    def _on_sentry_init(self):
        scope = self.sentry_exception_handler.scope
        from fbs_runtime import platform
        scope.set_extra('os', platform.name())

context = AppContext()
preserves = Perseverance()