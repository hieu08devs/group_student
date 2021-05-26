# Bài toán phân nhóm học tập, dựa vào kết quả học tập

## Nhận xét

- Bài toán tương tự: knapsack problem

- Ý tưởng, dùng giải thuật di truyền (genetic algorithm)

### Ràng buộc:

- Sinh viên phải được xếp nhóm

- Nhóm có giới hạn số sinh viên (cố định nhóm 3 sinh viên)

### Genetic algorithm key-points:

- Encode gen: Xếp danh sách sinh viên theo hàng, nhiễm sắc thể chính là tên nhóm

- Hàm fitness: hàm mục tiêu (điểm số của cả lớp sau khi được phân nhóm)

- Population size: tuỳ chỉnh

- Crossover: Ordered crossover

- Mutation: Swap mutation

- Stoping condition: dựa vào lower-bound và số vòng lặp

## How to run

- data input: đặt vào thư mục PPL_sample, mỗi thư mục con là 1 cột điểm

- run: python3 group_student_app.py

- output: merged_output.csv và result_output.csv