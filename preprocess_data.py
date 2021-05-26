import os
import pandas as pd

def convertFloat(value, default_val=0.0):
  try:
    return float(value)
  except ValueError:
    return default_val

def merge_student_score(input_dir, id_columns, score_column):
    '''
    Merge student score to pandas dataframe
    - main dir: data/
                week1/<student_score>.csv
                week2/<student_score>.csv
    - id_columns: columns to identify student: ["Tên", "Họ"]
    - score_column: main scores of a file: "Điểm/10,00"
    - output: "Tên", "Họ", "Week1", "Week2", "Week3"
    '''
    merged = pd.DataFrame()
    for sub_dir in os.listdir(input_dir):
        sub_path = os.path.join(input_dir, sub_dir)
        if not os.path.isdir(sub_path):
            continue

        sub_dataframe = pd.DataFrame()
        for file_name in os.listdir(sub_path):
            file_path = os.path.join(sub_path, file_name)
            if not file_path.endswith('csv'):
                continue

            dataset = pd.read_csv(file_path)[id_columns + [score_column]]
            dataset = dataset.dropna(how='any', subset=id_columns)

            # merge data in sub folder
            if sub_dataframe.shape[0] == 0:
                sub_dataframe = dataset
            else:
                sub_dataframe = pd.merge(sub_dataframe, dataset, how='outer')

        # remove duplicate
        sub_dataframe.sort_values(
            by=[score_column], ascending=False, inplace=True)
        sub_dataframe.drop_duplicates(subset=id_columns, inplace=True)
        sub_dataframe.columns = id_columns + [sub_dir]
        print(f'sub_dataframe.describe:\n {sub_dataframe.describe()}\n')

        # merge data
        if merged.shape[0] == 0:
            merged = sub_dataframe
        else:
            merged = pd.merge(merged, sub_dataframe,
                              on=id_columns, how='outer')

    merged.fillna('0', inplace=True)
    return merged

def get_student_score(dataset, id_columns, inplace=False):
    '''
    Return raw students score table, convert string score to float
    - dataset: "Tên", "Họ", "Week1", "Week2", "Week3"
    - output: content of Week1, Week2, Week3 in float
    - inplace: if True, also update dataset. default is False
    '''
    raw_scores = dataset.values[:, len(id_columns):]
    if inplace:
        converted_scores = raw_scores
    else:
        converted_scores = raw_scores.copy()

    for row in converted_scores:
        for col in range(len(row)):
            num_string = row[col].replace(',', '.')
            row[col] = convertFloat(num_string)
    return converted_scores