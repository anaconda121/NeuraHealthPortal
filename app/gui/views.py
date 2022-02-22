# Author: Tanish Tyagi

from itertools import chain, cycle
from django import template
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import pandas as pd
import regex as re
import matplotlib.pyplot as plt
import numpy as np

from . import sequence_extraction_pipeline
from . import run_clinical_bert
from . import patient_level_model

# running models on notes
def generate_output():
    """
    notes: dataframe with seq data and model preds
    """
    path = r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_notes.txt"
    notes = sequence_extraction_pipeline.sequence_extraction_pipeline(path)
    print("-----", len(notes), "----")

    notes = notes.rename(columns = {'regex_sent': 'text'}) 
    notes = run_clinical_bert.run_cb(notes)
    notes.to_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_preds.csv", index = False)
    patient_level_features = patient_level_model.run_patient_level(notes)
    patient_level_features.to_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\patient_level_pred.csv", index = False)

    #generate_output()

# highlighting keywords
def highlight(output):
    regex_raw = pd.read_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\keywords.csv")
    k = regex_raw["REGEX"].to_list()
    c = regex_raw["CASE"].to_list()
    regex_list = []

    for i in range(len(k)):
        if (c[i] == 1):
            regex_list.append(re.compile(k[i]))
        else:
            regex_list.append(re.compile(k[i], re.IGNORECASE))

    pattern_list = [re.findall(pattern, output) for pattern in regex_list]
    pattern_list = set(list((chain.from_iterable(pattern_list)))) # flatten list, remove duplicates

    tups = [(itm, r'<mark>' + itm + r'</mark>') for itm in pattern_list]

    # make the substitution to add highlight tag
    for old, new in tups:
        output = re.sub(old, new, output)

    # center on first keyword but suffixing URL with /#keyword
    # output = re.sub(r'(<mark>.+?</mark>)',r'<span id = "first-keyword">\1</span>', output, count=1)

    return output 

def get_overall_results():
    # note count
    path = r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\templates\uploads\patient_1_ehr.txt"
    ehr = open(path, "rb")
    note_count = len(ehr.readlines())

    # sequence count
    sequence_level = pd.read_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_preds.csv")
    sequence_level = sequence_level.reset_index(drop = True)
    sequence_count = len(sequence_level)

    # high proba sequences
    high_proba_sequences = 0
    for i in range(len(sequence_level)):
        # print("PROBA: ", sequence_level.at[i, "three_class"])
        probas = list(eval(sequence_level.at[i, "three_class"]))
        if (probas[2] >= 0.5):
            high_proba_sequences += 1
    
    # patient level CI proba
    patient_level = pd.read_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\patient_level_pred.csv")
    two_class_proba = list(eval(patient_level.at[0, "proba"]))
    print("two:", two_class_proba, len(two_class_proba))
    yes_proba = two_class_proba[0][1] * 100
    yes_proba = str(round(yes_proba, 2))

    return yes_proba, note_count, sequence_count, high_proba_sequences

def sequence_level_results():
    yes_list = []
    ntr_list = []
    no_list = []
    keywords_list = []
    text_list = []
    pred_list = []
    num_list = []
    
    sequence_level = pd.read_csv(r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\test_preds.csv")

    # getting all sequence level stats
    for i in range(len(sequence_level)):
        num_list.append(i + 1)
        probas = list(eval(sequence_level.at[i, "three_class"]))
        keywords = list(eval(sequence_level.at[i, "regex_matches"]))
        text = str(sequence_level.at[i, "padded_regex_sent_preprocessed"])
        text = highlight(text) #highlighting keywords

        pred = ""
        if (sequence_level.at[i, "pred"] == 0):
            pred = "No"
        elif (sequence_level.at[i, "pred"] == 1):
            pred = "Neither"
        else:
            pred = "Yes"
        
        no_list.append(str(round(probas[0] * 100, 2)))
        ntr_list.append(str(round(probas[1] * 100, 2)))
        yes_list.append(str(round(probas[2] * 100, 2)))
        keywords_list.append(keywords)
        text_list.append(text)
        pred_list.append(pred)

    return num_list, pred_list, no_list, ntr_list, yes_list, keywords_list, text_list

def scatterplot(yes_list, path_to_save, format):
    for i in range(len(yes_list)):
        yes_list[i] = float(yes_list[i])

    print("YES LIST: ", yes_list)

    fig = plt.gcf()
    fig.set_size_inches(12.33333, 7)
    x_list = list(np.arange(1,len(yes_list) + 1) * 1)

    s = []
    for i in yes_list:
        s.append(150)

    plt.scatter(x_list, yes_list, s, color = "blue")

    plt.axhline(y=50, color='r', linestyle='--')

    plt.xlim([1, len(yes_list) + 1])
    plt.ylim([0, 100])
    plt.title("Distribution of Sequence's Probability \nof Cognitive Impairment\n")

    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Sequence Number")
    plt.ylabel("Probability of Indicating Cognitive Impairment")

    plt.savefig(path_to_save, bbox_inches='tight', format = format)

def output(request):
    generate_output()

    num_list, pred_list, no_list, ntr_list, yes_list, keywords_list, text_list  = sequence_level_results()
    sequence_level_list = zip(num_list, pred_list, no_list, ntr_list, yes_list, keywords_list, text_list)
    yes_proba, note_count, sequence_count, high_proba_sequences = get_overall_results()

    scatterplot(yes_list, r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\static\images\scatter_plot.png", "png")

    context = {
        "ci_percent" : yes_proba,
        "note_count" : note_count,
        "sequence_count" : sequence_count,
        "high_proba_sequence_count" : high_proba_sequences,
        "sequence_level" : sequence_level_list
        # "pred_list" : pred_list,
        # "probas_list" : probas_list,
        # "keywords_list" : keywords_list,
        # "text_list" : text_list
    }

    return render(request, r"C:\Users\tanis\OneDrive - Phillips Exeter Academy\Data\Programming\APOE-SLAT\Web-Tool\app\gui\templates\gui\output.html", context)

def predict(request):
    context = {}
    return render(request, r"gui\predict.html", context)