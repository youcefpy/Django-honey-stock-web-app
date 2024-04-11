BOX_CONFIG = {
    '3500': {
        (0.2, 'Miel kalitus'),
        (0.2, 'Miel djabali'),
        (0.2, 'Miel djerdjir'),
    },
    '4000':{
        (0.2, 'Miel kalitus'),
        (0.2, 'Miel djabali'),
        (0.2, 'Miel djerdjir'),
        (0.01, 'propolis'),
    },
    '4500':{
        (0.2, 'Miel kalitus'),
        (0.2, 'Miel djabali'),
        (0.2, 'Miel djerdjir'),
        (0.01, 'propolis'),
    },
    '7500':{
        (0.25, 'Miel kalitus'),
        (0.25, 'Miel djabali'),
        (0.25, 'Miel djerdjir'),
        (0.25,'Miel sidr'),
        (0.1,'pollen'),
        (0.01, 'propolis'),
    },
    '8500':{
        (0.5, 'Miel orange'),
        (0.5, 'Miel djabali'),
        (0.25, 'Miel djerdjir'),
        (0.25,'Miel sidr'),
        (0.1,'pollen'),
        (0.01, 'propolis'),
    },
    '9900':{
        (0.5, 'Miel orange'),
        (0.5, 'Miel djabali'),
        (0.5, 'Miel djerdjir'),
        (0.25,'Miel sidr'),
        (0.1,'pollen'),
        (0.01, 'propolis'),
    },
}

BOX_STANDARD = {
    'coffret 3500' : {
        'standard 1' : [
            [0.2,'Miel kalitus'],
            [0.2,'Miel djerdjir'],
            [0.2,'Miel djabali'],
        ],
        'standard 2':[
            [0.2,'Miel marar'],
            [0.2,'Miel djerdjir'],
            [0.2,'Miel djabali'],
        ]
        
    },
    'coffret 4000' : {
        'standard 1' : [
            [0.20,'Miel kalitus'],
            [0.20,'Miel djerdjir'],
            [0.20,'Miel djabali'],
            [0.01,'propolis'],
        ],
        'standard 2':[
            [0.20,'Miel marar'],
            [0.20,'Miel djerdjir'],
            [0.20,'Miel djabali'],
            [0.01,'propolis'],
        ]
        
    },
      'coffret 4500' : {
        'standard 1' : [
            [0.25,'Miel kalitus'],
            [0.25,'Miel djerdjir'],
            [0.25,'Miel djabali'],
           [ 0.01,'propolis'],
        ],
        'standard 2':[
            [0.25,'Miel marar'],
            [0.25,'Miel djerdjir'],
            [0.25,'Miel djabali'],
            [0.01,'propolis'],
        ]
        
    },
}
BOX_TYPE_MAPPING = {
    '1': 'coffret 3500',
    '2': 'coffret 4000',
    '3': 'coffret 8500',
    '4': 'coffret 9900'
  };