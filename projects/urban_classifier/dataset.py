'''
    2022 Benjamin Kellenberger, Tiziana Gelmi-Candusso
'''

import os
import json
from torch.utils.data import Dataset
from torchvision.transforms import Compose, Resize, ToTensor
from PIL import Image
import pandas as pd



class CTDataset(Dataset):

    def __init__(self, cfg, split='train', split_type = 'split_by_loc'):
        '''
            Constructor. Here, we collect and index the dataset inputs and
            labels.
        '''
        self.data_root = cfg['data_root']
        self.split = split
        self.split_type = split_type
        self.transform = Compose([              # Transforms. Here's where we could add data augmentation (see Björn's lecture on August 11).
            Resize((cfg['image_size'])),        # For now, we just resize the images to the same dimensions...
            ToTensor()                          # ...and convert them to torch.Tensor.
        ])
        
        # index data into list
        self.data = []
        #dict categories
        cat_csv = pd.read_csv(os.path.join(self.data_root, 'categories.csv')) #this could go into the cfg file
        species_idx = cat_csv['class'].to_list()
        species = cat_csv['description'].to_list()
        self.species_to_index_mapping = dict(zip(species, species_idx))

        #load the train file
        f = open(os.path.join(self.data_root, self.split_type.lower(), self.split.lower()+'.txt'), 'r') 
        lines = f.readlines() # load all lines

        for line in lines: # loop over lines
            file_name = line.strip().replace("\\", "/")
            sp = os.path.split(file_name)[0]
            # print(file_name)
            # print(os.path.split(file_name))
            
            # if not, add it and assign an index
            species_idx = self.species_to_index_mapping[sp]
            self.data.append([file_name, species_idx])


    def __len__(self):
        '''
            Returns the length of the dataset.
        '''
        return len(self.data)

    
    def __getitem__(self, idx):
        '''
            Returns a single data point at given idx.
            Here's where we actually load the image.
        '''
        image_path, label = self.data[idx]              # see line 57 above where we added these two items to the self.data list

        # load image
        image_path = os.path.join(self.data_root, 'crops', image_path)
        img = Image.open(image_path).convert('RGB')     # the ".convert" makes sure we always get three bands in Red, Green, Blue order

        # transform: see lines 31ff above where we define our transformations
        img_tensor = self.transform(img)

        return img_tensor, label

# %%
