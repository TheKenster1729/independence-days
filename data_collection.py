#!/usr/bin/env python3
"""
Merge the “List of national independence days” and “National day” Wikipedia
tables into a single CSV with one row per country:

Country,has_independence_day,independence_day_date,
        has_national_day,national_day_date
"""
import re
import pandas as pd

INDEP_URL   = "https://en.wikipedia.org/wiki/List_of_national_independence_days"
NATDAY_URL  = "https://en.wikipedia.org/wiki/National_day"
OUTFILE     = "independence_and_national_days.csv"

def clean_country(raw: str) -> str:
    """Strip footnote markers, non-breaking spaces, etc."""
    txt = re.sub(r"\[[0-9]+\]", "", raw)            # remove “[12]” style notes
    txt = txt.replace("\xa0", " ").strip()          # NB-spaces ➜ normal
    return txt

def tidy_dates(col: pd.Series) -> pd.Series:
    """Collapse multi-line dates and remove footnote brackets."""
    return (col.astype(str)
              .str.replace(r"\[[0-9]+\]", "", regex=True)
              .str.replace("\n+", " / ", regex=True)
              .str.strip())

# 1) ――― Independence-day table (only one wikitable)
indep = (pd.read_html(INDEP_URL, match="List of independence days")[0]
           .rename(columns={0: "Country",
                            2: "Independence day date"}))   # column 2 = date
indep["Country"] = indep["Country"].apply(clean_country)
indep["Independence day date"] = tidy_dates(indep["Date of holiday"])
indep["has_independence_day"] = True
indep = indep[["Country", "has_independence_day", "Independence day date"]]

# 2) ――― National-day tables (one per A/B/C… section, so concatenate)
nat_tables = pd.read_html(NATDAY_URL, match="Nation")
# returns a list, second item is something else
nat_table_correct = nat_tables[0]

# Drop provincial / sub-national entries ― they always show the parent state
# in parentheses, e.g. “Åland (Finland)”, “Sicily (Italy)”, etc.
is_subnational = nat_table_correct.iloc[:,0].str.contains(r"\(")
nat_table_correct = nat_table_correct[~is_subnational]

nat = (nat_table_correct.rename(columns={nat_table_correct.columns[0]: "Country",
                           nat_table_correct.columns[1]: "National day date"})
          .loc[:, ["Country", "National day date"]])
nat["Country"] = nat["Country"].apply(clean_country)
nat["National day date"] = tidy_dates(nat["National day date"])
nat["has_national_day"] = True

# 3) ――― Merge (outer join so every country appears once)

# Handle duplicates by combining dates for the same country
indep_combined = (indep.groupby('Country')
                      .agg({
                          'has_independence_day': 'first',
                          'Independence day date': lambda x: ' / '.join(x.unique())
                      })
                      .reset_index())

nat_combined = (nat.groupby('Country')
                   .agg({
                       'has_national_day': 'first',
                       'National day date': lambda x: ' / '.join(x.unique())
                   })
                   .reset_index())

merged = (pd.merge(indep_combined, nat_combined,
                   on="Country", how="outer",
                   indicator=False)
            .fillna({"has_independence_day": False,
                     "has_national_day": False,
                     "Independence day date": "",
                     "National day date": ""}))

# 4) ――― Write CSV
merged.sort_values("Country").to_csv(OUTFILE, index=False)
print(f"✓ Wrote {len(merged)} rows to {OUTFILE!r}")
