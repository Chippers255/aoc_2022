import random

import numpy
import pandas
import xgboost
from sklearn.metrics import mean_squared_error

# How much is a rock worth?
MOVE_SCORES = {"X": 1, "Y": 2, "Z": 3}

# Save the compute power for the model training
SCORES = {
    "X": {"A": 4, "B": 1, "C": 7},  # ROCK  # ROCK  # PAPER  # SCISSORS
    "Y": {"A": 8, "B": 5, "C": 2},  # PAPER  # ROCK  # PAPER  # SCISSORS
    "Z": {"A": 3, "B": 9, "C": 6},  # SCISSORS  # ROCK  # PAPER  # SCISSORS
}


def build_train_set() -> pandas.DataFrame:
    """Build a random dataset for training our model. 10,000 observations should suffice."""
    train_list = [
        [random.choice(["A", "B", "C"]), random.choice(["X", "Y", "Z"])]
        for _ in range(10000)
    ]
    return pandas.DataFrame(train_list, columns=["enemy_move", "my_move"])


def data_prep(training_data: pandas.DataFrame) -> pandas.DataFrame:
    """Take a move set as a pandas dataframe then create the features and label required for modeling."""
    # First we need to encode the move strings into something a model can use. One-hot-encoding should do the trick
    enemy_dummys = pandas.get_dummies(training_data["enemy_move"], drop_first=False)
    my_dummys = pandas.get_dummies(training_data["my_move"], drop_first=False)

    # Join all that data together
    df = pandas.concat([training_data, enemy_dummys, my_dummys], axis=1)

    # Let's engineer a new feature, we will add the move scores to the feature set
    df["move_score"] = df["my_move"].map(MOVE_SCORES)

    # Finally we need to create the training label, just ignore that we also create the answers for the real data
    df["total_scores"] = df.apply(
        lambda row: SCORES[row["my_move"]][row["enemy_move"]], axis=1
    )

    return df


def train_model(training_features: pandas.DataFrame) -> xgboost.XGBRegressor:
    """Takes a dataframe and trains a model on it. We are using XGBoost because it is fast, easy, and requires little
    tuning."""
    features = training_features.drop(
        columns=["enemy_move", "my_move", "total_scores"]
    ).values
    labels = training_features["total_scores"].values

    # Overkilled the number of estimators and the depth to ensure memorization
    xgb_reg = xgboost.XGBRegressor(
        objective="reg:linear", learning_rate=0.1, max_depth=11, n_estimators=100
    )

    # Go for memorization
    xgb_reg.fit(features, labels)

    # The model doesn't give me whole number so I need to force it
    preds = xgb_reg.predict(features)
    preds = [int(round(x, 0)) for x in preds]

    # Who needs a separate validation set?
    rmse = numpy.sqrt(mean_squared_error(labels, preds))
    print(f"Training RMSE: {rmse:.4f}")

    return xgb_reg


def run_model(
    xgb_reg: xgboost.XGBRegressor, inference_features: pandas.DataFrame
) -> list:
    features = inference_features.drop(
        columns=["enemy_move", "my_move", "total_scores"]
    ).values
    preds = xgb_reg.predict(features)
    preds = [int(round(x, 0)) for x in preds]
    return preds


if __name__ == "__main__":
    train_df = build_train_set()
    train_df = data_prep(train_df)

    run_df = pandas.read_csv("input.csv")
    run_df = data_prep(run_df)

    model = train_model(train_df)
    results = run_model(model, run_df)
    print(f"Total Score: {sum(results):,.0f}")
