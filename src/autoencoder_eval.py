import torch
import torch.nn as nn

class InverterAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(7, 16),
            nn.SiLU(),
            nn.Linear(16, 4)
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 16),
            nn.SiLU(),
            nn.Linear(16, 7)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

if __name__ == "__main__":
    model = InverterAutoencoder()
    sample = torch.randn(1, 7)
    reconstructed = model(sample)
    print("Autoencoder network verified. Output shape:", reconstructed.shape)
