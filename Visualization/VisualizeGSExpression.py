"""
Author:Wang Jingru
data:18/9/17
"""
import pymongo
import chart_studio
import plotly.graph_objs as go
import math


class DataStorage:

    def __init__(self, name):
        self.name = name
        self.path = self.__login()

    def __login(self):
        client = pymongo.MongoClient("127.0.0.1", 27017)
        db = client['Denovo']
        # db.authenticate("tanxian123", "123456")
        collection = client['Denovo'][self.name]
        return collection

    def FindByID(self, ID):
        # print(self.path.find_one({'id': ID}))
        return self.path.find_one({'id': ID})


class GseBox(object):
    def __init__(self):
        pass

    def FindData(self, geneID):
        a = DataStorage("HumanBrain_singleCell_Expression")  # HumanBrain_singleCell_Expression
        allData = a.FindByID(geneID)
        return allData

    def dropx(self, alist):
        res = []
        for item in alist:
            if item == "":
                res.append(0)
            else:
                res.append(item)
        return res

    def normalized(self, alist):
        result = []
        for item in alist:
            if item != 0 and item != "":
                result.append(round(math.log10(float(item) + 1.0), 2))
            else:
                result.append(0)
        return result

    def get_averge(self, alist, normaliaze=False):
        float_alist = []
        for item in alist:
            if item != "":
                float_alist.append(float(item))
            else:
                float_alist.append(float(0))
        result = sum(float_alist) / len(float_alist)

        if normaliaze == False:
            return round(result, 2)
        else:
            return round(math.log10(sum(float_alist) / len(float_alist) + 1), 2)

    def sorted_threelist(self, alist, blist, clist):
        total_list = []
        for item_a, item_b, item_c in zip(alist, blist, clist):
            total_list.append([item_a, item_b, item_c])
        sort_total_list = sorted(total_list, key=lambda x: x[0])
        return [item[0] for item in sort_total_list], [item[1] for item in sort_total_list], [item[2] for item in
                                                                                              sort_total_list]

    def DrawBox(self, allData):
        if allData == None:
            return '<div>There is no corresponding data published yet, we will update it when such data available.  </div>'
        # else:
        try:
            expData = allData['express_data']
            y_normalized_line_data = []
            y_line_data = []
            traces = []
            for item in expData:
                type = item['type']
                data = self.dropx(item['data'])
                period = item['period']
                traces.append(go.Box(
                    y=data,
                    x=[type + " - " + item_item for item_item in period],
                    name=type,
                    boxpoints='outliers',
                    line=dict(width=1),
                ))
            l = len(traces)
            for item in expData:
                type = item['type']
                data = self.normalized(item['data'])
                period = item['period']
                traces.append(go.Box(
                    y=data,
                    x=[type + " - " + item_item for item_item in period],
                    visible=False,
                    name=type,
                    boxpoints='outliers',
                    line=dict(width=1),
                ))
            # line_xaiax = []
            # for item in expData:
            # 	period_set = list(set(item.get('period')))
            # 	for item_item in period_set:
            # 		line_xaiax.append(item.get("type")+"-"+item_item)
            # line_y = []
            # for item in line_xaiax:
            # 	item_list = []
            # 	for item_item in expData:
            # 		if item_item.get("type") == item.split("-")[0]:
            # 			for item_item_item1, item_item_item2 in zip(item_item.get("period"), item_item.get("data")):
            # 				if item_item_item1 == item.split("-")[1]:
            # 					item_list.append(item_item_item2)
            # 	line_y.append(item_list)
            # for item in line_y:
            # 	y_line_data.append(self.get_averge(item))
            # 	y_normalized_line_data.append(self.get_averge(item, True))
            # line_xaiax, y_line_data, y_normalized_line_data = self.sorted_threelist(line_xaiax, y_line_data, y_normalized_line_data)
            # traces.append(
            # 	go.Scatter(
            # 		x=line_xaiax,
            # 		y=y_line_data,
            # 		visible=False,
            # 		text='Unnormalized',
            # 		name='Unnormalized TPM'
            # 	))
            # traces.append(
            # 	go.Scatter(
            # 		x=line_xaiax,
            # 		y=y_normalized_line_data,
            # 		visible=False,
            # 		text='Normalized',
            # 		name='Normalized TPM'
            # 	))
            visible_list_1 = [True] * l
            visible_list_2 = [False] * l
            # visible_list_3 = [False] * l
            for i in range(l):
                visible_list_1.append(False)
                visible_list_2.append(True)
            # visible_list_3.append(False)
            for j in range(2):
                visible_list_1.append(False)
                visible_list_2.append(False)
            # visible_list_3.append(True)
            updatemenus = list([
                dict(type="buttons",
                     active=-1,
                     # direction='left',
                     pad=dict(
                         # l=500,
                         r=30,
                         # b=250,
                         t=20,
                     ),
                     buttons=list([
                         dict(label='original TPM',
                              method='update',
                              args=[{'visible': visible_list_1},
                                    {'title': 'TPM without normalization',
                                     # 'annotations': high_annotations
                                     }]),
                         dict(label='log<sub>10</sub>( TPM + 1 )',
                              method='update',
                              args=[{'visible': visible_list_2},
                                    {'title': 'Normalized TPM',
                                     # 'annotations': low_annotations
                                     }]),
                         # dict(label='Average Line',
                         #   method='update',
                         #   args=[{'visible': visible_list_3},
                         # 		{'title': 'Normalized and Unnormalized average TPM',
                         # 		 # 'annotations': low_annotations
                         # 		 }])
                     ]))])
            layout = go.Layout(
                updatemenus=updatemenus,
                paper_bgcolor='rgb(249, 249, 249)',
                plot_bgcolor='rgb(249, 249, 249)',
                height=400,
                width=1000,
                hovermode='closest',
                xaxis=dict(
                    showgrid=True,
                    zeroline=False,
                    showline=False,
                    showticklabels=True,
                    tickangle=60,
                    titlefont=dict(
                        family='Arial',
                    ),
                ),
                yaxis=dict(
                    titlefont=dict(
                        family='Arial',
                    )

                ),
                margin=dict(
                    l=150,
                    r=10,
                    b=180,
                    t=30,
                ),
                # showlegend=False
            )
            fig = go.Figure(data=traces, layout=layout)
            # plotly.offline.plot(fig, show_link=False)
            return plotly.offline.plot(fig, show_link=False, output_type="div"
                                       # , include_plotlyjs=False
                                       )
        except:
            '<div>Sorry, there may be some problems with the visualization of this data, please give us feedback!</div>'


class EmbryonicExpressPlot(object):
    def __init__(self, id):
        self.id = id

    def run(self):
        gseBox = GseBox()
        allData = gseBox.FindData(self.id)
        return gseBox.DrawBox(allData)


def main():
    mainer = EmbryonicExpressPlot("85358")
    mainer.run()


if __name__ == '__main__':
    main()
