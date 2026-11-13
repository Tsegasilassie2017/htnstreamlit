"""Step 3: stratified train/test split. Test set is untouched until final evaluation."""
import pandas as pd
from sklearn.model_selection import train_test_split
from htn.config import resolve


def split_and_save(df: pd.DataFrame, cfg: dict):
    target = cfg["data"]["target"]
    train, test = train_test_split(
        df,
        test_size=cfg["data"]["test_size"],
        stratify=df[target],
        random_state=cfg["random_state"],
    )
    for key, part in (("train_path", train), ("test_path", test)):
        path = resolve(cfg["data"][key])
        path.parent.mkdir(parents=True, exist_ok=True)
        part.to_csv(path, index=False)
    return train, test
