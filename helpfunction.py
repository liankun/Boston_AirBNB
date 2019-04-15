import pandas as pd
import numpy as np

def city_map(city):
    #some city names are the same
    #this function map them to the 
    #same city
    names_map={'ROXBURY CROSSING':'Roxbury Crossing','Jamaica Plain, Boston':'Jamaica Plain','Boston, Massachusetts, US':'Boston',
              'Jamaica Plain ':'Jamaica Plain','ALLSTON':'Allston','South End, Boston':'South End Boston','Boston ':'Boston',
              'Roslindale, Boston':'Roslindale','Jamaica plain ':'Jamaica Plain','dorchester, boston ':'Dorchester',
              'Boston (Charlestown)':'Charlestown','Brighton ':'Brighton','Jamaica Plain, MA':'Jamaica Plain',
               'Boston (Jamaica Plain)':'Jamaica Plain','波士顿':'Boston','boston':'Boston','Jamaica Plain (Boston)':'Jamaica Plain'}
    if city in names_map:
        return names_map[city]
    else: 
        return city

def dollar_to_float(d):
    #transform $??? to 
    #the float
    if d=='nan':
        return np.nan
    res = ""
    for s in d:
        if s !='$' and s !=',':
            res += s
    return float(res)

def clean_list_data(df_org):
    #only for the selected features
    #input: listing data
    #output: data after cleaning
    #will perform data cleaning and 
    #engeerning
   
    feature_list=['neighbourhood','neighbourhood_cleansed','city','longitude','latitude',
              'is_location_exact','property_type','room_type','accommodates','bathrooms','beds',
             'bed_type','amenities','cleaning_fee','guests_included','extra_people',
              'availability_30','availability_365','number_of_reviews','instant_bookable','cancellation_policy',
             'require_guest_profile_picture','require_guest_phone_verification','calculated_host_listings_count',
             'reviews_per_month','price']

    df = df_org[feature_list].copy()
    #numerical features
    print("process numerical features")
    #beds:
    df['has_beds'] = df['beds'].notnull()
    #bathrooms
    df['has_bathrooms'] = df['bathrooms'].notnull()
    #review per month
    df['has_reviews_per_month'] = df['reviews_per_month'].notnull()

    #none numerical features
    print("process none numerical features")
    #neighbourhood
    df = pd.get_dummies(data=df,columns=['neighbourhood'],prefix='neighborhood')

    #neighbourhood_cleansed
    df = pd.get_dummies(data=df,columns=['neighbourhood_cleansed'],prefix='neighbourhood_cleansed',drop_first=True)
   
    #clean city

    df['city'] = df['city'].apply(city_map)

    df = pd.get_dummies(data=df,columns=['city'],prefix='city')

    #is_location_exact
    df['is_location_exact']=df['is_location_exact'].map({'t':True,'f':False})

    #property_type
    df = pd.get_dummies(data=df,columns=['property_type'],prefix='property_type')

    #room_type
    df = pd.get_dummies(data=df,columns=['room_type'],prefix='room_type',drop_first=True)

    #bed_type
    df = pd.get_dummies(data=df,columns=['bed_type'],prefix='bed_type',drop_first=True)

    #amenity
    amenity_list=[]
    for s_l in df['amenities'].values:
        for s in s_l[1:-1].split(','):
            amenity_list.append(s.replace('"',''))
    amenity_set = set(amenity_list)
    amenity_set.remove('')
    #add a new coloumn
    for t in amenity_set:
        df[t] = False
    nrows = df.shape[0]

    #set value according to amenity
    for a in amenity_set:
        for ir in range(nrows):
            if a in df['amenities'][ir]:
                df.loc[ir,a] = True
    
#    print("cleaning_fee")
    #cleaning_fee and create new columns for NaN
    df['cleaning_fee'] = df['cleaning_fee'].astype('str')
    df['cleaning_fee']=df['cleaning_fee'].apply(dollar_to_float)

    df['has_cleaning_fee'] = df['cleaning_fee']>0

    #extra_people
    df['extra_people'] = df['extra_people'].apply(dollar_to_float)
    
    #instant_bookable
    df['instant_bookable']=df['instant_bookable'].map({'f':False,'t':True})

    #cancellation policy
    df = pd.get_dummies(data=df,columns=['cancellation_policy'],prefix='cancel',drop_first=True)

    df['require_guest_profile_picture']=df['require_guest_profile_picture'].map({'f':False,'t':True})

    #price
    df['price'] = df['price'].astype('str')
    df['price'] = df['price'].apply(dollar_to_float)

    return df


