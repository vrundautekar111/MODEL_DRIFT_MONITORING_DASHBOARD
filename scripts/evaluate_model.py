
from src.models.predict import load_model


if __name__ == "__main__":
    bundle = load_model()

    print("Saved holdout evaluation:")

    for key, value in bundle.get("metrics", {}).items():
        print(f"{key}: {value}")
