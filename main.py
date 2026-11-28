import asyncio
import signal

from src.core.config import Config
from src.core.logger import AppLogger


async def main() -> None:
    config = Config()
    AppLogger(config.logging, json_output=config.environment == "production")
    log = AppLogger.get(__name__).bind(service="app")
    log.info(
        "Config loaded",
        environment=config.environment,
        log_level=config.logging.level,
    )

    # Docker runs the app as PID 1, and the kernel ignores signals PID 1 does not handle
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    log.info("Starting application")
    async with asyncio.TaskGroup() as tg:
        # Code ... start long-running tasks here, and let each one return on stop
        tg.create_task(stop.wait())
    log.info("Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
