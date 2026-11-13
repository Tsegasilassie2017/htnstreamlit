"""End-to-end orchestration:  python -m htn.pipeline --stage all"""
import argparse
import json

import pandas as pd

from htn.config import feature_lists, load_config, resolve
from htn.data.ingest import load_raw
from htn.data.split import split_and_save
from htn.data.validate import clean, validate
from htn.models.evaluate import evaluate
from htn.models.predict import load_artifact
from htn.models.train import compare_models, save_artifact, tune_and_fit


def stage_data(cfg):
    df = load_raw(cfg)
    report = validate(df, cfg)
    print("Data quality report:\n", json.dumps(report, indent=2))
    split_and_save(clean(df, cfg), cfg)
    print("Saved train/test splits.")


def stage_train(cfg):
    train = pd.read_csv(resolve(cfg["data"]["train_path"]))
    table = compare_models(train, cfg)
    print("\nCross-validated model comparison:\n", table.to_string(index=False))
    best = table.iloc[0]["model"]
    print(f"\nTuning best model: {best}")
    pipe, params, score = tune_and_fit(train, cfg, best)
    meta = save_artifact(pipe, cfg, best, params, score)
    print("Saved model:", json.dumps(meta, indent=2))


def stage_evaluate(cfg):
    test = pd.read_csv(resolve(cfg["data"]["test_path"]))
    art = load_artifact(cfg)
    print("\nTest-set metrics:\n", json.dumps(evaluate(art["pipeline"], art["features"], test, cfg), indent=2))


STAGES = {"data": stage_data, "train": stage_train, "evaluate": stage_evaluate}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=[*STAGES, "all"], default="all")
    p.add_argument("--config", default=None)
    args = p.parse_args()
    cfg = load_config(args.config) if args.config else load_config()
    for name in (STAGES if args.stage == "all" else [args.stage]):
        print(f"\n===== {name.upper()} =====")
        STAGES[name](cfg)


if __name__ == "__main__":
    main()
