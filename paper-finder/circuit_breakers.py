import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Use seaborn whitegrid style
sns.set(font_scale=1.8, style="whitegrid")

# Use Palatino font
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Palatino']

methods = ['Refusal Trained', 'Adv Trained', '+RR (Ours)']
TAP = [85.8, 68.7, 17.5]
PAIR = [69.5, 59.9, 23.3]
GCG = [88.7, 7.8, 11.2]

x = np.arange(len(methods))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(x - width, TAP, width, label='TAP-T', color='#F6B500')
ax.bar(x, PAIR, width, label='PAIR', color='#009EFF')
ax.bar(x + width, GCG, width, label='GCG', color='#A569BD')

ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.set_ylabel('Robustness (↓)')
ax.set_title('Robustness of Circuit Breakers (Mistral-7B-Instruct-v2)', pad=10)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

plt.tight_layout()
plt.show()
# plt.savefig('circuit_breakers_comparison.pdf') 