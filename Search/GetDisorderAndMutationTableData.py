# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        FindDisorderByMutation
# @Author:      GuoSijia
# @Purpose:
# @Created:     2018-10-01
# @update:      2018-10-01 11:15
# @Software:    PyCharm
# -------------------------------------------------------------------------------
from Base import DBBase


class DbMappingTable(object):

    def __init__(self):
        pass

    def dmt(self, db_type, table_type):
        if db_type == table_type:
            return True
        elif db_type.startswith(table_type):
            return True
        elif db_type.upper() == table_type.upper():
            return True
        elif db_type.upper().startswith(table_type.upper()):
            return True
        else:
            return False

    def disorder(self, db_str):
        # if db_str == "ASD or SCZ":
        # 	return "Others"
        # elif self.dmt(db_str, "ADHD"):
        # 	return "ADHD"
        # elif self.dmt(db_str, "Autism (ASD)"):
        # 	return "ASD"
        # elif self.dmt(db_str, "BD") or db_str == "Bipolar Disorder" or db_str == "BP":
        # 	return "BD"
        # elif db_str == "Congenital Heart Disease" or self.dmt(db_str, "CHD"):
        # 	return "CHD"
        # elif self.dmt(db_str, "Control"):
        # 	return "Control"
        # elif self.dmt(db_str, "DD"):
        # 	return "DD"
        # elif self.dmt(db_str, "DEE"):
        # 	return "DEE"
        # elif self.dmt(db_str, "EE"):
        # 	return "EE"
        # elif self.dmt(db_str, "ID") or db_str == "Intellectual Disability/Developmental Disability":
        # 	return "ID"
        # elif self.dmt(db_str, "OCD"):
        # 	return "OCD"
        # elif self.dmt(db_str, "PD"):
        # 	return "PD"
        # elif self.dmt(db_str, "SCZ") or db_str == "Schizophrenia":
        # 	return "SCZ"
        # elif db_str == "Tourette Disorder" or self.dmt(db_str, "TS"):
        # 	return "TS"
        # else:
        # 	return "Others"
        if db_str == "Acromelic Frontonasal Dysostosis (AFND)":
            return "AFND"
        elif self.dmt(db_str, "Amyotrophic Lateral Sclerosis (ALS)"):
            return "ALS"
        elif self.dmt(db_str, "Anophthalmia and Microphthalmia (A/M)"):
            return "A/M"
        elif self.dmt(db_str, "Attention Deficit Hyperactivity Disorder (ADHD)") or db_str == 'ADHD':
            return "ADHD"
        elif self.dmt(db_str, "Autism (ASD)") or db_str == 'ASD':
            return "ASD"
        elif self.dmt(db_str, "Bipolar Disorder (BP)") or db_str == 'BD':
            return "BP"
        elif self.dmt(db_str, "Cantu Syndrome (CS)"):
            return "CS"
        elif self.dmt(db_str, "Cerebral Palsy (CP)"):
            return "CP"
        elif self.dmt(db_str, "Congenital Diaphragmatic Hernia (CDH)"):
            return "CDH"
        elif self.dmt(db_str, "Congenital Heart Disease (CHD)"):
            return "CHD"
        elif self.dmt(db_str, "Developmental and Epileptic Encephalopathies (DEE)"):
            return "DEE"
        elif self.dmt(db_str, "Developmental Delay (DD)"):
            return "DD"
        elif self.dmt(db_str, "Early-onset Alzheimer Disorder (eoAD)"):
            return "eoAD"
        elif self.dmt(db_str, "Early-onset High Myopia (eoHM)"):
            return "eoHM"
        elif self.dmt(db_str, "Early-onset Parkinson Disorder (eoPD)"):
            return "eoPD"
        elif self.dmt(db_str, "Epileptic Encephalopathies (EE)"):
            return "EE"
        elif self.dmt(db_str, "Fetal non-Preterm birth (non-PTB)"):
            return "non-PTB"
        elif self.dmt(db_str, "Fetal preterm birth (PTB)"):
            return "PTB"
        elif self.dmt(db_str, "Infantile Spasms (IS)"):
            return "IS"
        elif self.dmt(db_str, "Intellectual disability (ID)") or db_str == 'ID':
            return "ID"
        elif self.dmt(db_str, "Lennox Gastaut Syndrome (LGS)"):
            return "LGS"
        elif self.dmt(db_str, "Mesial Temporal Lobe Epilepsy with Hippocampal Sclerosis (MTLE-HS)"):
            return "MTLE-HS"
        elif self.dmt(db_str, "Mix (Autism or Schizophrenia)"):
            return "ASD or SCZ"
        elif self.dmt(db_str, "Neural Tube Defects (NTD)"):
            return "NTD"
        elif self.dmt(db_str, "Obsessive-Compulsive Disorder (OCD)") or db_str == 'OCD':
            return "OCD"
        elif self.dmt(db_str, "Schizophrenia (SCZ)") or db_str == 'SCZ':
            return "SCZ"
        elif self.dmt(db_str, "Sibling Control"):
            return "Sibling Control"
        elif self.dmt(db_str, "Sotos-like syndrome"):
            return "Sotos-like syndrome"
        elif self.dmt(db_str, "Sporadic Infantile Spasm Syndrome (IS)"):
            return "SISS"
        elif self.dmt(db_str, "Tourette Disorder (TD)"):
            return "TD"
        elif self.dmt(db_str, "Uncharacterized (Mixed healthy control)"):
            return "Mixed healthy control"
        elif self.dmt(db_str, "Control"):
            return "Control"
        else:
            return "Others"

    def coding_mapping(self, m_str):
        if m_str.startswith("frameshift"):
            return "frameshift"
        elif m_str == "stopgain":
            return "nonsense"
        elif m_str.startswith("Splice-site"):
            return "splice-site"
        elif m_str == "start gain":
            return "start gain"
        elif m_str == "stoploss":
            return "stoploss"
        elif m_str == "nonsynonymous SNV":
            return "missense"
        elif m_str == "Non-frameshit" or m_str == "non-frameshit" or m_str == "non frameshit" or m_str.startswith("nonframeshift"):
            return "Non-frameshit"
        elif m_str.startswith("synonymous") or m_str == "synonymous SNV":
            return "synonymous SNV"
        else:
            return "coding-Others"

    def non_coding_mapping(self, m_str):

        if m_str == "intronic":
            return "intronic"
        elif m_str == "UTR3" or m_str == "UTR5":
            return "UTR region"
        elif m_str == "upstream" or m_str == "downstream" or m_str == "upstream;downstream" or m_str == ['upstream',
                                                                                                         'downstream']:
            return "up-down-stream"
        elif m_str == "intergenic" or m_str.startswith("intergenic"):
            return "intergenic"
        elif m_str.startswith("ncRNA"):
            return "ncRNA"
        # elif m_str == "intergenic"
        else:
            return "non-coding-all-Others"

    def cnv(self, m_str):
        if m_str.startswith("Deletion") or m_str in ["deletion", "Deletion", "DEL", "del", 'Del'] or m_str.startswith("Del"):
            return "deletion"
        elif m_str.startswith("Duplication") or m_str in ["Duplication", "duplication", "DUP",
                                                          "dup", 'Dup'] or m_str.startswith("Dup"):
            return "duplication"
        else:
            return "cnv-others"


