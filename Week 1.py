##################################
#listing 
import pandas as pd
import glob

# Automatically find all CSV files starting with "CRMLSListing" in the folder
files = sorted(glob.glob('CRMLSListing*.csv'))
print("Number of files found:", len(files))

# Read each file one by one
all_listings = []
total_rows_before = 0

for f in files:
    df = pd.read_csv(f, low_memory=False)
    total_rows_before += len(df)
    all_listings.append(df)
    print(f"{f}: {len(df)} rows")

print("Total rows before concat:", total_rows_before)

# Concatenate into one combined dataset
listing = pd.concat(all_listings, ignore_index=True)
print("Total rows after concat:", len(listing))

# Filter to keep only Residential
print("Rows before filter:", len(listing))
listing = listing[listing['PropertyType'] == 'Residential']
print("Rows after filter:", len(listing))

# Save as a new CSV
listing.to_csv('listing_combined.csv', index=False)
print("Saved listing_combined.csv")

##################################
# sold 
import pandas as pd

# ---------- Read each month's Sold file ----------
# Rule: If a month has BOTH a _filled and a regular version, always use the regular one.
#       If a month has ONLY a _filled version, use that instead (and drop the extra columns).

sold202401 = pd.read_csv('CRMLSSold202401.csv', low_memory=False)
sold202402 = pd.read_csv('CRMLSSold202402.csv', low_memory=False)
sold202403 = pd.read_csv('CRMLSSold202403.csv', low_memory=False)
sold202404 = pd.read_csv('CRMLSSold202404.csv', low_memory=False)

# These three months only have a _filled version available
sold202405 = pd.read_csv('CRMLSSold202405_filled.csv', low_memory=False)
sold202405 = sold202405.drop(columns=['latfilled', 'lonfilled'], errors='ignore')

sold202406 = pd.read_csv('CRMLSSold202406_filled.csv', low_memory=False)
sold202406 = sold202406.drop(columns=['latfilled', 'lonfilled'], errors='ignore')

sold202407 = pd.read_csv('CRMLSSold202407_filled.csv', low_memory=False)
sold202407 = sold202407.drop(columns=['latfilled', 'lonfilled'], errors='ignore')

sold202408 = pd.read_csv('CRMLSSold202408.csv', low_memory=False)
sold202409 = pd.read_csv('CRMLSSold202409.csv', low_memory=False)
sold202410 = pd.read_csv('CRMLSSold202410.csv', low_memory=False)
sold202411 = pd.read_csv('CRMLSSold202411.csv', low_memory=False)
sold202412 = pd.read_csv('CRMLSSold202412.csv', low_memory=False)

# This month only has a _filled version available
sold202501 = pd.read_csv('CRMLSSold202501_filled.csv', low_memory=False)
sold202501 = sold202501.drop(columns=['latfilled', 'lonfilled'], errors='ignore')

sold202502 = pd.read_csv('CRMLSSold202502.csv', low_memory=False)
sold202503 = pd.read_csv('CRMLSSold202503.csv', low_memory=False)
sold202504 = pd.read_csv('CRMLSSold202504.csv', low_memory=False)
sold202505 = pd.read_csv('CRMLSSold202505.csv', low_memory=False)
sold202506 = pd.read_csv('CRMLSSold202506.csv', low_memory=False)
sold202507 = pd.read_csv('CRMLSSold202507.csv', low_memory=False)
sold202508 = pd.read_csv('CRMLSSold202508.csv', low_memory=False)
sold202509 = pd.read_csv('CRMLSSold202509.csv', low_memory=False)
sold202510 = pd.read_csv('CRMLSSold202510.csv', low_memory=False)
sold202511 = pd.read_csv('CRMLSSold202511.csv', low_memory=False)
sold202512 = pd.read_csv('CRMLSSold202512.csv', low_memory=False)
sold202601 = pd.read_csv('CRMLSSold202601.csv', low_memory=False)
sold202602 = pd.read_csv('CRMLSSold202602.csv', low_memory=False)
sold202603 = pd.read_csv('CRMLSSold202603.csv', low_memory=False)
sold202604 = pd.read_csv('CRMLSSold202604.csv', low_memory=False)
sold202605 = pd.read_csv('CRMLSSold202605.csv', low_memory=False)

# Row count before concat
all_sold = [sold202401, sold202402, sold202403, sold202404, sold202405,
            sold202406, sold202407, sold202408, sold202409, sold202410,
            sold202411, sold202412, sold202501, sold202502, sold202503,
            sold202504, sold202505, sold202506, sold202507, sold202508,
            sold202509, sold202510, sold202511, sold202512, sold202601,
            sold202602, sold202603, sold202604, sold202605]

print("Rows before concat:", sum(len(df) for df in all_sold))

# Concatenate into one combined dataset
sold = pd.concat(all_sold, ignore_index=True)

print("Rows after concat:", len(sold))

# Filter to keep only Residential
print("Rows before filter:", len(sold))
sold = sold[sold['PropertyType'] == 'Residential']
print("Rows after filter:", len(sold))

# Save as a new CSV
sold.to_csv('sold_combined.csv', index=False)
print("Saved sold_combined.csv")