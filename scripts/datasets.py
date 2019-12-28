from ftplib import FTP
from io import StringIO
from datetime import datetime
from abc import ABCMeta, abstractmethod
import numpy as np
import pandas as pd
from bokeh.models.sources import ColumnDataSource

class timeseries_dataset(metaclass=ABCMeta):
    #This is the abstract base class for time series datasets. They need a name, the info whether one is able to obtain
    #the data without a token or password, and whether users need to upload the file on their own
    ##TODO are there any cases I haven't thought about yet?
    ##TODO think about how to use needs_token and needs_local_dataset in the GUI
    def __init__(self, name, bool_token, bool_local):
        self.name = name ##TODO create names that are unique and userfriendly, or create userfriendly names and ids
        self.needs_token = bool_token
        self.needs_local_dataset = bool_local
        self.is_loaded = False
        self.version = None ##TODO think about how to maintain datasets

    @abstractmethod
    def get_citation(self):
        #This function must return a string that users can simply paste into their documents as correct citation
        pass

    @abstractmethod
    def load_data(self): #This function needs to load a ColumnDataSource into self.data and set self.is_loaded to true
        pass

    def __str__(self):
        return self.name


class dwd_dataset(timeseries_dataset):
    def __init__(self, init_arguments):
        self.ftp_path, self.ftp_file = init_arguments ##If more than one argument is passed, arguments need to be separated afterwards
        print(self.ftp_file)
        print(self.ftp_path)
        self.y_columns = ['y']
        self.y_labels = ['Temperature (Celsius)']
        ##TODO Especially for these datasets, make geolocation input-able and use this information to choose the
        # correct dataset

        super().__init__("Tmp_DWD", False, False)

    def load_data(self):
        month_str_to_int = {"Jan": 1, "Feb": 2, "Mrz": 3, "Apr": 4, "Mai": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
                            "Okt": 10, "Nov": 11, "Dez": 12}

        ftp = FTP("opendata.dwd.de")
        ftp.login()
        ftp.cwd(self.ftp_path)
        r = StringIO()
        def customWriter(line):
            r.write(line)
            r.write("\n")
        ftp.retrlines("RETR " + self.ftp_file, customWriter)

        labels = []
        values = []
        for i, line in enumerate(r.getvalue().split("\n")):
            if i == 0:
                tmp_labels = line.split(";")[1:]
            else:
                if len(line.split(";")) > 1:
                    labels += [np.datetime64(datetime(
                        int(line.split(";")[0]), month_str_to_int[lab.strip()], 1))
                                    for lab in tmp_labels]
                    values += [float(part) for part in line.split(";")[1:]]

        self.data = ColumnDataSource({'x': labels, 'y': values})
        self.is_loaded = True

    def get_citation(self):
        return("Deutscher Wetterdienst")


class global_carbon_project_dataset(timeseries_dataset):
    def __init__(self, gcp_global_file):
        self.gcp_global_file = gcp_global_file
        self.y_columns = ['Fossil-Fuel-And-Industry', 'Land-Use-Change-Emissions', 'Atmospheric-Growth',
                          'Ocean-Sink', 'Land-Sink', 'Budget-Imbalance']
        self.y_labels = ['Fossil-Fuel-And-Industry (Gt)', 'Land-Use-Change-Emissions (Gt)', 'Atmospheric-Growth (Gt)',
                         'Ocean-Sink (Gt)', 'Land-Sink (Gt)', 'Budget-Imbalance (Gt)']
        super().__init__("Global Carbon Budget 2019", False, False)


    def load_data(self):
        csv_data = pd.read_csv(self.gcp_global_file, error_bad_lines=False)
        csv_data.columns = ["x", 'Fossil-Fuel-And-Industry', 'Land-Use-Change-Emissions',
                                  'Atmospheric-Growth', 'Ocean-Sink', 'Land-Sink', 'Budget-Imbalance']
        csv_data["x"] = [np.datetime64(datetime(f, 1, 1)) for f in csv_data["x"]]
        self.data = ColumnDataSource(csv_data)
        self.is_loaded = True

    def get_citation(self):
        return("Global Carbon Project. (2019). Supplemental data of Global Carbon Budget 2019 (Version 1.0) [Data set]. "
               "Global Carbon Project. https://doi.org/10.18160/gcp-2019")



class data_collection(object):
    def __init__(self):
        self.datasets = []

    def add_dataset(self, new_dataset):
        #TODO this might be necessary if a user is adding its own dataset. Make this possible!
        None

    def load(self, savefile):
        for i, line in enumerate(open(savefile)):
            if len(line.strip().split("\t")) == 2:
                self.datasets.append(globals()[line.split("\t")[0]](line.strip().split("\t")[1]))
            else:
                self.datasets.append(globals()[line.split("\t")[0]](line.strip().split("\t")[1:]))


