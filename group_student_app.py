# python3 group_student_app.py
# put data in PPL_sample folder
# PPL_sample/
#           week1/<student_score>.csv
#           week2/<student_score>.csv
import os
import pandas as pd
import genetic_group as ga
import preprocess_data as predata
import time

GROUP_SIZE = 2
MAX_SCORE = 10.0

input_dir = 'PPL_sample'
output_dir = 'output'

id_columns = ["Tên", "Họ"]
score_column = "Điểm/10,00"
group_column = "Nhóm"

os.makedirs(output_dir, exist_ok=True)

# prepare data
merged = predata.merge_student_score(input_dir, id_columns, score_column)
merged.sort_values(by=id_columns[0], inplace=True)
merged.to_csv(f'{output_dir}/merged_output.csv', index=False)
print(f'merged describe: \n {merged.describe()}')


# run genetic group function
start_time = time.time()

student_score = predata.get_student_score(merged, id_columns, inplace=True)
grouped = ga.group_student_by_ga(student_score, group_size=GROUP_SIZE, max_score=MAX_SCORE)
print(f'final grouped scores: {grouped.fitness}')
done_time = time.time()

elapsed = done_time - start_time
print(f'Time elapsed: {elapsed}')

# export output
merged[group_column] = grouped.genes
merged.to_csv(f'{output_dir}/result_output.csv', index=False)
