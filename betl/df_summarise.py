from . import logger

JOB_LOG = logger.getJobLog()


#
# The default summarise process. This is very simple, because summaries
# have to be custom-built by the app. All this does is truncate all the
# tables when running a bulk load
#
def defaultSummarise(scheduler):

    sumLayer = scheduler.logicalDataModels['SUM']

    sumTables = sumLayer.dataModels['SUM'].tables

    if scheduler.bulkOrDelta == 'BULK':
        for tableName in sumTables:
            if (sumTables[tableName].getTableType() == 'SUMMARY'):
                # If it's a bulk load, drop facts' foreign key constraints
                # to speed up writing.
                JOB_LOG.info(
                    logger.logStepStart('Dropping fact indexes for ' +
                                        tableName))
                sumTables[tableName].dropIndexes()

                # Because it's a bulk load, clear out the data (which also
                # restarts the SK sequences).
                JOB_LOG.info(
                    logger.logStepStart('Truncating ' + tableName))
                sumTables[tableName].truncateTable()
