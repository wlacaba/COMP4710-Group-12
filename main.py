"""
This will be the main script.
"""

from logic import id3
import data_cleanup

print("Parsing data and correcting for inflation...\n")
data_cleanup.clean_data()

print("Beginning tree construction and accuracy testing...\n")
id3.run_id3('data/new_database2.csv', 50)
