# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        line_cnv
# @Author:      WangJingru
# @Purpose:     
# @Created:     2018/5/22
# @update:      2018/5/22 10:08
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import pymongo
import plotly.graph_objs as go
import plotly.offline as py
from itertools import chain
import json


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
        x = self.path.find_one({'ENTREZ_ID': ID})
        return x


class Cnv_gene:
    def __init__(self):
        pass

    def get_index(self, alist, target):
        for index, item in enumerate(alist):
            if target == item:
                return index + 1

    def get_chrlist(self, chr, filepath="/var/www/Flask/Visualization/gene_sort.json"):
    # def get_chrlist(self, chr, filepath="F:\\PsyMuKB.net\\code\\PsyMuKB_v3.6\\Visualization\\gene_sort.json"):
        with open(filepath) as f:
            g_dict = json.loads(f.read())
        chr_list = g_dict.get(chr)
        return chr_list

    def bubbleSort(self, chr, nums):
        chr_list = self.get_chrlist(chr)
        for i in range(len(nums) - 1):  # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(nums) - i - 1):  # ｊ为列表下标
                if self.get_index(chr_list, nums[j]) != None and self.get_index(chr_list, nums[j + 1]) != None:
                    if self.get_index(chr_list, nums[j]) > self.get_index(chr_list, nums[j + 1]):
                        nums[j], nums[j + 1] = nums[j + 1], nums[j]
                else:
                    pass
        return nums

    def get_len(self, cnv_x_list):
        alist = []
        for item in cnv_x_list:
            for item_item in item:
                alist.append(item_item)
        alist = list(set(alist))
        return len(alist)

    def cnv_gene(self, cnv):
        Symbol = cnv['Symbol']
        """
        number_cnv:找到的cnv总数
        """
        colors = []
        cnvID = []
        geneSymbol = []
        number_cnv = 0
        dis_list = []
        patient_list = []

        for item in cnv['CNV']:
            cnvID.append(item['CNV_ID'])
            geneSymbol.append(item['genesymbol'])
            dis_list.append(item.get("Disorder"))
            patient_list.append(item.get("Patient ID"))

        """
        重复的CNV去重
        """

        del_cnvID = []
        del_geneSymbol = []
        for item in cnvID:
            if str(item).lower() not in del_cnvID:
                number_cnv += 1
                del_cnvID.append(str(item).lower())
                loc = cnvID.index(item)
                del_geneSymbol.append(geneSymbol[loc])
                if str(item).lower().endswith('del'):
                    colors.append("rgba(" + str(199) + "," + str(21) + "," + str(133) + ",1)")
                else:
                    colors.append("rgba(" + str(109) + "," + str(90) + "," + str(205) + ",1)")

        """
        location:搜索基因所在的最远位置；
        x:x轴坐标名称；
        """
        location = 0
        for item in del_geneSymbol:
            cut_str = item
            gene_location = cut_str.index(Symbol)
            if location < gene_location:
                location = gene_location
            if location < (len(cut_str) - gene_location - 1):
                location = (len(cut_str) - gene_location - 1)

        """
        loc:当前CNV中的gene位置；
        以搜索基因为中心，左右补“”；
        min:空格最少的
        """
        min = []
        list_gene_of_cnv = []
        list_y_cnv = []
        time = 0
        for item in del_geneSymbol:
            num = 0
            list_eachCNV = []
            list_eachY = []
            cut_str = item
            """
            cut_str去重
            """
            quchong = []
            [quchong.append(t) for t in cut_str if not t in quchong]
            quchong = self.bubbleSort(cnvID[0].split(":")[0], quchong)
            loc = quchong.index(Symbol)
            if loc < location:
                for i in range(location - loc):
                    list_eachCNV.append("")
                    list_eachY.append("")
                    num += 1
            for j in range(len(quchong)):
                list_eachCNV.append(quchong[j])
                list_eachY.append(time)
            time += 1
            if len(list_eachCNV) < (location * 2):
                for k in range(location * 2 - len(list_eachCNV)):
                    list_eachCNV.append("")
                    list_eachY.append("")
            min.append(num)
            list_gene_of_cnv.append(list_eachCNV)
            list_y_cnv.append(list_eachY)

        """
        找到前面空格最少的那条cnv
        和第一条cnv交换
        """
        min_null = min[0]
        index = 0
        for item in min:
            if item < min_null:
                min_null = item
                index = min.index(item)

        """
        最前面的要第一个画，不然会按照第一条cnv的横坐标画图
        """
        if index != 0:
            temp = list_gene_of_cnv[index]
            list_gene_of_cnv[index] = list_gene_of_cnv[0]
            list_gene_of_cnv[0] = temp
            temp_y = list_y_cnv[index]
            list_y_cnv[index] = list_y_cnv[0]
            list_y_cnv[0] = temp_y

        """
        colors:每条线的颜色
        labels:每条线的标签（纵坐标）
        line_size:每条线的宽度
        list_gene_of_cnv:横坐标数据
        y_data:纵坐标数据
        """
        labels = []
        line_size = []
        y_data = []
        mode_size = []
        for i in range(number_cnv):
            labels.append("cnv" + str(i) + ":")
            line_size.append(6)
            l_y = []
            for j in range(location * 2):
                l_y.append(i)
            y_data.append(l_y)
            mode_size.append(6)

        traces = []
        for i in range(0, number_cnv):
            traces.append(go.Scatter(
                x=list_gene_of_cnv[i],
                y=list_y_cnv[i],
                xaxis='x1',
                yaxis='y1',
                mode='markers',
                marker=dict(color=colors[i], size=mode_size[i], symbol='square'),
                hoverinfo='x',
                name=dis_list[i],
            ))
        traces.append(go.Scatter(
            x=[Symbol],
            y=[number_cnv],
            mode='markers+text',
            text='X-axis of gene pos',
            textposition='right',
            xaxis='x1',
            yaxis='y1',
            marker=dict(color="black", size=10, symbol='triangle-down'),
            hoverinfo='text',
            hoveron="points+fills",
            hovertext='the position of gene on the X-axis'
        ))
        traces.append(go.Scatter(
            x=[Symbol, Symbol],
            y=[number_cnv, 0],
            mode='lines',
            text='X-axis of gene pos',
            textposition='bottom',
            marker=dict(color="black", size=3, symbol='hash-dot'),
            hoverinfo='text',
            # hoveron="points+fills",
            hovertext='the position of gene on the X-axis'
        ))

        annotations = []
        i = 0
        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot
            annotations.append(dict(xref='paper', x=0.02, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text=dis_list[i] + ":" + patient_list[i] + " " + del_cnvID[i],
                                    font=dict(family='Arial',
                                              size=10,
                                              color=colors, ),
                                    # tickangle=-40,
                                    showarrow=False))
            i += 1
        annotations.append(dict(xref='paper', x=0.02, y=[number_cnv],
                                xanchor='right', yanchor='middle',
                                text="<b>Phenotype:PatientID Location:VariantType<b>",
                                font=dict(family='Arial',
                                          size=10,
                                          color=colors, ),
                                # tickangle=-40,
                                showarrow=False))

        if len(traces) <= 2:
            layout_height = 200
        elif len(traces) <= 6:
            layout_height = len(traces) * 60
        else:
            layout_height = len(traces) * 30

        if self.get_len(list_gene_of_cnv) < 50:
            layout_weight = 850
        elif self.get_len(list_gene_of_cnv) < 100:
            layout_weight = 1320
        else:
            layout_weight = 6 * self.get_len(list_gene_of_cnv) + 600
        layout = go.Layout(
            paper_bgcolor='rgb(249, 249, 249)',
            plot_bgcolor='rgb(249, 249, 249)',
            height=layout_height,
            width=layout_weight,
            margin=go.Margin(
                l=200,
                r=0,
                t=20,
                b=80,
                pad=0
            ),
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='rgb(204, 204, 204)',
                linewidth=4,
                autotick=True,
                tickfont=dict(size=8),
                tickangle=70,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=True,
            showlegend=False,
            hovermode='closest',

        )
        layout['annotations'] = annotations

        fig = go.Figure(data=traces, layout=layout)
        # plotly.offline.plot(fig, show_link=False)
        try:
            # plotly.offline.plot(fig, show_link=False)
            return py.plot(fig, show_link=False, output_type="div"
                           # , include_plotlyjs=False
                           )
        except:
            return '<div><p>There is no corresponding data published yet,we will update it when such data available.</p></div>'


