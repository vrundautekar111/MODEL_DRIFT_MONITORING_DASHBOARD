
from src.models.train import train_model


if __name__ == "__main__":
    metrics = train_model()
    print("Training completed.")
    print(metrics)
