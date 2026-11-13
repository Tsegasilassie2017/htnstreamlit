from htn.data.split import split_and_save
from htn.config import feature_lists
from htn.models.predict import predict_proba
from htn.models.train import compare_models, tune_and_fit


def test_end_to_end(df, cfg, tmp_path, monkeypatch):
    cfg = {**cfg, "training": {**cfg["training"], "cv_folds": 3, "tuning_iterations": 2}}
    cfg["data"] = {**cfg["data"], "train_path": str(tmp_path / "tr.csv"),
                   "test_path": str(tmp_path / "te.csv")}
    monkeypatch.setattr("htn.config.ROOT", tmp_path)
    train, test = split_and_save(df, cfg)
    assert abs(len(test) / len(df) - cfg["data"]["test_size"]) < 0.02
    table = compare_models(train, cfg)
    assert table["roc_auc"].iloc[0] > 0.6
    pipe, _, score = tune_and_fit(train, cfg, "logistic_regression")
    cat, num = feature_lists(cfg)
    row = test[cat + num].iloc[0].to_dict()
    p = predict_proba({"pipeline": pipe, "features": cat + num}, row)
    assert 0.0 <= p <= 1.0
