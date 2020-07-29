

# lists acquired from a sample run from the table Gwen sent me
import csv
import time
import os

import tablib

from samples.admin import SampleResource
from samples.models import SOIL_TYPE_CHOICES

example_input = ['Sample #', 'Job #', 'Job Name', 'Latitude', 'Longitude', 'Depth', 'Soil type', 'Texture ', 'Color', 'pH', 'Redox Potential (mV)', 'Conductivity (µS/cm)', 'Chloride (ppm)', 'Sulfate (ppm)', 'Salinity (%)', 'Resistivity as Collected (KΩ-cm)', 'Resistivity Saturated (KΩ-cm)', 'Carbonate', 'Sulfide', 'Moisture Content (%)', 'Comments']
example_output = ['sample_no', 'job_no', 'job_name', 'latitude', 'longitude', 'depth', 'soil_type', 'texture', 'color', 'ph', 'redox_potential', 'conductivity', 'chloride', 'sulfate', 'salinity', 'resistivity_as_collected', 'resistivity_saturated', 'carbonate', 'sulfide', 'moisture_content', 'comments']

known_csv_to_model_map = dict(zip(example_input, example_output))
known_model_to_csv_map = dict(zip(example_input, example_output))

def matchup_fieldnames(input_list, model_list):
    """I don't think that model_list is actually necessary, but leaving it just in case"""
    input_match = []
    output_match = []
    for fieldname in input_list:
        # TODO make this fuzzy, or at least caps insensitive
        if fieldname in known_csv_to_model_map:
            input_match.append(fieldname)
            output_match.append(known_csv_to_model_map[fieldname])

    return input_match, output_match


def mapping_sanity_check(inputmap, outputmap, filename):
    if len(inputmap) != len(outputmap):
        return False, "Length of field mappings do not match"
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        input_list = reader.fieldnames
        # Get first line to test and normalize
        firstline = next(reader)
        csv_to_model_map = dict(zip(inputmap, outputmap))
        transformed_firstline = {csv_to_model_map[k]: firstline[k] for k in inputmap}
        transformed_firstline, errors = normalize_rowdict(transformed_firstline)
        if not transformed_firstline:
            return False, errors
        # Instantiate dataset and dry run the first line
        sample_resource = SampleResource()
        dataset = tablib.Dataset(list(transformed_firstline.values()), headers=list(transformed_firstline.keys()))
        result = sample_resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            return False, str(result.row_errors())
        for row in reader:
            transformed_row = {csv_to_model_map[k]: row[k] for k in inputmap}
            transformed_row, errors = normalize_rowdict(transformed_row)
            if not transformed_row:
                return False, errors
            dataset.append(list(transformed_row.values()))

    result = sample_resource.import_data(dataset, dry_run=True)
    if result.has_errors():
        return False, str(result.row_errors())

    return True, result.totals





def normalize_rowdict(row):
    soil_type_dict = {x[1]: x[0] for x in SOIL_TYPE_CHOICES}
    soil_type_dict['Silty Clay'] = "clay"
    soil_type_dict['Silty clay'] = "clay"
    soil_type_dict['Silty Sand'] = "silt"
    soil_type_dict['Clean Sand'] = "sand"
    "string".lower()
    if "soil_type" in row:
        if row["soil_type"] in soil_type_dict:
            row["soil_type"] = soil_type_dict[row["soil_type"]]
        elif row["soil_type"].lower().replace(" ", "_") in dict(SOIL_TYPE_CHOICES):
            row["soil_type"] = row["soil_type"].lower().replace(" ", "_")
        else:
            return False, f"Unrecognized soil type {row['soil_type']} in row {row['sample_no']}"

    if "carbonate" in row:
        row["carbonate"] = row["carbonate"].lower()
    if "sulfide" in row:
        row["sulfide"] = row["sulfide"].lower()

    if "moisture_content" in row:
        try:
            float(row["moisture_content"])
        except ValueError:
            row["moisture_content"] = None

    return row, None


def start_processing(input_match, output_match, upload_filepath):
    start = time.time()
    with open(upload_filepath, "r") as f:
        reader = csv.DictReader(f)
        input_list = reader.fieldnames

        csv_to_model_map = dict(zip(input_match, output_match))
        # Instantiate dataset and dry run the first line
        sample_resource = SampleResource()
        dataset = None
        for row in reader:
            transformed_row = {csv_to_model_map[k]: row[k] for k in input_match}
            transformed_row, errors = normalize_rowdict(transformed_row)
            if not transformed_row:
                return False
                print("Something has gone wrong during final import")
                print(errors)
            if not dataset:
                dataset = tablib.Dataset(headers=list(transformed_row.keys()))
            dataset.append(list(transformed_row.values()))

    result = sample_resource.import_data(dataset)
    end = time.time()
    print("ingestion complete")
    print(f"elapsed time = {end - start}")
    print(f"rows processed = {len(dataset)}")

    if not result.has_errors():
        os.remove(upload_filepath)

    return result
