# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


source = '../source/gapdata009.xlsx'
out_dir = '../../'

# the datapoint name and datapoint id
dp_name_sheet = 'data & sources'
dp_name = 'Average age at 1st marriage (girls)'
dp_id = to_concept_id(dp_name)

if __name__ == '__main__':

    # reading data
    data001 = pd.read_excel(source, sheetname=dp_name_sheet)

    data001_dp = data001[['Country', 'Year', 'Data']].copy()
    data001_dp.columns = ['country', 'year', dp_id]

    # entities
    country = data001_dp['country'].unique()
    country_id = list(map(to_concept_id, country))
    ent = pd.DataFrame([], columns=['country', 'name'])
    ent['country'] = country_id
    ent['name'] = country
    path = os.path.join(out_dir, 'ddf--entities--country.csv')
    ent.to_csv(path, index=False)

    # datapoints
    data001_dp['country'] = data001_dp['country'].map(to_concept_id)
    path = os.path.join(out_dir, 'ddf--datapoints--{}--by--country--year.csv'.format(dp_id))
    (data001_dp.sort_values(by=['country', 'year'])
     .dropna()
     .to_csv(path, index=False, float_format='%g'))

    # concepts
    conc = [dp_id, 'country', 'year', 'name']

    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])

    cdf['concept'] = conc
    cdf['name'] = [dp_name, 'Country', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'entity_domain', 'time', 'string']

    cdf.to_csv(os.path.join(out_dir, 'ddf--concepts.csv'), index=False)

    # index
    create_index_file(out_dir)

    print('Done.')
