from xlrd import open_workbook,XLRDError
from collections import defaultdict


def get_job_titles(path_to_job_titles):
    try:
        wb = open_workbook(path_to_job_titles)
    except XLRDError as e:
        print(e)
    sheet = wb.sheet_by_index(0)
    no_of_entries = sheet.nrows
    job_titles = []
    for i in range(1, no_of_entries):
        job_titles.append(sheet.cell_value(i, 0))
    return job_titles

def get_location_details(path_to_location_details):
    try:
        wb = open_workbook(path_to_location_details)
    except XLRDError as e:
        print(e)

    sheet = wb.sheet_by_index(0)
    no_of_cols = sheet.ncols
    no_of_rows = sheet.nrows
    location_details = defaultdict(list)

    for i in range(no_of_cols):
        key_name = sheet.cell_value(0, i)
        for j in range(1, no_of_rows):
            location_details[key_name].append(sheet.cell_value(j, i))
    print(location_details['State'][0], location_details['Code'][0], location_details['Capital'][0])



