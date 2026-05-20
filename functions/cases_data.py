# functions/cases_data.py

# 1. Patientenfälle
cases = {
    "Fall 1": {
        "story": "Eine 26-jährige Patientin wird notfallmässig ins Spital eingeliefert. Sie wirkt verwirrt und desorientiert. Die Pflege berichtet von hohem Fieber und starkem Schüttelfrost. Bei der Untersuchung zeigt sich eine schmerzhafte Schwellung am Oberschenkel, aus dem eitriges Sekret austritt. Eine Probe wird ins Labor geschickt.",
        "name": "Britney McAdams", "age": 26, "sex": "weiblich", "symptoms": "Fieber, Schüttelfrost, Verwirrtheit"
    },
    "Fall 2": {
        "story": "Eine Patientin stellt sich mit starken Halsschmerzen und Fieber vor. Sie berichtet über Schluckbeschwerden seit mehreren Tagen. Bei der Untersuchung zeigen sich gerötete Tonsillen und geschwollene Lymphknoten.",
        "name": "Rebekka Schmidt", "age": 17, "sex": "weiblich", "symptoms": "Halsschmerzen, Fieber"
    },
    "Fall 3": {
        "story": "Eine junge Patientin klagt über Schmerzen beim Wasserlassen und häufigen Harndrang. Zusätzlich bestehen leichte Unterbauchschmerzen.",
        "name": "Sara Keller", "age": 24, "sex": "weiblich", "symptoms": "Dysurie, Bauchschmerzen, Häufiger Harndrang"
    },
    "Fall 4": {
        "story": "Ein Patient stellt sich mit anhaltenden Bauchschmerzen und Durchfall vor. Er berichtet über eine kürzliche Reise ins Ausland.",
        "name": "Tim Weber", "age": 33, "sex": "männlich", "symptoms": "Bauchschmerzen, Durchfall, Gewichtsverlust"
    },
    "Fall 5": {
        "story": "Bei einem älteren Patienten zeigt sich eine Rötung im Bereich einer Katheterstelle. Die Beschwerden bestehen seit mehreren Tagen.",
        "name": "Samuel D McDonald", "age": 72, "sex": "männlich", "symptoms": "Rötung an Katheterstelle, leichtes Fieber, Unwohlsein"
    },
    "Fall 6": {
        "story": "Eine Patientin berichtet über Juckreiz und einen weisslichen Belag im Mund- und Intimbereich. Die Beschwerden bestehen seit einigen Tagen.",
        "name": "Kelly Keller", "age": 29, "sex": "weiblich", "symptoms": "Juckreiz, weisser Belag"
    }
}

# 2. Mikroskopie-Informationen
microscope_info = {
    "Fall 1": {"view": "Grampositive Kokken in Haufen, typisch für Staphylokokken", "gram_type": "Gram-positiv", "image": "images/fall1_mikro.png", "sample": "Probe: Eiter aus einer Hautabszess-Läsion"},
    "Fall 2": {"view": "Grampositive Kokken in Ketten, typisch für Streptokokken", "gram_type": "Gram-positiv", "image": "images/fall2_mikro.png", "sample": "Probe: Rachenabstrich"},
    "Fall 3": {"view": "Gramnegative Stäbchen sichtbar", "gram_type": "Gram-negativ", "image": "images/fall3_mikro.png", "sample": "Probe: Mittelstrahlurin"},
    "Fall 4": {"view": "Auffälliges, strukturiertes Ei, passend zu einem Helminthen", "gram_type": "Nicht sinnvoll", "image": "images/fall4_mikro.png", "sample": "Probe: Stuhlprobe"},
    "Fall 5": {"view": "Grampositive Kokken erkennbar", "gram_type": "Gram-positiv, aber unspezifisch", "image": "images/fall5_mikro.png", "sample": "Probe: Abstrich von der Katheterstelle"},
    "Fall 6": {"view": "Sprosszellen und Hyphen, vereinbar mit einem Hefepilz", "gram_type": "Nicht typisch / Pilzverdacht", "image": "images/fall6_mikro.png", "sample": "Probe: Vaginalabstrich"}
}

# 3. Schnelltests
micro_tests = {
    "Fall 1": {"Katalase": "positiv", "Koagulase": "positiv"},
    "Fall 2": {"Katalase": "negativ", "Koagulase": "nicht sinnvoll"},
    "Fall 3": {"Katalase": "nicht zentral", "Koagulase": "nicht sinnvoll"},
    "Fall 4": {"Katalase": "nicht sinnvoll", "Koagulase": "nicht sinnvoll"},
    "Fall 5": {"Katalase": "positiv", "Koagulase": "negativ"},
    "Fall 6": {"Katalase": "nicht primär", "Koagulase": "nicht primär"}
}

