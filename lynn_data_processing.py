#!/usr/bin/env python
import pandas as pd

# The list in lynn_consolidated_list needs to be converted into a "clean" list with information:
# Name
# Gender
# Age
# Detail of death (description of death, not the post mortem number etc)
# Street
# Location
# Date of death - in format day/month/year - simple date, not "Died on", etc
# Comments
#
# Then Location needs to be converted into a geographic coordinate

input_filename = 'lynn_consolidated_list.csv'
string_data = open(input_filename).read()
data = pd.read_csv(input_filename, names=['Name', 'Gender', 'Age', 'Details', 'Street', 'Location', 'Date of death', 'Comments'])
