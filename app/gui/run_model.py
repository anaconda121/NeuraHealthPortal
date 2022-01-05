import pandas as pd
import regex as re

import sequence_extraction_pipeline
import run_clinical_bert
import patient_level_model

# running models on notes
def generate_output():
    """
    notes: dataframe with seq data and model preds
    """
    path = r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_notes.txt"
    notes = sequence_extraction_pipeline.sequence_extraction_pipeline(path)
    notes = notes.rename(columns = {'regex_sent': 'text'}) 
    notes = run_clinical_bert.run_cb(notes)
    notes.to_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_preds_actual.csv", index = False)
    patient_level_features = patient_level_model.run_patient_level(notes)
    patient_level_features.to_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\patient_level_pred_actual.csv", index = False)

generate_output()