class GetDisorderAndMutationTableData(object):

    def __init__(self, id):
        self.Gene_db = DBBase.DBBase("Genes")
        self.id = id
        self.mapping = DbMappingTable()

    def get_dam_statics(self):
        mutation_type_list = ["frameshift", "nonsense", "splice-site", "missense", "start gain", "stoploss",
                              "Non-frameshit", "synonymous SNV", "intronic", "UTR region", "up-down-stream",
                              "intergenic", "ncRNA", "coding-Others", "non-coding-all-Others", "deletion",
                              "duplication", "cnv-others", "coding-all", "non-coding-all"]
        disorder_list = ["AFND", "ALS", "A/M", "ADHD", "ASD",
                         "BP", "CS", "CP", "CDH", "CHD", "DEE", "DD", "eoAD", "eoHM", "eoPD", "EE", "non-PTB",
                         "PTB", "IS", "ID", "LGS", "MTLE-HS", "ASD or SCZ", "NTD", "OCD", "SCZ", "Sibling Control",
                         "Sotos-like syndrome",
                         "SISS", "TD", "Mixed healthy control", "Others", "Control"]
        disorder_dict = {
            "all": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "AFND": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ALS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "A/M": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ADHD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                     "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                     "non-coding-all-Others": [],
                     "deletion": [], "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ASD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "BP": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CP": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CDH": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CHD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "DEE": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "DD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoAD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoHM": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoPD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "EE": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                       "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                       "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                       "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                       "coding-all": [], "non-coding-all": []},
            "non-PTB": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                        "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                        "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                        "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                        "coding-all": [], "non-coding-all": []},
            "PTB": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "IS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ID": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "LGS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                     "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                     "non-coding-all-Others": [],
                     "deletion": [], "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "MTLE-HS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ASD or SCZ": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "NTD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "OCD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "SCZ": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Sibling Control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Sotos-like syndrome": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "SISS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "TD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Mixed healthy control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                       "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                       "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                       "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                       "coding-all": [], "non-coding-all": []},
            "Control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                        "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                        "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                        "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                        "coding-all": [], "non-coding-all": []},
            "Others": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                        "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                        "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                        "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                        "coding-all": [], "non-coding-all": []}
            }
        mutation_count = {
            "all": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "AFND": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ALS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "A/M": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ADHD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                     "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                     "non-coding-all-Others": [],
                     "deletion": [], "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ASD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "BP": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CP": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CDH": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "CHD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "DEE": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "DD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoAD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoHM": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "eoPD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "EE": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                   "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                   "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                   "coding-all": [], "non-coding-all": []},
            "non-PTB": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                        "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                        "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                        "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                        "coding-all": [], "non-coding-all": []},
            "PTB": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "IS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ID": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "LGS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                    "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                    "non-coding-all-Others": [],
                    "deletion": [], "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "MTLE-HS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                        "stoploss": [],
                        "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                        "up-down-stream": [],
                        "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                        "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "ASD or SCZ": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                           "stoploss": [],
                           "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                           "up-down-stream": [],
                           "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [],
                           "deletion": [],
                           "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "NTD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "OCD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "SCZ": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                    "stoploss": [],
                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Sibling Control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                                "stoploss": [],
                                "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                                "up-down-stream": [],
                                "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [],
                                "deletion": [],
                                "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Sotos-like syndrome": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [],
                                    "start gain": [],
                                    "stoploss": [],
                                    "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                                    "up-down-stream": [],
                                    "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [],
                                    "deletion": [],
                                    "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "SISS": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                     "stoploss": [],
                     "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                     "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                     "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "TD": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                   "stoploss": [],
                   "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [], "up-down-stream": [],
                   "intergenic": [], "ncRNA": [], "coding-Others": [], "non-coding-all-Others": [], "deletion": [],
                   "duplication": [], "cnv-others": [], "coding-all": [], "non-coding-all": []},
            "Mixed healthy control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [],
                                      "start gain": [],
                                      "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [],
                                      "UTR region": [],
                                      "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                                      "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                                      "coding-all": [], "non-coding-all": []},
            "Control": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [],
                                      "start gain": [],
                                      "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [],
                                      "UTR region": [],
                                      "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                                      "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                                      "coding-all": [], "non-coding-all": []},
            "Others": {"frameshift": [], "nonsense": [], "splice-site": [], "missense": [], "start gain": [],
                       "stoploss": [], "Non-frameshit": [], "synonymous SNV": [], "intronic": [], "UTR region": [],
                       "up-down-stream": [], "intergenic": [], "ncRNA": [], "coding-Others": [],
                       "non-coding-all-Others": [], "deletion": [], "duplication": [], "cnv-others": [],
                       "coding-all": [], "non-coding-all": []}
            }
        if self.Gene_db.find_one_by_one_condition("ENTREZ_ID", self.id):
            dnm_dict = self.Gene_db.find_one_by_one_condition("ENTREZ_ID", self.id).get("DNM")
            cnv_dict = self.Gene_db.find_one_by_one_condition("ENTREZ_ID", self.id).get("CNV")
            # print(cnv_dict)
            # print(cnv_dict)
            # print("Idenx, Disorder, MutationType")
            if dnm_dict != None:
                for index, item in enumerate(dnm_dict):
                    # print(index + 1, end=", ")
                    # print(self.mapping.disorder(item.get("Disorder")), end=", ")
                    if item.get("Func refGene") == 'exonic':
                        # print(self.mapping.coding_mapping(item.get("Exonic Func")), end=" ")
                        # type.append(item.get("Exonic Func"))
                        disorder_dict[self.mapping.disorder(item.get("Disorder"))][
                            self.mapping.coding_mapping(item.get("Exonic Func"))].append(item)
                    # print(self.disorder_dict)
                    else:
                        # print(self.mapping.non_coding_mapping(item.get("Func refGene")), end=" ")
                        disorder_dict[self.mapping.disorder(item.get("Disorder"))][
                            self.mapping.non_coding_mapping(item.get("Func refGene"))].append(item)
            # print()
            if cnv_dict != None:
                for item in cnv_dict:
                    disorder_dict[self.mapping.disorder(item.get("Disorder"))][
                        self.mapping.cnv(item.get("mutation type"))].append(item)
        # print()
        # print(list(set(type)))
        # for item in self.disorder_dict.get("ASD").keys():
        # 	print(self.disorder_dict.get("ASD").get(item))
        # print(len(self.disorder_dict.get("Others").get("duplication")))
        # print(self.disorder_dict.get("Others").get("duplication"))
        # return
        for item in disorder_dict.keys():
            for item_item in ["frameshift", "nonsense", "splice-site", "missense", "start gain", "stoploss",
                              "Non-frameshit", "synonymous SNV"]:
                for item_item_item in disorder_dict[item][item_item]:
                    disorder_dict[item]["coding-all"].append(item_item_item)
            for item_item in ["intronic", "UTR region", "up-down-stream", "intergenic", "ncRNA"]:
                for item_item_item in disorder_dict[item][item_item]:
                    disorder_dict[item]["non-coding-all"].append(item_item_item)
        for item in disorder_dict.keys():
            # print(item)
            for item_item in disorder_dict.get(item).keys():
                mutation_count[item][item_item] = len(disorder_dict[item][item_item])
        for m_item in mutation_type_list:
            for d_itme in disorder_list:
                for item_item1 in disorder_dict[d_itme][m_item]:
                    disorder_dict["all"][m_item].append(item_item1)
                # for item_item2 in mutation_count[d_itme][m_item]:
                mutation_count["all"][m_item] = len(disorder_dict["all"][m_item])

        return disorder_dict, mutation_count


