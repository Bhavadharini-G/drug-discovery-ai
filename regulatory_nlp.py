import pandas as pd
import re

# Load example clinical trial summaries
df = pd.read_csv('data/clinical_trials.csv')  # columns: trial_id, summary

# Simple keyword extraction: does the summary mention FDA?
df['has_fda'] = df['summary'].apply(lambda x: bool(re.search(r'FDA', x, re.I)))
print(df[['trial_id', 'has_fda']])
