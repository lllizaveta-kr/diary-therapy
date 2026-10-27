import logging


def setup_logging():
    # Настраиваем основной логгер для нашего приложения
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

    logging.getLogger('mysql.connector').setLevel(logging.WARNING)