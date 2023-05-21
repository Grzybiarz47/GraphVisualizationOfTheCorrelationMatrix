import pandas as pd
import numpy as np
import glob
import settings

class DataFrameHandler:
    di = dict()
    picked = dict()
    sector = dict()

    def read(self, path, picked_column="Close"):
        all_files = glob.glob(path + "/*.csv")
        settings.n = len(all_files)
        settings.column_names = []
        self.sector = dict()
        self.picked = dict()
        self.di = dict()
        
        for filename in all_files:
            df = pd.read_csv(filename, index_col=None, header=0)
            df = self.__renameColumns(df)

            df['Date'] = pd.to_datetime(df['Date'])
            df.sort_values(by='Date', inplace = True)
            df = df.reset_index(drop=True)

            df = self.__clearDataFrame(df)

            df[picked_column + 'Diff'] = np.log(df[picked_column]) - np.log(df[picked_column].shift(1))

            filename = filename.replace("\\", "/")
            name = filename.split("/")[-1].split(".")[0].upper()
            name_elems = name.split("_")
            column_name = name_elems[0]
            if len(name_elems) > 1:
                self.sector[column_name] = name_elems[1]
            else:
                self.sector[column_name] = "OTH"

            settings.column_names.append(column_name)
            self.picked[column_name] = df[picked_column + 'Diff'][1:].reset_index(drop=True)
            self.di[column_name] = df[['Open', 'High', 'Close', 'Low']]
            self.di['Date'] = df['Date'][1:].reset_index(drop=True)

        settings.column_names.sort()
        cdf = pd.DataFrame(self.picked)
        cdf = cdf[settings.column_names]

        print(cdf.shape[0])
        print(settings.n)
        return cdf
    
    def getDates(self):
        return self.di['Date']
    
    def getSectors(self):
        return self.sector

    def __clearDataFrame(self, df):
        # remove commas
        df['Close'] = df['Close'].astype(str).apply(lambda x: x.replace(',', '.'))
        df['Open'] = df['Open'].astype(str).apply(lambda x: x.replace(',', '.'))
        df['Low'] = df['Low'].astype(str).apply(lambda x: x.replace(',', '.'))
        df['High'] = df['High'].astype(str).apply(lambda x: x.replace(',', '.'))
        df['Volume'] = df['Volume'].astype(str).apply(lambda x: x.replace(',', '.'))

        # remove dolar mark
        df['Close'] = df['Close'].apply(lambda x: x.replace('$', ''))
        df['Open'] = df['Open'].apply(lambda x: x.replace('$', ''))
        df['Low'] = df['Low'].apply(lambda x: x.replace('$', ''))
        df['High'] = df['High'].apply(lambda x: x.replace('$', ''))
        
        # cast to float
        df['Close'] = df['Close'].str[:].astype(float)
        df['Open'] = df['Open'].str[:].astype(float)
        df['Low'] = df['Low'].str[:].astype(float)
        df['High'] = df['High'].str[:].astype(float)
        return df
    
    def __renameColumns(self, df):
        df.rename(columns = {'Data':'Date', 
                            'Otwarcie':'Open', 
                            'Najwyzszy':'High',
                            'Najnizszy':'Low',
                            'Zamkniecie':'Close',
                            'Wolumen':'Volume'}, inplace=True)
        df.rename(columns = {'Close/Last':'Close'}, inplace=True)
        return df