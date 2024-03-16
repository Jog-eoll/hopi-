import pandas as pd

# 读取CSV文件
csv_file = "D:/datas/模型_top300-1.csv"
df = pd.read_csv(csv_file)

# 将出荷时间列转换为年份，处理不规范的数据
def convert_to_year(date_str):
    try:
        return pd.to_datetime(date_str, format='%Y年%m月%d日').year
    except ValueError:
        return None

df['出荷时间'] = df['出荷时间'].apply(convert_to_year)

# 删除包含无效年份的行
df = df.dropna(subset=['出荷时间'])

# 保存修改后的数据到新的CSV文件
output_csv_file = "D:/datas/模型_top300-1_updated.csv"
df.to_csv(output_csv_file, index=False)
