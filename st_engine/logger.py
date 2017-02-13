done = False
def setup():
    global done
    if done:
        return
    import os
    if os.environ.get("sentry"):
        import logging
        from raven.handlers.logging import SentryHandler
        handler = SentryHandler(os.environ.get("sentry"), level=logging.INFO)
        from raven.conf import setup_logging
        setup_logging(handler)
        root = logging.getLogger()
        root.setLevel(logging.INFO)
    done = True
