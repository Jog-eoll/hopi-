import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

# 加载CSV文件
file_path = "D:/datas/模型_top300-2.csv"
df = pd.read_csv(file_path)

# 清理数据：将 '现价' 和 '参考价格' 列中的非数值字符替换为NaN
df['现价'] = df['现价'].str.replace('%', '').str.replace(',', '').replace('#VALUE!', float('nan')).astype(float)
df['参考价格'] = df['参考价格'].str.replace('%', '').str.replace(',', '').replace('#VALUE!', float('nan')).astype(float)

# 计算涨幅：(现价 - 参考价格) / 参考价格 * 100
df['涨幅'] = ((df['现价'] - df['参考价格']) / df['参考价格']) * 100

# 删除包含NaN值的行
df = df.dropna()

# 按系列分组计算涨幅均值
series_data = df.groupby('系列')['涨幅'].mean().reset_index()

# 创建柱状图
bar = (
    Bar()
    .add_xaxis(series_data['系列'].tolist())
    .add_yaxis("涨幅均值", series_data['涨幅'].round(2).tolist())
    .set_global_opts(title_opts=opts.TitleOpts(title="不同系列的涨幅均值"))
)

# 保存为HTML文件
bar.render("涨幅柱状图.html")
