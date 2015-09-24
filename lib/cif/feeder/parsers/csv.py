__author__ = 'James DeVincentis <james.d@hexhost.net>'

import csv

from ..parser import Parser


class Csv(Parser):
    def __init__(self):
        self.csv = csv.reader(self.file)

    def parsefile(self, filehandle, max_objects=1000):
        """Parse file provided by `filehandle`. Return `max_objects` at a time. This is repetitively called

        :param filehandle: Open text mode filehandle object pointing to the file to be parsed.
        :param int max_objects: Number of objects to return
        :return: List of parsed observables
        :rtype: list
        """

        self.loadjournal()

        observables = []

        if self.total_objects == 0 and "start" in self.parsing_details and self.parsing_details["start"] > 0:
            for x in range(1, self.parsing_details["start"]+1):
                try:
                    next(self.csv)
                    self.total_objects += 1
                except:
                    self.parsing = False
                    return observables

        objects = 0
        while objects < max_objects:

            try:
                line = next(self.csv)
            except StopIteration:
                self.parsing = False
                break

            if len(line) != self.valuecount:
                self.logging.warning("No Match - contents: '{0}'; match-count: {2}; values: {1}".format(
                    line, len(self.parsing_details["values"]), len(line))
                )
                continue

            observable = self.create_observable_from_meta_if_not_in_journal(line)
            if observable is not None:
                observables.append(observable)
                objects += 1
                self.total_objects += 1

            if self.ending and self.total_objects >= self.end:
                self.parsing = False
                break

        self.writejournal()

        return observables
