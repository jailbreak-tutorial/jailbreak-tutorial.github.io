import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data in long-form
models = ['Mistral-7B-Instruct-v2'] * 9 + ['Llama-3-8B-Instruct'] * 9
methods = (['Refusal Trained', 'Adv Trained', '+RR'] * 3) + (['Refusal Trained', '+RR', 'Cygnet'] * 3)
attacks = ['TAP-T'] * 3 + ['PAIR'] * 3 + ['GCG'] * 3 + ['TAP-T'] * 3 + ['PAIR'] * 3 + ['GCG'] * 3
values = [
    85.8, 68.7, 17.5, 69.5, 59.9, 23.3, 88.7, 7.8, 11.2,  # Mistral
    17.4, 2.1, 0.0, 18.7, 7.5, 0.0, 44.5, 2.5, 0.0        # Llama
]

df = pd.DataFrame({
    'Model': models,
    'Method': methods,
    'Attack': attacks,
    'Value': values
})

# Filter for just 'Refusal Trained' and '+RR'
df = df[df['Method'].isin(['Refusal Trained', '+RR'])]

sns.set(style="whitegrid", font_scale=1.8)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']

palette = {'TAP-T': '#F6B500', 'PAIR': '#009EFF', 'GCG': '#A569BD'}

g = sns.catplot(
    data=df,
    kind="bar",
    x="Method",
    y="Value",
    hue="Attack",
    col="Model",
    palette=palette,
    height=6,
    aspect=0.9,
    legend=True
)

g.set_axis_labels("Method", "Attack success rate (%)")
g.set_titles("{col_name}")

# g._legend.remove()
# handles, labels = g.axes[0][0].get_legend_handles_labels()
# g.fig.legend(
#     handles, labels,
#     loc='lower center',
#     bbox_to_anchor=(0.5, 0.13),
#     ncol=3,
#     frameon=False
# )
# g.fig.subplots_adjust(bottom=0.28)

# plt.show()
g.savefig('circuit_breakers_facetgrid.pdf') 