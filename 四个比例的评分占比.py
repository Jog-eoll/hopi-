import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Page

# 读取CSV文件
csv_file = "D:/datas/模型_top300-2.csv"
df = pd.read_csv(csv_file)

# 提取所需的数据
series_scores = df[['系列', '评分']]

# 定义评分范围和标签
score_ranges = [0, 4, 4.25, 4.5, 4.75, 5]
score_labels = ['<4', '4-4.25', '4.25-4.5', '4.5-4.75', '4.75-5']

# 初始化四个系列的评分统计字典
series_scores_counts = {'HG': [0] * len(score_ranges),
                        'RG': [0] * len(score_ranges),
                        'MG': [0] * len(score_ranges),
                        'PG': [0] * len(score_ranges)}

# 统计各系列评分占比
for index, row in series_scores.iterrows():
    series = row['系列']
    score = row['评分']
    if series in series_scores_counts and 0 <= score <= 5:
        for i in range(len(score_ranges) - 1):
            if score_ranges[i] <= score < score_ranges[i + 1]:
                series_scores_counts[series][i] += 1

# 创建四个饼图
pie_hg = (
    Pie()
    .add("", [list(z) for z in zip(score_labels, series_scores_counts['HG'])])
    .set_global_opts(title_opts=opts.TitleOpts(title="HG评分占比"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

pie_rg = (
    Pie()
    .add("", [list(z) for z in zip(score_labels, series_scores_counts['RG'])])
    .set_global_opts(title_opts=opts.TitleOpts(title="RG评分占比"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

pie_mg = (
    Pie()
    .add("", [list(z) for z in zip(score_labels, series_scores_counts['MG'])])
    .set_global_opts(title_opts=opts.TitleOpts(title="MG评分占比"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

pie_pg = (
    Pie()
    .add("", [list(z) for z in zip(score_labels, series_scores_counts['PG'])])
    .set_global_opts(title_opts=opts.TitleOpts(title="PG评分占比"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# 创建一个页面并将四个饼图放入其中
page = Page()
page.add(pie_hg)
page.add(pie_rg)
page.add(pie_mg)
page.add(pie_pg)

# 生成HTML文件
html_file = "score_pie_chart.html"
page.render(html_file)
