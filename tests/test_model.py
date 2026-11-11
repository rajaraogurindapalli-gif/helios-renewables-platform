import pytest
import torch
from src.autoencoder_eval import InverterAutoencoder

@pytest.fixture
def autoencoder():
    model = InverterAutoencoder()
    model.eval()
    return model

def test_model_tensor_dimensions(autoencoder):
    # Batch size 4, 7 input sensor features
    x = torch.randn(4, 7)
    with torch.no_grad():
        out = autoencoder(x)
    assert out.shape == (4, 7), f"Expected reconstructed shape (4, 7), got {out.shape}"

def test_latent_bottleneck_compression(autoencoder):
    # Assert bottleneck layer strictly limits capacity to 4 latent dimensions
    latent = autoencoder.encoder(torch.randn(1, 7))
    assert latent.shape == (1, 4), f"Latent bottleneck must be dimension 4, got {latent.shape[1]}"
