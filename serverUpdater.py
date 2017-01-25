#!/usr/bin/env python

import sys
import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    loggers = {
        '': {'handlers': ['h'],
	     'level': logging.DEBUG}
        }
)

dictConfig(logging_config)

from PySide.QtCore import QObject, QCoreApplication
from PySide import QtNetwork,QtSql

from passwords import DB_SERVER, DB_PORT, DB_LOGIN, DB_PASSWORD, DB_NAME

#update server
from updater.updateServer import *

UNIT16 = 8

class start(QObject):

    def __init__(self, parent=None):
        try:
            super(start, self).__init__(parent)
            self.logger = logging.getLogger()

            self.logger.info("Update server starting")
            self.db = QtSql.QSqlDatabase("QMYSQL")
            self.db.setHostName(DB_SERVER)
            self.db.setPort(DB_PORT)

            self.db.setDatabaseName(DB_NAME)
            self.db.setUserName(DB_LOGIN)
            self.db.setPassword(DB_PASSWORD)
            self.db.setConnectOptions("MYSQL_OPT_RECONNECT=1")

            if not self.db.open():
                self.logger.error(self.db.lastError().text())

            else:
                self.logger.info("DB opened.")

            self.updater = updateServer(self)
            if not self.updater.listen(QtNetwork.QHostAddress.Any, 9001):

                self.logger.error("Unable to start the server")

                return
            else:
                self.logger.info("Starting the update server on  %s:%i" % (self.updater.serverAddress().toString(),self.updater.serverPort()))
        except Exception as e:
            self.logger.exception("Error: %r" % e)

if __name__ == '__main__':
    print("Running updater server")
    logger = logging.getLogger()
    import sys

    try:

        app = QCoreApplication(sys.argv)
        server = start()
        app.exec_()
        print("Shutting down")

    except Exception as e:

        logger.exception("Error: %r" % e)
        logger.debug("Finishing main")

