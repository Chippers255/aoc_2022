import gc
import numpy
import pandas
import xgboost

from sklearn.metrics import mean_squared_error


MOVE_SCORES = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

# Save the compute power for the model training
SCORES = {
    "X": {       # ROCK
        "A": 4,  # ROCK
        "B": 1,  # PAPER
        "C": 7   # SCISSORS
    },
    "Y": {       # PAPER
        "A": 8,  # ROCK
        "B": 5,  # PAPER
        "C": 2   # SCISSORS
    },
    "Z": {       # SCISSORS
        "A": 3,  # ROCK
        "B": 9,  # PAPER
        "C": 6   # SCISSORS
    }
}


def data_prep() -> pandas.DataFrame:
    df = pandas.read_csv("input.csv")
    enemy_dummys = pandas.get_dummies(df['enemy_move'], drop_first=False)
    my_dummys = pandas.get_dummies(df['my_move'], drop_first=False)
    df = pandas.concat([df, enemy_dummys, my_dummys], axis=1)
    df["move_score"] = df["my_move"].map(MOVE_SCORES)
    df["total_scores"] = df.apply(lambda row: SCORES[row["my_move"]][row["enemy_move"]], axis=1)

    del enemy_dummys
    del my_dummys
    gc.collect()

    return df


def run_model(df: pandas.DataFrame) -> list:
    features = df.drop(columns=["enemy_move","my_move","total_scores"]).values
    labels = df["total_scores"].values

    # Overkilled the number of estimators and the depth to ensure memorization
    xg_reg = xgboost.XGBRegressor(objective ='reg:linear', learning_rate=0.1, max_depth=11, n_estimators=100)

    # Who needs a validation set?
    xg_reg.fit(features,labels)
    preds = xg_reg.predict(features)

    preds = [int(round(x, 0)) for x in preds]

    # Go for memorization
    rmse = numpy.sqrt(mean_squared_error(labels, preds))
    print(f"RMSE: {rmse}")
    return preds



df = data_prep()
results = run_model(df)
print(sum(results))