"""
input_catalog_reader
"""
import os
import re
import warnings
import numpy as np
import tables
import pandas as pd
import matplotlib.pyplot as plt
from GCR import BaseGenericCatalog
from pandas.util.testing import assert_frame_equal

__all__ = ['InputCatalogReader']

class InputCatalogReader(BaseGenericCatalog):
    
    def _subclass_init(self, **kwargs):
        #fileName = '/global/projecta/projectdirs/lsst/groups/SSim/DC2/reference_catalogs/dc2_reference_catalog_dc2v3_fov4.txt'
        fileName = '/global/homes/b/bhairav/dc2_test.txt'
        self._file = fileName
        self._quantity_modifiers = {
            'uniqueId' : 'uniqueId',
            'ra' : 'raJ2000',
            'dec' : 'decJ2000',
            'sigma_ra' : 'sigma_raJ2000',
            'sigma_dec' : 'sigma_decJ2000',
            'ra_smeared' : 'raJ2000_smeared',
            'dec_smeared' : 'decJ2000_smeared',
            'lsst_u' : 'lsst_u',
            'sigma_lsst_u' : 'sigma_lsst_u',
            'lsst_g' : 'lsst_g',
            'sigma_lsst_g' : 'sigma_lsst_g',
            'lsst_r' : 'lsst_r',
            'sigma_lsst_r' : 'sigma_lsst_r',
            'lsst_i' : 'lsst_i',
            'sigma_lsst_i' : 'sigma_lsst_i',
            'lsst_z' : 'lsst_z',
            'sigma_lsst_z' : 'sigma_lsst_z',
            'lsst_y' : 'lsst_y',
            'sigma_lsst_y' : 'sigma_lsst_y',
            'lsst_u_smeared' : 'lsst_u_smeared',
            'lsst_g_smeared' : 'lsst_g_smeared',
            'lsst_r_smeared' : 'lsst_r_smeared',
            'lsst_i_smeared' : 'lsst_i_smeared',
            'lsst_z_smeared' : 'lsst_z_smeared',
            'lsst_y_smeared' : 'lsst_y_smeared',
            'isresolved' : 'isresolved',
            'isagn' : 'isagn',
            'properMotionRa' : 'properMotionRa',
            'properMotionDec' : 'properMotionDec',
            'parallax' : 'parallax',
            'radialVelocity' : 'radialVelocity'
        }
        self.Nlines=10000
        
        self.native_quantities = ['uniqueId', 'raJ2000', 'decJ2000', 'sigma_raJ2000', 'sigma_decJ2000', 
                                  'raJ2000_smeared', 'decJ2000_smeared', 'lsst_u', 'sigma_lsst_u', 
                                  'lsst_g', 'sigma_lsst_g', 'lsst_r', 'sigma_lsst_r', 'lsst_i', 'sigma_lsst_i', 
                                  'lsst_z', 'sigma_lsst_z', 'lsst_y', 'sigma_lsst_y', 'lsst_u_smeared', 
                                  'lsst_g_smeared', 'lsst_r_smeared', 'lsst_i_smeared', 'lsst_z_smeared', 
                                  'lsst_y_smeared', 'isresolved', 'isagn', 'properMotionRa', 'properMotionDec', 
                                  'parallax', 'radialVelocity']
        self.name2ndx = {}
        self.names = []
                
        for i,n in enumerate(self.native_quantities):
            self.name2ndx[n]=i
            
    def _iter_native_dataset(self, native_filters = None):
        assert (native_filters is None)
        with open(self._file, 'r') as f:
            for i in range(11):
                f.readline()
            while True:
                l=[]
                for c in range(self.Nlines):
                    line = f.readline()
                    if len(line) == 0:
                        break
                    values = [float(x) for x in line.split(', ')]
                    l.append(values)
                if len(l)>0:
                    values=np.array(l)
                else:
                    return                      
                
                def native_quantity_getter(native_quantity):
                    res=np.array([values[:,self.name2ndx[native_quantity]]])
                    #print(res)
                    return res.flatten()
                yield native_quantity_getter
        
    
    def _generate_native_quantity_list(self, native_filters = None):
        with open(self._file, 'r') as f:
            # skip 10 lines
            for i in range(10):
                f.readline()
            # elenveth line is fields
            fields = f.readline()
            fields = fields[1:] ### get rid of the first character
            fields = fields.split(', ')
            fields[len(fields) - 1] = fields[len(fields) - 1].strip()
            fieldsData = pd.DataFrame({'data':fields})
            nativeQuantData = pd.DataFrame({'data':self.native_quantities})
        #assert fields == self.native_quantities, "The lists are not equal."
        #print(assert all([a == b for a, b in zip(fields, self.native_quantities)]))
        #for n1,n2 in zip(fields, self.native_quantities):
        #assert(n1 == n2)
        try:
            assert_frame_equal(fieldsData.sort_index(axis=1), nativeQuantData.sort_index(axis=1), check_names=True)
            print("Both frames are equal.")
        except:
            print("Both frames are not equal.")
        return self.native_quantities
    