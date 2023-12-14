import pandas as pd


def inference(model_path, data_path):
    df1 = pd.DataFrame({"inference A": range(5), "B": range(5, 10)})
    df2 = pd.DataFrame({"inference C": range(10, 15), "D": range(15, 20)})
    df3 = pd.DataFrame({"inference E": range(20, 25), "F": range(25, 30)})
    df4 = pd.DataFrame({"inference G": range(30, 35), "H": range(35, 40)})
    return df1, df2, df3, df4
