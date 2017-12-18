"""
This will be the main script.

AUTHOR
Warren Lacaba
"""

from logic import id3
from logic import cart
import data_cleanup

print("Parsing data and correcting for inflation...")
data_cleanup.clean_data()

print("\nBuilding decision tree using ID3 algorithm...\n")
id3.run_id3('data/new_database2.csv', 50)

cart.run_cart('data/new_database2.csv', 50)
