import pandas 
import numpy

def PairMatchWithPosition(table1, table2, t1_ra_name, t1_dec_name, 
                          t2_ra_name, t2_dec_name, output_file_name,how,
                         thres_dist = 1/3600):
# Input: 
#         1. table1, table2: pandas table1 and pandas table2;
#         2. t1_ra_name, t1_dec_name, t2_ra_name, t2_dec_name : (strs) columns names of 
#         ra and dec in two tables
#         3. output_file_name: (strs) the name of the output merged file you want to save
#         4. how: 'inner' take the intersection and 'outer' take the union set.
#         5. thres_dist: the maximun distance that you think they are the same source, the
#         default value is 1 arcsec.

# Output:
#         Merged table with only 'one' columns ra and dec named as 'RA' and 'DEC'. There 
#         also a additonal column named 'name' that you can ignore.

# Key updata: 
#         Other tools to pair match like pd.merge and topcat can not merge the position
#         information so that you can not further cross match with other tables because
#         the merged tables have two columns positons that did not merged to one columns.



    table1['name'] = np.arange(len(table1))
    table2['name'] = -9999
    for i in range(len(table1)):
        new_dataframe = pd.DataFrame([])
        dist = ((table1['%s' %t1_ra_name][i] - table2['%s' %t2_ra_name])**2 + 
                (
                    table1['%s' %t1_dec_name][i] - table2['%s' %t2_dec_name])**2) ** 0.5
        min_dist = np.min(dist)
        if min_dist <= thres_dist:
            index = dist.argmin()
            table2.loc[index,'name'] = i
    
    if t1_ra_name == t2_ra_name:
        t1_ra_name = t1_ra_name + '_x'
        t2_ra_name = t2_ra_name + '_y'
        
    if t1_dec_name == t2_dec_name:
        t1_dec_name = t1_dec_name + '_x'
        t2_dec_name = t2_dec_name + '_y'
            
    if how == 'outer':
        new_table = pd.merge(table1,table2,on='name',how='outer') 
    elif how == 'inner':
        new_table = pd.merge(table1,table2,on='name',how='inner') 

    new_table['RA_Merge'] = new_table[['%s' %t1_ra_name,'%s' %t2_ra_name]].median(axis=1)
    new_table['DEC_Merge'] = new_table[['%s' %t1_dec_name,'%s' %t2_dec_name]].median(axis=1)
    new_table.drop(['%s'%t1_ra_name, '%s'%t2_ra_name, '%s'%t1_dec_name, '%s'%t2_dec_name]
                   , axis=1, inplace=True)
    
    new_table.to_csv('%s' %output_file_name,index=None)
    return new_table
