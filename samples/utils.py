

# lists acquired from a sample run from the table Gwen sent me
import csv

import tablib

from samples.admin import SampleResource
from samples.models import SOIL_TYPE_CHOICES

select2 = ['Sample #', 'Job #', 'Job Name', 'Latitude', 'Longitude', 'Depth', 'Soil type', 'Texture ', 'Color', 'pH', 'Redox Potential (mV)', 'Conductivity (µS/cm)', 'Chloride (ppm)', 'Sulfate (ppm)', 'Salinity (%)', 'Resistivity as Collected (KΩ-cm)', 'Resistivity Saturated (KΩ-cm)', 'Carbonate', 'Sulfide', 'Moisture Content (%)', 'Comments']
select3 = ['sample_no', 'job_no', 'job_name', 'latitude', 'longitude', 'depth', 'soil_type', 'texture', 'color', 'ph', 'redox_potential', 'conductivity', 'chloride', 'sulfate', 'salinity', 'resistivity_as_collected', 'resistivity_saturated', 'carbonate', 'sulfide', 'moisture_content', 'comments']

known_csv_to_model_map = dict(zip(select2, select3))
known_model_to_csv_map = dict(zip(select2, select3))

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
        firstline = next(reader)
    csv_to_model_map = dict(zip(select2, select3))
    transformed_firstline = {csv_to_model_map[k]: firstline[k] for k in inputmap}
    transformed_firstline, errors = normalize_rowdict(transformed_firstline)
    if not transformed_firstline:
        return False, errors
    sample_resource = SampleResource()
    dataset = tablib.Dataset(list(transformed_firstline.values()), headers=list(transformed_firstline.keys()))
    result = sample_resource.import_data(dataset, dry_run=True)
    print(result.has_errors())
    print(result.row_errors())
    print(result.base_errors)
    print(result.invalid_rows)
    print(result.failed_dataset)
    if result.has_errors():
        return False, str(result.row_errors())

    return (True, f"{result.totals}")





def normalize_rowdict(row):
    soil_type_dict = {x[1]: x[0] for x in SOIL_TYPE_CHOICES}
    soil_type_dict['Silty Clay'] = "clay"
    soil_type_dict['Silty Sand'] = "silt"
    "string".lower()
    if "soil_type" in row:
        if row["soil_type"] in soil_type_dict:
            row["soil_type"] = soil_type_dict[row["soil_type"]]
        elif row["soil_type"].lower.replace(" ", "_") in dict(SOIL_TYPE_CHOICES):
            row["soil_type"] = row["soil_type"].lower.replace(" ", "_")
        else:
            return False, f"Unrecognized soil type in row {row['sample_no']}"

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
