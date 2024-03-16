import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid

# 读取CSV文件
csv_file = "D:/datas/模型_top300-1.csv"
df = pd.read_csv(csv_file)

# 提取指定比例类型的数据
selected_ratios = ['1/100', '1/144', '1/60']
selected_df = df[df['比例'].isin(selected_ratios)]

# 设置评分分组范围
score_ranges = np.arange(0, 5.05, 0.2)

# 根据评分分组范围计算各组的评分数量
selected_df['评分范围'] = pd.cut(selected_df['评分'], bins=score_ranges, right=False)
score_groups = selected_df.groupby(['比例', '评分范围']).size().reset_index(name='数量')

# 创建单个比例类型的柱状图
def create_single_bar(ratio):
    bar = (
        Bar()
        .add_xaxis(score_ranges[:-1])  # 排除最后一个范围（5.0分）
        .add_yaxis(ratio, score_groups[score_groups['比例'] == ratio]['数量'].tolist())
        .set_series_opts(label_opts=opts.LabelOpts(position="top", formatter="{c}"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{ratio}比例评分分布"),
            xaxis_opts=opts.AxisOpts(type_="category", name="评分"),
            yaxis_opts=opts.AxisOpts(type_="value", name="数量"),
        )
    )
    return bar

# 创建三个比例类型的柱状图
bars = [create_single_bar(ratio) for ratio in selected_ratios]

# 合并柱状图
grid = (
    Grid()
    .add(bars[0], grid_opts=opts.GridOpts(pos_left="5%", pos_top="10%", height="30%"))
    .add(bars[1], grid_opts=opts.GridOpts(pos_left="5%", pos_top="50%", height="30%"))
    .add(bars[2], grid_opts=opts.GridOpts(pos_left="5%", pos_top="90%", height="30%"))
)

# 生成HTML文件
grid.render("toy_score_summary_bar_chart.html")
