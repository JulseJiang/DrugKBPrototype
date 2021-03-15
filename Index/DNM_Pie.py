# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        Pie
# @Author:      GuoSijia
# @Purpose:     
# @Created:     2018-10-28
# @update:      2018-10-28 14:14
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly
import sys


class DNMPie(object):

    def __init__(self):
        pass

    def get_pie(self):
        fig = {
            'data': [
                {
                    'labels': ["Attention Deficit Hyperactivity Disorder (ADHD)",
                               "Autism (ASD)",
                               "Mix (Autism or Schizophrenia)",
                               "Bipolar Disorder (BP)",
                               "Developmental Delay (DD)",
                               "Intellectual Disability (ID)",
                               "Obsessive-Compulsive Disorder (OCD)",
                               "Schizophrenia (SCZ)",
                               "Tourette Disorder (TD)"],
                    'values': [6, 312167, 4931, 75, 8513, 2585, 262, 3610, 850],
                    'type': 'pie',
                    'name': 'Psychiatric Disorder',
                    # 'marker': {'colors': ['rgb(56, 75, 126)',
                    #                       'rgb(18, 36, 37)',
                    #                       'rgb(34, 53, 101)',
                    #                       'rgb(36, 55, 57)',
                    #                       'rgb(6, 4, 4)']},
                    'domain': {'x': [0, .48],
                               'y': [.51, 1]},
                    'hoverinfo': 'label+value+name',
                    'textinfo': 'none',
                    "hole": .4,
                },
                {
                    'labels': ["Amyotrophic Lateral Sclerosis (ALS)", "Cerebral Palsy (CP)",
                               "Developmental and Epileptic Encephalopathies (DEE)",
                               "Early-onset Alzheimer Disorder (eoAD)",
                               "Early-onset High Myopia (eoHM)", "Early-onset Parkinson Disorder (eoPD)",
                               "Epileptic Encephalopathies (EE)", "Infantile Spasms (IS)",
                               "Lennox Gastaut Syndrome (LGS)",
                               "Mesial Temporal Lobe Epilepsy with Hippocampal Sclerosis (MTLE-HS)",
                               "Neural Tube Defects (NTD)"],
                    'values': [111, 61, 508, 24, 20, 20, 564, 260, 174, 18, 40],
                    # 'marker': {'colors': ['rgb(177, 127, 38)',
                    #                       'rgb(205, 152, 36)',
                    #                       'rgb(99, 79, 37)',
                    #                       'rgb(129, 180, 179)',
                    #                       'rgb(124, 103, 37)']},
                    'type': 'pie',
                    'name': 'neurological disorde',
                    'domain': {'x': [.52, 1],
                               'y': [.51, 1]},
                    'hoverinfo': 'label+value+name',
                    'textinfo': 'none',
                    "hole": .4,

                },
                {
                    'labels': ["Acromelic Frontonasal Dysostosis (AFND)", "Anophthalmia and Microphthalmia (A/M)",
                               "Cantu Syndrome (CS)", "Congenital Diaphragmatic Hernia (CDH)",
                               "Congenital Heart Disease (CHD)"],
                    'values': [4, 4, 11, 40, 1884],
                    'marker': {'colors': ['rgb(33, 75, 99)',
                                          'rgb(79, 129, 102)',
                                          'rgb(36, 73, 147)',
                                          'rgb(175, 49, 35)',
                                          'rgb(151, 179, 100)']},
                    'type': 'pie',
                    'name': 'birth defect',
                    'domain': {'x': [0, .48],
                               'y': [0, .49]},
                    'hoverinfo': 'label+value+name',
                    'textinfo': 'none',
                    "hole": .4,
                },
                {
                    'labels': ["Fetal non-Preterm birth (non-PTB)", "Fetal preterm birth (PTB)", "Sibling Control",
                               "Uncharacterized (Mixed healthy control)"],
                    'values': [22985, 13456, 162800, 340192],
                    'marker': {'colors': ['rgb(146, 123, 21)',
                                          'rgb(177, 180, 34)',
                                          'rgb(206, 206, 40)',
                                          'rgb(175, 51, 21)',
                                          'rgb(35, 36, 21)']},
                    'type': 'pie',
                    'name': 'control study',
                    'domain': {'x': [.52, 1],
                               'y': [0, .49]},
                    'hoverinfo': 'label+value+name',
                    'textinfo': 'none',
                    "hole": .4,
                }
            ],
            'layout': {
                "height": 420,
                "width": 500,
                "margin": {
                    "l": 1,
                    "r": 1,
                    "b": 20,
                    "t": 38
                },
                # "legend": {
                # 	"orientation": "h"
                # },
                'title': '<b>DNM Statistics</b>',
                'showlegend': False,
                "annotations": [
                    {
                        "font": {
                            "size": 12
                        },
                        "showarrow": False,
                        "text": "<b>Psychiatric Disorder<br>DNM<br>Total:332,999</b>",
                        "x": 0.11,
                        "y": 0.79
                    },
                    {
                        "font": {
                            "size": 12
                        },
                        "showarrow": False,
                        "text": "<b>Neurological Disorder<br>DNM<br>Total:180,0</b>",
                        "x": 0.92,
                        "y": 0.79
                    },
                    {
                        "font": {
                            "size": 12
                        },
                        "showarrow": False,
                        "text": "<b>Birth Defect<br>DNM<br>Total:194,3</b>",
                        "x": 0.16,
                        "y": 0.20
                    },
                    {
                        "font": {
                            "size": 12
                        },
                        "showarrow": False,
                        "text": "<b>Control Study<br>DNM<br>Total:539,433</b>",
                        "x": 0.85,
                        "y": 0.20
                    },
                ]
            }
        }

        # plotly.offline.plot(fig, show_link=False)
        # print(sys.getsizeof(plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)))
        # print('-------------')
        # print(sys.getsizeof(plotly.offline.plot(fig, show_link=False, output_type="div")))
        return plotly.offline.plot(fig, show_link=False, output_type="div", include_plotlyjs=False)


if __name__ == '__main__':
    pie = DNMPie()
    pie.get_pie()
