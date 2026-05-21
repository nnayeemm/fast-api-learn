import logging
import ex
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,        
    format='%(asctime)s | %(name)s | %(lineno)d | %(levelname)-8s - %(message)s',
       datefmt='%d-%m-%Y %I:%M:%S %p',
       handlers=[console_handler, file_handler]
)

# Create logger object
logger = logging.getLogger("myApp")


# Example functions
def login(username):
    logger.info(f"{username} logged in successfully")


def divide(a, b):
    logger.debug(f"Dividing {a} by {b}")

    try:
        result = a / b
        logger.info(f"Result of dividing {a} by {b} = {result}")
        return result

    except ZeroDivisionError:
        logger.error("Cannot divide by zero")


def check_disk_space(space):
    if space < 20:
        logger.warning("Disk space is running low")


def connect_database():
    logger.critical("Database connection failed")


# Calling functions
login("Nayeem")

divide(10, 2)

divide(10, 0)

check_disk_space(10)

connect_database()
print(__name__)