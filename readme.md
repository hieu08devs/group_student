# Bài toán phân nhóm học tập, dựa vào kết quả học tập

## Nhận xét

- Dạng bài toán: tối ưu tập hợp

- Ý tưởng: dùng giải thuật di truyền (Genetic algorithm)

### Ràng buộc:

- Sinh viên phải được xếp nhóm.

- Nhóm có giới hạn số sinh viên.

### Genetic algorithm key-points:

- Encode gen: Xếp danh sách sinh viên theo hàng, nhiễm sắc thể chính là tên nhóm

- Hàm fitness: hàm mục tiêu (điểm số của cả lớp sau khi được phân nhóm)

- Population size: tuỳ chỉnh

- Crossover: Ordered crossover

- Mutation: Swap mutation

- Stoping condition: dựa vào lower-bound và số vòng lặp

## How to run

- data input: đặt vào thư mục PPL_sample, mỗi thư mục con là 1 cột điểm

    - PPL_sample/        
        - week1/student_score.csv
        - week2/student_score.csv

- output: merged_output.csv và result_output.csv

- run: python3 group_student_app.py

### Các thông số có thể điều chỉnh

- Số lượng sinh viên mỗi group: `GROUP_SIZE` trong file group_student_app.py (`GROUP_SIZE = 2`, `GROUP_SIZE = 3`)

- Thông số của giải thuật di truyền: `POPULATION_SIZE`, `LOOP` trong file genetic_group.py