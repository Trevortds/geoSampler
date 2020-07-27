

# lists acquired from a sample run from the table Gwen sent me
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
    return (False, "Field mapping sanity check feature is not implemented yet")