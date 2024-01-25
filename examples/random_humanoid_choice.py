import random

def sample_humanoid(name_list, num_samples):
    samples = []
    for i in range(num_samples):
        samples.append(random.sample(name_list, 1)[0])
    return samples

names_list = ["female_0", "female_1", "female_2", "female_3", "male_0", "male_1", "male_2", "male_3"]

random.seed(42)
num_samples = 50

# サンプリングの実行
result = sample_humanoid(names_list, num_samples)

# 結果の表示
for i in range(num_samples):
    print(str(i) + " : ", result[i])