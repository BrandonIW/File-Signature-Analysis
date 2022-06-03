import binascii
import logging
import os
import sqlite3

from logging.handlers import RotatingFileHandler


def main():
    logger = _build_logger()
    _build_sql_db(logger)
    _parse_sigs(logger)

    while True:
        if _detect_signature(logger):
            logger.info("Success. Signature is a match")
            print("Success. Signature is a match. See log for details")
        else:
            logger.warning("Failure. Signature does not match")
            print("Failure. Signature does not match. See log for details")

        choice = input("Do you want to analyze another image? [Y/N]: ").lower()
        while choice not in ["y", "yes", "n", "no"]:
            choice = input("Invalid input. Scan analyze another image? [Y/N]: ").lower()

        if choice in ["y", "yes"]:
            continue
        print("Exiting program...")
        break


def _build_sql_db(logger):
    conn = sqlite3.connect("..\File Sig DB\\filesig.db")
    sql_cursor = conn.cursor()

    try:
        sql_cursor.execute("""                 
                       CREATE TABLE filesig(
                       sig TEXT,
                       ext TEXT);
                       """)
        logger.info("Successfully Created SQLite DB")

    except sqlite3.OperationalError:
        logger.warning("SQLite DB already exists")

    conn.commit()
    conn.close()


def _add_entry_sql_db(sig, ext):
    conn = sqlite3.connect("..\File Sig DB\\filesig.db")
    sql_cursor = conn.cursor()

    with conn:
        sql_cursor.execute("INSERT INTO filesig VALUES (?, ?)",
                           (sig, ext))


def _get_sig(ext):
    conn = sqlite3.connect("..\File Sig DB\\filesig.db")
    sql_cursor = conn.cursor()

    with conn:
        sql_cursor.execute("SELECT sig FROM filesig WHERE ext = ?", (ext,))
        return sql_cursor.fetchone()[0]


def _detect_signature(logger):
    file_path = input("Input path to file we will check: ")
    file_path = _validate_file(file_path, logger)
    file_ext = os.path.splitext(file_path)[1]

    try:
        signature = _get_sig(file_ext)
        return True if _file_signature_analysis(logger, signature, file_path) else False

    except TypeError:
        logger.warning(f"{file_ext} Could not perform analysis because {file_ext} is not inside the SQLite DB. "
                       f"Check DB and add entry for the signature/ext")
        return False


def _file_signature_analysis(logger, sig, file_path):
    with open(file_path, 'rb') as file:
        content = file.read()

    file_sig = binascii.hexlify(content)[:len(sig)].decode()
    logger.info(f"Expected File Signature: {sig} | Received File's Signature: {file_sig}")

    return True if file_sig.lower() == sig.lower() else False


def _parse_sigs(logger):
    """ Open up the local database of file signature/extension pairs and load them as a dictionary """
    file_sig_db = input("Input path to the local signature database: ")
    file_sig_db = _validate_file(file_sig_db, logger)

    try:
        with open(file_sig_db, 'r') as file:
            for line in file.readlines():
                ext, sig = line.strip("\n").split(" ")
                _add_entry_sql_db(sig, ext)
        logger.info("Successfully processed file signature database")

    except ValueError:
        logger.error(f"Failed to process File Sig Database. Not enough values to unpack")


def _build_logger():
    """ Build a logger for the program """
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler_info = RotatingFileHandler('../logs/FileSig.log', maxBytes=1048576)
    file_handler_info.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s || %(levelname)s || %(message)s || %(name)s')
    file_handler_info.setFormatter(formatter)
    logger.addHandler(file_handler_info)

    return logger


def _validate_file(filepath, logger):
    while not os.path.isfile(filepath):
        filepath = input("Cannot find file. Try again: ")
        logger.warning(f"Could not find file path of {filepath}")
    return filepath


if __name__ == "__main__":
    main()