# 4. Agarplatten-Texte
plate_text = {
    "Fall 1": {"COS": "Goldene Kolonien mit β-Hämolyse", "MAC": "Kein Wachstum", "CNA": "Wachstum mit β-Hämolyse"},
    "Fall 2": {"COS": "Kleine Kolonien mit starker β-Hämolyse", "MAC": "Kein Wachstum", "CNA": "Wachstum mit β-Hämolyse"},
    "Fall 3": {"COS": "Graue Kolonien", "MAC": "Rosa Kolonien (Laktose+)", "CNA": "Kein Wachstum"},
    "Fall 4": {"COS": "Kein Wachstum", "MAC": "Kein Wachstum", "CNA": "Kein Wachstum"},
    "Fall 5": {"COS": "Weisse Kolonien ohne Hämolyse", "MAC": "Kein Wachstum", "CNA": "Wachstum ohne Hämolyse"},
    "Fall 6": {"COS": "Cremige, weissliche Kolonien", "MAC": "Kein Wachstum", "CNA": "Kaum oder kein Wachstum"}
}

# 5. Blutwerte & Differentialblutbild
blood_values = {
    "Fall 1": {"CRP (mg/L)": 180, "PCT (ng/mL)": 8.5, "Leukos (G/L)": 18, "Laktat (mmol/L)": 4.2, "pH (BGA)": 7.28},
    "Fall 2": {"CRP (mg/L)": 95, "Leukos (G/L)": 14},
    "Fall 3": {"CRP (mg/L)": 35, "Leukos (G/L)": 12},
    "Fall 4": {"CRP (mg/L)": 8, "Leukos (G/L)": 8},
    "Fall 5": {"CRP (mg/L)": 4, "Leukos (G/L)": 9},
    "Fall 6": {"CRP (mg/L)": 20, "Leukos (G/L)": 10}
}

blood_diff = {
    "Fall 1": {"Leukozyten (G/L)": 18, "Neutrophile (%)": 82, "Lymphozyten (%)": 12, "Eosinophile (%)": 1},
    "Fall 2": {"Leukozyten (G/L)": 13, "Neutrophile (%)": 78, "Lymphozyten (%)": 15, "Eosinophile (%)": 1},
    "Fall 3": {"Leukozyten (G/L)": 12, "Neutrophile (%)": 74, "Lymphozyten (%)": 18, "Eosinophile (%)": 1},
    "Fall 4": {"Leukozyten (G/L)": 8, "Neutrophile (%)": 45, "Lymphozyten (%)": 25, "Eosinophile (%)": 18},
    "Fall 5": {"Leukozyten (G/L)": 9, "Neutrophile (%)": 55, "Lymphozyten (%)": 30, "Eosinophile (%)": 2},
    "Fall 6": {"Leukozyten (G/L)": 10, "Neutrophile (%)": 55, "Lymphozyten (%)": 30, "Eosinophile (%)": 6}
}

# 6. Referenzwerte
REF = {
    "CRP (mg/L)": (0, 5), "PCT (ng/mL)": (0, 0.05), "Leukos (G/L)": (4, 10),
    "Troponin (ng/L)": (0, 14), "Glukose (mmol/L)": (3.9, 5.6), "pH (BGA)": (7.35, 7.45), "Laktat (mmol/L)": (0.5, 2.0)
}

REF_BLOOD_DIFF = {
    "Leukozyten (G/L)": (4, 10), "Neutrophile (%)": (40, 75), "Lymphozyten (%)": (20, 45), "Eosinophile (%)": (0, 6)
}

# 7. Lösungen & Diagnosen
solutions = {
    "Fall 1": "Staphylococcus aureus", "Fall 2": "Streptococcus pyogenes",
    "Fall 3": "Escherichia coli", "Fall 4": "Helmintheninfektion",
    "Fall 5": "Staphylococcus epidermidis", "Fall 6": "Candida spp."
}

DIAG_CHOICES = [
    "Staphylococcus aureus", "Staphylococcus epidermidis", "Streptococcus pyogenes",
    "Escherichia coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa",
    "Candida spp.", "Helmintheninfektion", "Giardiasis (Protozoen)",
    "Virale Ursachen", "Akutes Koronarsyndrom", "Diabetische Ketoazidose", "Unklar"
]
