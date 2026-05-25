import os
import urllib.request
import zipfile
import json
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# Configuration
DATA_DIR = Path("data/potato_disease")
MODEL_DIR = Path("models/disease")
MODEL_PATH = MODEL_DIR / "model.pth"
HISTORY_PATH = MODEL_DIR / "training_history.json"
BATCH_SIZE = 16
NUM_EPOCHS = 10
LEARNING_RATE = 0.001

def ensure_dataset():
    """Checks if the dataset exists, otherwise gives instructions/downloads."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Dataset directory created at {DATA_DIR}.")
        
    # Check for subdirectories
    classes = ["Potato___Early_blight", "Potato___Late_blight", "Potato___healthy"]
    missing = [c for c in classes if not (DATA_DIR / c).exists()]
    
    if missing:
        print("!" * 80)
        print("DATASET NOT FOUND!")
        print(f"Please place the PlantVillage Potato dataset inside: {DATA_DIR.absolute()}")
        print("The folder structure should look exactly like this:")
        for c in classes:
            print(f"  {DATA_DIR}/{c}/*.jpg")
        print("\nTo get the dataset:")
        print("1. Download from Kaggle: https://www.kaggle.com/datasets/emmarex/plantdisease")
        print("2. Extract the 'PlantVillage' folder.")
        print("3. Move the three 'Potato___*' folders into the 'data/potato_disease' directory.")
        print("!" * 80)
        return False
    return True

def train_model():
    if not ensure_dataset():
        print("Exiting training. Please download the dataset first.")
        return

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    # Data transformation for MobileNetV2
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize(256),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Load full dataset
    full_dataset = datasets.ImageFolder(DATA_DIR, transform=data_transforms['train'])
    
    # Split into train/val (80% / 20%)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    # Override transform for val_dataset (workaround for random_split keeping same transform)
    val_dataset.dataset.transform = data_transforms['val']

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    class_names = full_dataset.classes
    print(f"Classes found: {class_names}")
    # Ensure they map to our expected indices:
    # 0 -> Potato Early Blight
    # 1 -> Potato Late Blight
    # 2 -> Potato healthy
    # Note: ImageFolder sorts alphabetically, so it will be:
    # 0: Potato___Early_blight
    # 1: Potato___Late_blight
    # 2: Potato___healthy

    # Load pre-trained MobileNetV2
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
    
    # Modify the classifier for 3 classes
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_ftrs, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_acc = 0.0
    history = {
        'train_acc': [],
        'val_acc': [],
        'train_loss': [],
        'val_loss': []
    }

    print("Starting training...")
    for epoch in range(NUM_EPOCHS):
        print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
        print("-" * 10)

        # Train phase
        model.train()
        running_loss = 0.0
        running_corrects = 0

        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
        train_loss = running_loss / train_size
        train_acc = running_corrects.double() / train_size
        print(f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f}")

        # Val phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)

        val_loss = val_loss / val_size
        val_acc = val_corrects.double() / val_size
        print(f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            print(f"Saving new best model to {MODEL_PATH}")
            torch.save(model.state_dict(), MODEL_PATH)
            
        # Record history
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_acc'].append(train_acc.item())
        history['val_acc'].append(val_acc.item())

    print(f"Training complete. Best Val Acc: {best_acc:.4f}")
    
    # Save history
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)
    print(f"Saved training history to {HISTORY_PATH}")

if __name__ == "__main__":
    train_model()
