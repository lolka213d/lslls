from bot import Bot
import logging
from config.config import LOGGING_LEVEL

# Configure logging
logging.basicConfig(
    level=LOGGING_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting bot...")
        bot = Bot()
        bot.run()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise e

if __name__ == "__main__":
    main()
