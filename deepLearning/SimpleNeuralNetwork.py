import torch
from torch import nn

class SimpleNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU() # Rectified Linear Unit activation
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x


from torch.utils.data import DataLoader, TensorDataset

# Example data (replace with your actual data)
X_train = torch.randn(1, 10) # 100 samples, 10 features
y_train = torch.randint(0, 2, (1, 1)).float() # 100 samples, binary output

print(X_train)
print(y_train)

train_dataset = TensorDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


from torch import optim

# Instantiate the model
input_size = 10
hidden_size = 20
output_size = 1
model = SimpleNeuralNetwork(input_size, hidden_size, output_size)

# Define loss function and optimizer
criterion = nn.BCEWithLogitsLoss() # For binary classification
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 1
for epoch in range(num_epochs):
    for inputs, targets in train_loader:
        # Forward pass
        print("applied : ",inputs)
        outputs = model(inputs)
        print("outputs : ",outputs)
        print("targets : ",targets)

        loss = criterion(outputs, targets)

        # Backward and optimize
        optimizer.zero_grad() # Clear previous gradients
        loss.backward() # Compute gradients
        optimizer.step() # Update weights


    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

with torch.inference_mode():
    print("Inference model :")
    xval= torch.randn(1, 10)
    y_pred = model(xval)
    print(y_pred)
    y_pred = model(xval)
    print(y_pred)