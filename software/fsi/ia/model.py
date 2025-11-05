import torch
import torch.nn as nn
import torch.optim as optim

# Por si no está definido:
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
EPOCHS = 5
LR = 1e-3

class SkinDiseaseModelCNN(nn.Module):
    def __init__(self, num_classes):
        super(SkinDiseaseModelCNN, self).__init__()
        self.num_classes = num_classes

        # Capa 1: convolución + activación + pooling
        self.conv1 = nn.LazyConv2d(out_channels=16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Capa 2: convolución + activación + pooling
        self.conv2 = nn.LazyConv2d(out_channels=32, kernel_size=3, padding=1)

        # fully connected
        self.fc1 = nn.LazyLinear(512)
        self.fc2 = nn.LazyLinear(num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(x)

        x = self.relu(self.conv2(x))
        x = self.pool(x)

        x = torch.flatten(x, 1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


model = SkinDiseaseModelCNN(5).to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)