# -*- encoding: utf-8 -*-

class MutationScore(object):

    def __init__(self, message):
        self.message = message

    def get_score(self):
        score_list = []
        for item in self.message:
            if item.get('DNM'):
                for item_item in item.get('DNM'):
                    if item_item.get('Func refGene') in ['exonic', 'exonic;splicing', 'splicing']:
                        # if item_item.get('Exonic Func').startswith("frameshift") or item_item.get(
                        #         'Exonic Func') == 'stopgain' or item_item.get('Exonic Func').startswith("Splice-site"):
                        score = 0
                        if item_item.get('SIFT_pred') == 'D':
                            score += 1
                        if item_item.get('Polyphen2_HDIV_pred') == 'D':
                            score += 1
                        if item_item.get('GERP++_RS') not in ['.', '-', '', None]:
                            if float(item_item.get('GERP++_RS')) >= 5.6:
                                score += 1
                        if item_item.get('CADD_phred') not in ['.', '-', '', None]:
                            if float(item_item.get('CADD_phred')) >= 30:
                                score += 1
                        if item_item.get('ClinVar_SIG') not in ['.', '-', '', None]:
                            if 'pathogenic' in item_item.get('ClinVar_SIG') or 'Pathogenic' in item_item.get(
                                    'ClinVar_SIG'):
                                score += 1
                        if item_item.get('Exonic Func').startswith("frameshift") or item_item.get('Exonic Func').startswith("Splice-site") or item_item.get('Exonic Func') == 'stopgain': #LoF
                            score_list.append('High')
                        else:
                            if item_item.get('Exonic Func') == "nonsynonymous SNV" and score >= 3: #至少被5个工具里3个工具预测为有害的missense
                                score_list.append('High')
                            else:
                                if item_item.get('Exonic Func') == "nonsynonymous SNV" and score >= 1: # 被5个工具里1-2个工具预测为有害的missense
                                    score_list.append('Medium')
                                else:
                                    score_list.append('Low')
        return score_list

    def get_score2(self):
        score_list = []
        for item_item in self.message:
            if item_item.get('Func refGene') in ['exonic', 'exonic;splicing', 'splicing']:
                # if item_item.get('Exonic Func').startswith("frameshift") or item_item.get(
                #         'Exonic Func') == 'stopgain' or item_item.get('Exonic Func').startswith("Splice-site"):
                score = 0
                if item_item.get('SIFT_pred') == 'D':
                    score += 1
                if item_item.get('Polyphen2_HDIV_pred') == 'D':
                    score += 1
                if item_item.get('GERP++_RS') not in ['.', '-', '', None]:
                    if float(item_item.get('GERP++_RS')) >= 5.6:
                        score += 1
                if item_item.get('CADD_phred') not in ['.', '-', '', None]:
                    if float(item_item.get('CADD_phred')) >= 30:
                        score += 1
                if item_item.get('ClinVar_SIG') not in ['.', '-', '', None]:
                    if 'pathogenic' in item_item.get('ClinVar_SIG') or 'Pathogenic' in item_item.get(
                            'ClinVar_SIG'):
                        score += 1
                if item_item.get('Exonic Func').startswith("frameshift") or item_item.get(
                        'Exonic Func').startswith("Splice-site") or item_item.get(
                        'Exonic Func') == 'stopgain':  # LoF
                    score_list.append('High')
                else:
                    if item_item.get(
                            'Exonic Func') == "nonsynonymous SNV" and score >= 3:  # 至少被5个工具里3个工具预测为有害的missense
                        score_list.append('High')
                    else:
                        if item_item.get(
                                'Exonic Func') == "nonsynonymous SNV" and score >= 1:  # 被5个工具里1-2个工具预测为有害的missense
                            score_list.append('Medium')
                        else:
                            score_list.append('Low')
        return score_list