if __name__ == '__main__':
    # m_str = "Del"
    # if m_str == "Deletion" or m_str.startswith("Deletion") or m_str == "deletion":
    #     print(True)
    # else:
    #     print(False)
    find = GetDisorderAndMutationTableData("2994")
    disorder_dict, mutation_count = find.get_dam_statics()
    # print(mutation_count.get("all"))
    # print(disorder_dict.get("all").get("deletion"))
    # for item in disorder_dict.get("all").keys():
    #     print(disorder_dict.get("all").get(item))
# # for item in mutation_count.keys():
# # 	print(item, end=" ")
# # 	print(mutation_count[item])
# # print(mutation_count.get("all").get("nonsense"))
# print(mutation_count.get("ASD").get("non-coding-all"))
# print(disorder_dict.get("ASD").get("non-coding-all"))
# for item in disorder_dict.get("ASD").get("non-coding-all"):
# 	print(item)
# print(mutation_count.get("ASD").get("nonsense"))
# print(mutation_count.get("ASD").get("splice-site"))
# print(mutation_count.get("ASD").get("missense"))
# print(mutation_count.get("ASD").get("start gain"))
# print(mutation_count.get("ASD").get("stoploss"))
# print(mutation_count.get("ASD").get("Non-frameshit") )
# print(mutation_count.get("ASD").get("synonymous SNV"))
#
#
# print(mutation_count.get("ASD").get("frameshift") + mutation_count.get("ASD").get("nonsense") + mutation_count.get("ASD").get("splice-site")+ mutation_count.get("ASD").get("missense")+ mutation_count.get("ASD").get("start gain")+ mutation_count.get("ASD").get("stoploss")+ mutation_count.get("ASD").get("Non-frameshit") + mutation_count.get("ASD").get("synonymous SNV"))
