def apply_fuzzy_logic(label, confidence):
    if 0.4 < confidence < 0.6:
        return "Uncertain - Need manual review"
    else:
        return label
