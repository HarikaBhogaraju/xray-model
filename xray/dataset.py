import os

import pandas as pd
import torch
import torchvision.transforms as transforms
from PIL import Image as Im
from torch.utils.data import Dataset


class XrayImageDataset(Dataset):
    def __init__(self, annotations_file, img_dir, test_data=False):
        self.img_labels = pd.read_csv(annotations_file, dtype={'ImageId': str, 'Label': int})
        self.img_dir = img_dir
        self.test_data = test_data
        self.transform = transforms.Compose(
            [
                # transforms.ToPILImage(),
                # transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ])

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0] + ".png")
        image = Im.open(img_path).convert('RGB')
        image = self.transform(image)
        label = self.img_labels.iloc[idx, 1]
        if self.test_data:
            return self.img_labels.iloc[idx, 0], image
        else:
            return image, torch.tensor(label)
