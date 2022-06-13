#!/usr/bin/env python3
import pandas as pd
import os

default_kwargs = {
    'sep': ';',
    'quotechar': '"',
}
def process_caracs_pre_2019(caracs: pd.DataFrame) -> pd.DataFrame:
    caracs[['lat','long']] /= 100_000
    return caracs

sources = {
    '2020': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/78c45763-d170-4d51-a881-e3147802d7ee',
            'opts': {**default_kwargs}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/07a88205-83c1-4123-a993-cba5331e8ae0',
            'opts': {
                **default_kwargs,
                'decimal': ','
            }
        }
    },
    '2019': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/36b1b7b3-84b4-4901-9163-59ae8a9e3028',
            'opts': {**default_kwargs}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a',
            'opts': {
                **default_kwargs,
                'decimal': ','
            }
        }
    },
    '2018': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2017': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/07bfe612-0ad9-48ef-92d3-f5466f8465fe',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2016': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/e4c6f4fe-7c68-4a1d-9bb6-b0f1f5d45526',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/96aadc9f-0b55-4e9a-a70e-c627ed97e6f7',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2015': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/b43a4237-9359-4217-b833-8d3dc29a6c24',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/185fbdc7-d4c5-4522-888e-ac9550718f71',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2014': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/457c10ff-ea6c-4238-9af1-d8dc62b896d4',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/85dfe8c6-589f-4e76-8a07-9f59e49ec10d',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2013': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/af4349c5-0293-4639-8694-b8b628bfc6c3',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/18b1a57a-57bf-4bf1-b9ee-dfa5a3154225',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2012': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/a19e060e-1c18-4272-ac4e-d4745ab8fade',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/b2518ec1-6529-47bc-9d55-40e2effeb0e7',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2011': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/bd946492-31b3-428e-8494-a1e203bdc9cc',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/37991267-8a15-4a9d-9b1c-ff3e6bea3625',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2010': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/c5e5664d-1483-41da-a4c6-5f1727d7a353',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/decdfe8c-38ff-4a06-b7fc-615785f2914d',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2008': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/433e26cf-d4c8-4dd9-b3f2-ecbc8a8f0509',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/722ebb99-c8b2-4635-bf8d-125dd280ee42',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2007': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/c5c30fc2-9bfd-4bcd-b45b-f01a31f1d087',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/6fc7b169-4dfe-442c-8c28-8bd773aeddf8',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2006': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/ebb4c37e-1616-497d-b5ed-f8113bed2ae7',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/fafa33cf-50cb-4092-a819-d5209f684089',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2005': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/cecdbd46-11f2-41fa-b0bd-e6e223de6b3c',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/a47866f7-ece1-4de8-8d31-3a1b4f477e08',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
}

for year, src in sources.items():
    print(f"Collecting data for {year}")
    print("Reading user data...")
    usagers = pd.read_csv(src['usagers']['url'], **src['usagers']['opts'])
    print("Reading accident caracteristics data...")
    caracs = pd.read_csv(src['caracteristiques']['url'], **src['caracteristiques']['opts'])

    if 'process' in src['usagers']:
        usagers = src['usagers']['process'](usagers)

    if 'process' in src['caracteristiques']:
        caracs = src['caracteristiques']['process'](caracs)
    
    acc_grav = usagers[['Num_Acc','grav']].groupby('Num_Acc').agg('max')
    acc_caracs_grav = pd.merge(caracs, acc_grav, how='inner', on='Num_Acc')
    acc_caracs_grav['year'] = year

    # print("Writing file(s)...")
    # usagers.to_csv(f"{year}/usagers.csv", index=False)
    # caracs.to_csv(f"{year}/caracteristiques.csv", index=False)
    acg = acc_caracs_grav.drop(columns=['hrmn', 'gps', 'adr', 'com', 'atm', 'int', 'an'], errors='ignore')
    acg.to_pickle(f"acc_caracs_grav-{year}.pkl")


print()
print("Done.")