class Cnv_gene_double:
    def __init__(self):
        pass

    def get_index(self, alist, target):
        error_dic = {'C22orf25': 'TANGO2', 'C22orf29': 'RTL10', 'CDC45L': 'CDC45', 'DGCR14': 'ESS2',
                     'FLJ39582': 'THAP7-AS1'}
        flag = False
        if target in error_dic.keys():
            for index, item in enumerate(alist):
                if item == error_dic.get(target):
                    flag = True
                    return index + 1
        else:
            for index, item in enumerate(alist):
                if target == item:
                    flag = True
                    return index + 1
        if flag == False:
            return None

    def get_chrlist(self, chr, filepath="/var/www/Flask/Visualization/gene_sort.json"):
    # def get_chrlist(self, chr, filepath="F:\\PsyMuKB.net\\code\\PsyMuKB_v3.6\\Visualization\\gene_sort.json"):
        with open(filepath) as f:
            g_dict = json.loads(f.read())
        chr_list = g_dict.get(chr)
        return chr_list

    def bubbleSort(self, chr, nums):
        chr_list = self.get_chrlist(chr)
        for i in range(len(nums) - 1):  # 这个循环负责设置冒泡排序进行的次数
            for j in range(len(nums) - i - 1):  # ｊ为列表下标
                if self.get_index(chr_list, nums[j]) != None and self.get_index(chr_list, nums[j + 1]) != None:
                    if self.get_index(chr_list, nums[j]) > self.get_index(chr_list, nums[j + 1]):
                        nums[j], nums[j + 1] = nums[j + 1], nums[j]
                else:
                    pass
        return nums

    def get_len(self, cnv_x_list, cnv_x2_list):
        alist = []
        for item in chain(cnv_x_list, cnv_x2_list):
            for item_item in item:
                alist.append(item_item)
        alist = list(set(alist))
        return len(alist)

    def cnv_gene(self, id, f, ppi):
        Symbol = ppi['Symbol']

        """
        **************************1.找出所有control的数据********************************
        **************************2.其他全都归为case的数据*******************************
        x_cnvID：存储找到的cnv名称
        x_geneSymbol：存储和cnv名称对应的geneSymbol段
        x_colors：存储颜色值，用于区分del和dup类型
        x_number_cnv：用于存储cnv条数
        """

        control_cnvID = []
        control_colors = []
        control_number_cnv = 0
        control_geneSymbol = []
        case_cnvID = []
        case_colors = []
        case_number_cnv = 0
        case_geneSymbol = []
        dis_list = []
        patient_list = []

        for item in ppi['CNV']:
            if item['Disorder'] == 'Control':
                control_cnvID.append(item['CNV_ID'])
                control_geneSymbol.append(item['genesymbol'])
                dis_list.append(item.get("Disorder"))
                patient_list.append(item.get("Patient ID"))
        for item in ppi['CNV']:
            if item.get('Disorder') != 'Control':
                case_cnvID.append(item['CNV_ID'])
                case_geneSymbol.append(item['genesymbol'])
                dis_list.append(item.get("Disorder"))
                patient_list.append(item.get("Patient ID"))

        if control_cnvID != []:
            chrom = control_cnvID
        else:
            chrom = case_cnvID
        """
        cnv去重，并按照del dup类型给定颜色值作为区分
        """
        if control_cnvID != []:
            del_control_cnvID = []
            del_control_geneSymbol = []
            for item in control_cnvID:
                if str(item).lower() not in del_control_cnvID:
                    control_number_cnv += 1
                    del_control_cnvID.append(str(item).lower())
                    loc = control_cnvID.index(item)
                    del_control_geneSymbol.append(control_geneSymbol[loc])
                    if str(item).lower().endswith('del'):
                        control_colors.append("rgba(" + str(199) + "," + str(21) + "," + str(133) + ",1)")
                    else:
                        control_colors.append("rgba(" + str(109) + "," + str(90) + "," + str(205) + ",1)")
        if case_cnvID != []:
            del_case_cnvID = []
            del_case_geneSymbol = []
            for item in case_cnvID:
                if str(item).lower() not in del_case_cnvID:
                    case_number_cnv += 1
                    del_case_cnvID.append(str(item).lower())
                    loc = case_cnvID.index(item)
                    del_case_geneSymbol.append(case_geneSymbol[loc])
                    if str(item).lower().endswith('del'):
                        case_colors.append("rgba(" + str(199) + "," + str(21) + "," + str(133) + ",1)")
                    else:
                        case_colors.append("rgba(" + str(109) + "," + str(90) + "," + str(205) + ",1)")

        """
        location:搜索基因所在的最远位置；
        x:x轴坐标名称；
        """
        control_location = 0
        for item in del_control_geneSymbol:
            cut_str = item
            gene_location = cut_str.index(Symbol)
            if control_location < gene_location:
                control_location = gene_location
            if control_location < (len(cut_str) - gene_location - 1):
                control_location = (len(cut_str) - gene_location - 1)

        case_location = 0
        for item in del_case_geneSymbol:
            cut_str = item
            if len(cut_str) != 0:
                case_location = 1
            gene_location = cut_str.index(Symbol)
            if case_location < gene_location:
                case_location = gene_location
            if case_location < (len(cut_str) - gene_location - 1):
                case_location = (len(cut_str) - gene_location - 1)

        """
        time是y轴坐标值
        """
        time = 0
        """
        loc:当前CNV中的gene位置；
        以搜索基因为中心，左右补“”；
        min:空格最少的
        """
        control_min = []
        control_list_gene_of_cnv = []
        control_list_y_cnv = []

        for item in del_control_geneSymbol:
            num = 0
            list_eachCNV = []
            list_eachY = []
            cut_str = item
            """
            cut_str去重
            """
            quchong = []
            chr_list = self.get_chrlist(chrom[0].split(":")[0])
            [quchong.append(t) for t in cut_str if (not t in quchong and t in chr_list)]
            quchong = self.bubbleSort(chrom[0].split(":")[0], quchong)
            loc = quchong.index(Symbol)
            if loc < control_location:
                for i in range(control_location - loc):
                    list_eachCNV.append("")
                    list_eachY.append("")
                    num += 1
            for j in range(len(quchong)):
                list_eachCNV.append(quchong[j])
                list_eachY.append(time)
            time += 1
            if len(list_eachCNV) < (control_location * 2):
                for k in range(control_location * 2 - len(list_eachCNV)):
                    list_eachCNV.append("")
                    list_eachY.append("")
            control_min.append(num)
            control_list_gene_of_cnv.append(list_eachCNV)
            control_list_y_cnv.append(list_eachY)

        case_min = []
        case_list_gene_of_cnv = []
        case_list_y_cnv = []

        for item in del_case_geneSymbol:
            num = 0
            list_eachCNV = []
            list_eachY = []
            cut_str = item
            """
            cut_str去重
            """
            quchong = []
            chr_list = self.get_chrlist(chrom[0].split(":")[0])
            [quchong.append(t) for t in cut_str if (not t in quchong and t in chr_list)]
            quchong = self.bubbleSort(chrom[0].split(":")[0], quchong)
            loc = quchong.index(Symbol)
            if loc < case_location:
                for i in range(case_location - loc):
                    list_eachCNV.append("")
                    list_eachY.append("")
                    num += 1
            for j in range(len(quchong)):
                list_eachCNV.append(quchong[j])
                list_eachY.append(time)
            time += 1
            if len(list_eachCNV) < (case_location * 2):
                for k in range(case_location * 2 - len(list_eachCNV)):
                    list_eachCNV.append("")
                    list_eachY.append("")
            case_min.append(num)
            case_list_gene_of_cnv.append(list_eachCNV)
            case_list_y_cnv.append(list_eachY)
        """
        找到前面空格最少的那条cnv
        和第一条cnv交换
        """
        control_min_null = control_min[0]
        control_index = 0
        for item in control_min:
            if item < control_min_null:
                control_min_null = item
                control_index = control_min.index(item)

        case_min_null = case_min[0]
        case_index = 0
        for item in case_min:
            if item < case_min_null:
                case_min_null = item
                case_index = case_min.index(item)

        """
        找到最前面的那个，第一个画
        """
        del_cnvID = del_control_cnvID + del_case_cnvID
        labels = []
        line_size = []
        y_data = []
        mode_size = []
        traces = []
        """
        先画case
        """
        if control_index >= case_index:
            colors = case_colors + control_colors
            if case_index != 0:
                temp = case_list_gene_of_cnv[case_index]
                case_list_gene_of_cnv[case_index] = case_list_gene_of_cnv[0]
                case_list_gene_of_cnv[0] = temp
                temp_y = case_list_y_cnv[case_index]
                case_list_y_cnv[case_index] = case_list_y_cnv[0]
                case_list_y_cnv[0] = temp_y

            """
            labels:每条线的标签（纵坐标）
            line_size:每条线的宽度
            list_gene_of_cnv:横坐标数据
            y_data:纵坐标数据
            """
            labels = []
            line_size = []
            y_data = []
            mode_size = []

            """
            画纵坐标：先画control 再画case
            """
            for i in range(control_number_cnv):
                labels.append("cnv" + str(i) + ":")
                line_size.append(6)
                l_y = []
                for j in range(control_location * 2):
                    l_y.append(i)
                y_data.append(l_y)
                mode_size.append(6)
            """
            middle_y:找到中间空格的位置
            """
            middle_y = y_data[len(y_data) - 1][0] + 3

            for i in range(case_number_cnv):
                labels.append("cnv" + str(i) + ":")
                # colors.append("rgba(" + str(74) + "," + str(112) + "," + str(139) + ",1)")
                line_size.append(6)
                l_y = []
                for j in range(case_location * 2):
                    l_y.append(i + middle_y)
                y_data.append(l_y)
                mode_size.append(6)

            """
            所有都是control占用 0-->i行； case占用 i+1--> n 行；
            """
            for i in range(0, control_number_cnv):
                traces.append(go.Scatter(
                    x=control_list_gene_of_cnv[i],
                    y=control_list_y_cnv[i],
                    xaxis='x1',
                    yaxis='y1',
                    mode='markers',
                    marker=dict(color=control_colors[i], size=mode_size[i + middle_y - 2], symbol='square'),
                    hoverinfo='x',
                    name=dis_list[i]
                ))

            for i in range(0, case_number_cnv):
                linshi_y = case_list_y_cnv[i]
                y_list = []
                for item in linshi_y:
                    if item != '':
                        y_list.append(int(item) + 2)
                    else:
                        y_list.append('')
                traces.append(go.Scatter(
                    x=case_list_gene_of_cnv[i],
                    y=y_list,
                    xaxis='x1',
                    yaxis='y1',
                    mode='markers',
                    marker=dict(color=case_colors[i], size=mode_size[i], symbol='square'),
                    hoverinfo='x',
                    name=dis_list[control_number_cnv + i]
                ))

            traces.append(go.Scatter(
                x=[Symbol],
                y=[case_number_cnv + middle_y],
                mode='markers+text',
                text='X-axis of gene pos',
                textposition='bottom',
                xaxis='x1',
                yaxis='y1',
                marker=dict(color="black", size=10, symbol='triangle-down'),
                hoverinfo='text',
                hoveron="points+fills",
                hovertext='the position of gene on the X-axis'
            ))
            traces.append(go.Scatter(
                x=[Symbol, Symbol],
                y=[case_number_cnv + middle_y, 0],
                mode='lines',
                text='X-axis of gene pos',
                textposition='bottom',
                marker=dict(color="black", size=3, symbol='hash-dot'),
                hoverinfo='text',
                # hoveron="points+fills",
                hovertext='the position of gene on the X-axis'
            ))
        else:
            """
            先画control
            """

            colors = control_colors + case_colors
            if control_index != 0:
                temp = control_list_gene_of_cnv[control_index]
                control_list_gene_of_cnv[control_index] = control_list_gene_of_cnv[0]
                control_list_gene_of_cnv[0] = temp
                temp_y = control_list_y_cnv[control_index]
                control_list_y_cnv[control_index] = control_list_y_cnv[0]
                control_list_y_cnv[0] = temp_y

            """
            colors:每条线的颜色
            labels:每条线的标签（纵坐标）
            line_size:每条线的宽度
            list_gene_of_cnv:横坐标数据
            y_data:纵坐标数据
            """
            """
            画纵坐标：先画control 再画case
            """
            for i in range(control_number_cnv):
                labels.append("cnv" + str(i) + ":")
                line_size.append(6)
                l_y = []
                for j in range(control_location * 2):
                    l_y.append(i)
                y_data.append(l_y)
                mode_size.append(6)
            """
            middle_y:找到中间空格的位置
            """
            middle_y = y_data[len(y_data) - 1][0] + 3

            for i in range(case_number_cnv):
                labels.append("cnv" + str(i) + ":")
                line_size.append(6)
                l_y = []
                for j in range(case_location * 2):
                    l_y.append(i + middle_y)
                y_data.append(l_y)
                mode_size.append(6)

            """
            画散点：先画control 再画case
            """
            for i in range(0, case_number_cnv):
                linshi_y = case_list_y_cnv[i]
                y_list = []
                for item in linshi_y:
                    if item != '':
                        y_list.append(int(item) + 2)
                    else:
                        y_list.append('')

                traces.append(go.Scatter(
                    x=case_list_gene_of_cnv[i],
                    y=y_list,
                    # xaxis='x1',
                    # yaxis='y1',
                    mode='markers',
                    marker=dict(color=case_colors[i], size=mode_size[i + middle_y - 2], symbol='square'),
                    hoverinfo='x',
                    name=dis_list[control_number_cnv + i]
                ))

            for i in range(0, control_number_cnv):
                traces.append(go.Scatter(
                    x=control_list_gene_of_cnv[i],
                    y=control_list_y_cnv[i],
                    # xaxis='x1',
                    # yaxis='y1',
                    mode='markers',
                    marker=dict(color=control_colors[i], size=mode_size[i], symbol='square'),
                    hoverinfo='x',
                    name=dis_list[i]
                ))

            traces.append(go.Scatter(
                x=[Symbol],
                y=[case_number_cnv + middle_y],
                mode='markers+text',
                text='X-axis of gene pos',
                textposition='bottom',
                marker=dict(color="black", size=10, symbol='triangle-down'),
                hoverinfo='text',
                hoveron="points+fills",
                hovertext='the position of gene on the X-axis'
            ))

            traces.append(go.Scatter(
                x=[Symbol, Symbol],
                y=[case_number_cnv + middle_y, 0],
                mode='lines',
                text='X-axis of gene pos',
                textposition='bottom',
                marker=dict(color="black", size=3, symbol='hash-dot'),
                hoverinfo='text',
                # hoveron="points+fills",
                hovertext='the position of gene on the X-axis'
            ))
        total_list = []
        for index, itemss in enumerate(traces):
            for index2, itemss_itemss in enumerate(itemss.get("x")):
                if itemss_itemss != "" and itemss not in total_list:
                    total_list.append(itemss_itemss)
        total_list = self.bubbleSort(chrom[0].split(":")[0], total_list)
        traces1 = []
        traces1.append(go.Scatter(
            x=total_list,
            y=[""] * len(total_list),
            mode='markers',
        ))
        for item in traces:
            traces1.append(item)
        del traces

        if len(traces1) <= 2:
            layout_height = 450
        elif len(traces1) <= 6:
            layout_height = len(traces1) * 90
        elif len(traces1) <= 10:
            layout_height = len(traces1) * 40
        else:
            layout_height = len(traces1) * 30
        if self.get_len(control_list_gene_of_cnv, case_list_gene_of_cnv) < 50:
            layout_weight = 800
        elif self.get_len(control_list_gene_of_cnv, case_list_gene_of_cnv) < 100:
            layout_weight = 1300
        else:
            layout_weight = 6 * self.get_len(control_list_gene_of_cnv, case_list_gene_of_cnv) + 500

        layout = go.Layout(
            height=layout_height,
            width=layout_weight,
            paper_bgcolor='rgb(249, 249, 249)',
            plot_bgcolor='rgb(249, 249, 249)',
            margin=go.Margin(
                l=200,
                r=0,
                t=0,
                b=80,
                pad=0
            ),
            xaxis=dict(
                showline=True,
                showgrid=False,
                linecolor='rgb(204, 204, 204)',
                linewidth=4,
                autotick=True,
                tickfont=dict(size=7),
                tickangle=70,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
            ),
            autosize=True,
            showlegend=False,
            hovermode='closest',
        )

        annotations = []
        i = 0
        # Adding labels
        for y_trace, label, color in zip(y_data, labels, colors):
            # labeling the left_side of the plot

            annotations.append(dict(xref='paper', x=0.02, y=y_trace[0],
                                    xanchor='right', yanchor='middle',
                                    text=dis_list[i] + ":" + patient_list[i] + " " + del_cnvID[i],
                                    font=dict(family='Arial',
                                              size=8,
                                              color=colors),
                                    showarrow=False))
            i += 1
        annotations.append(dict(xref='paper', x=0.02, y=[case_number_cnv + middle_y],
                                xanchor='right', yanchor='middle',
                                text="<b>Phenotype:PatientID Location:VariantType<b>",
                                font=dict(family='Arial',
                                          size=10,
                                          color=colors, ),
                                # tickangle=-40,
                                showarrow=False))

        layout['annotations'] = annotations

        fig = go.Figure(data=traces1, layout=layout)

        # plotly.offline.plot(fig, show_link=False)
        try:
            # plotly.offline.plot(fig, show_link=False)
            return py.plot(fig, show_link=False, output_type="div"
                           # , include_plotlyjs=False
                           )
        # py.plot(fig, show_link=False, filename="biogrid_PPI.html")
        except:
            return '<div><p>There is no corresponding data published yet,we will update it when such data available.</p></div>'


class Main:
    def __init__(self):
        pass

    def run(self, id):
        cg = Cnv_gene_double()
        dan_cg = Cnv_gene()
        f = DataStorage("Genes")
        data = f.FindByID(str(id))
        if data != None:
            if 'CNV' in data.keys():
                case_f = 0
                control_f = 0
                for item in data['CNV']:
                    if item.get('Disorder') == 'Control':
                        control_f = 1
                    elif item.get('Disorder') != None:
                        case_f = 1
                if control_f == 1 and case_f == 0:
                    return dan_cg.cnv_gene(data)

                elif control_f == 0 and case_f == 1:
                    return dan_cg.cnv_gene(data)
                elif control_f == 1 and case_f == 1:
                    return cg.cnv_gene(id, f, data)
        else:
            pass


def main(ID):
    mainer = Main()
    ID = str(ID)
    return mainer.run(ID)


if __name__ == '__main__':
    mainer = Main()
    # mainer.run("339302")
    mainer.run("4204")
    # mainer.run("53335")
    # mainer.run("6925")
    # mainer.run("54487")
    # mainer.run("85358")
# mainer.run("1108")
