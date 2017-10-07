

import logging

class htmlColorFormatter(logging.Formatter):
    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        self.original_fmt = fmt
        logging.Formatter.__init__(self, fmt)
        self.err_fmt = '<p style="color:red">' + self.original_fmt + '</p>'
        self.warn_fmt = '<p style="color:yellow">' + self.original_fmt + '</p>'
        self.info_fmt = '<p style="color:white">' + self.original_fmt + '</p>'

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.WARNING:
            self._fmt = self.warn_fmt

        elif record.levelno == logging.INFO:
            self._fmt = self.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = self.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result