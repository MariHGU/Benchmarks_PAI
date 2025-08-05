import albumentations as A
from albumentations.pytorch import ToTensorV2
   
def apply_augmentation(image):
    transform = A.Compose([
        A.Rotate(limit=30, p=0.5),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        ToTensorV2()
    ])
    
    return transform(image=np.array(image))["image"]