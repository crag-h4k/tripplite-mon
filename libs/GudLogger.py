# This module is a custom logging modules for Adobe DX SecENG

import logging
import logging.handlers

from os import path


'''
levels:
    info:
    warning:
    error:
    critical:
    log:
'''
class Logger(object):
    def __init__(self, outfile, imports=[], stdout=True, rotate=True, max_log_size=2, max_backups=5):
        # set logging format
        self.fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)

        if outfile is "":
            self.outfile = path.abspath('/var/log/{}.log'.format(__file__))
        else:
            self.outfile = path.abspath(outfile)

        # for stdout, gives typical 'print() behavior'
        if stdout is True:
            self.ch = logging.StreamHandler()
            # set the level of the stdout
            self.ch.setLevel(logging.DEBUG)
            # set the format of stdout
            self.ch.setFormatter(self.fmt)
            self.logger.addHandler(self.ch)
        # set file rotation for 
        if rotate is True:
            # max size of log file before rotation, default 2 MB
            self.max_log_size = max_log_size* 10**6
            self.rt = logging.handlers.RotatingFileHandler(self.outfile,
                    maxBytes=self.max_log_size,
                    backupCount=max_backups)
            self.rt.setFormatter(self.fmt)
            self.rt.setLevel(logging.INFO)
            self.logger.addHandler(self.rt)
        else:
            self.fh = logging.FileHandler(outfile)
            # set the verbosity of output to logfile
            self.fh.setLevel(logging.INFO)
            # set location of log file
            # set the format of the log file
            self.fh.setFormatter(self.fmt)
            self.logger.addHandler(self.fh)
        # get loggers from specific modules
        if imports is not []:
            for i in imports:
                self.logging.getLogger(i).setLevel(logging.WARNING)
        #self.logging.captureWarnings(True)
        self.logger.propagate = False

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warning(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)

    def critical(self, msg, extra=None):
        self.logger.critical(msg, extra=extra)

    def exception(self, msg, extra=None):
        if type(msg) is not str:
            msg = str(msg)
        self.logger.exception(msg, extra=extra)


if __name__ == '__main__':
    from sys import argv

    outfile = argv[1]
    logger = Logger(outfile)
    square = lambda x: x**x
    x = square(2)

    logger.info('{}'.format(x))
    logger.debug('{}'.format(x))
    logger.warning('{}'.format(x))
    logger.critical('{}'.format(x))

    try:
        raise Exception
    except Exception as E:
        logger.exception('Don\'t freak out about this exception, it\'s intentional')
        logger.exception(E)

 
