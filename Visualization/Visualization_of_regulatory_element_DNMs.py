# -*- encoding: utf-8 -*-
# -------------------------------------------------------------------------------
# @file:        0618_cg
# @Author:      GuoSijia
# @Purpose:
# @Created:     2018-06-30
# @update:      2018-06-30 23:59
# @Software:    PyCharm
# -------------------------------------------------------------------------------
import pymongo
from itertools import chain
import plotly.graph_objs as go
from plotly.graph_objs import *
import plotly


class DataQuery(object):

    def __init__(self, name):
        self.name = name
        self.path = self.__login()

    def __login(self):
        client = pymongo.MongoClient("127.0.0.1", 27017)
        db = client['Denovo']
        # db.authenticate("tanxian123", "123456")
        collection = client['Denovo'][self.name]
        return collection

    def Storage(self, dic):
        return self.path.insert(dic)

    def FindByID(self, ID):
        return self.path.find_one({'ENTREZ_ID': ID})


class GetData(object):
    """
    获取数据类，转录本、调控原件（启动子，增强子）大段以及DNM位点
    """

    def __init__(self, gene_data):
        self.gene_data = gene_data

    def drop_duplication(self, a_list, b_list, c_list):
        a_copy_list = []
        b_copy_list = []
        c_copy_list = []
        for i, item in enumerate(c_list):
            if item not in c_copy_list:
                c_copy_list.append(item)
                b_copy_list.append(b_list[i])
                a_copy_list.append(a_list[i])
        return [a_copy_list, b_copy_list, c_copy_list]

    def get_ep_data(self):
        promoter = []
        enhancer = []
        if self.gene_data != None:
            temp_promoter = []
            temp_promoter_frag = []
            temp_promoter_tips = []
            if 'Promote' in self.gene_data.keys():
                for item in self.gene_data['Promote']:
                    if 'start' in item.keys() and 'end' in item.keys():
                        if item['start'] != '-' and item['end'] != '-':  # 有增强子
                            tips = ''.join(item.get('promoter number')) + ',' + \
                                   str(item.get('promoter location')).split(':')[-1].replace(',+"', '').replace(',-"',
                                                                                                                '') \
                                # +','+item.get('robust/permissive')
                            # + ',TargetGeneID:' + ','.join(item['targetgeneid'])
                            temp_promoter.append('Promoter')
                            temp_promoter_frag.append([int(item['start']), int(item['end'])])
                            temp_promoter_tips.append(tips)
                        # temp2 = [[int(item['start']), int(item['end'])], tips, 'p']
                        # ep_data.append(temp2)
            temp_enhancer = []
            temp_enhancer_frag = []
            temp_enhancer_tips = []
            if 'Enhance' in self.gene_data.keys():
                for item in self.gene_data['Enhance']:
                    if 'start' in item.keys() and 'end' in item.keys():
                        if item['start'] != '-' and item['end'] != '-':  # 有启动子
                            tips = ''.join(item['attributes'].split(';')[0]).replace('genehancer_id=', '') + ',' + \
                                   str([item['start'].replace("'", '') + ',' + item['end'].replace("'",
                                                                                                   '')]) + 'local'  # +',TargetGeneID:'+','.join(item['targetgeneid'])
                            temp_enhancer.append('Enhancer')
                            temp_enhancer_frag.append([int(item['start']), int(item['end'])])
                            temp_enhancer_tips.append(tips)
            if 'DNM' in self.gene_data.keys():
                for item_item in self.gene_data['DNM']:
                    if 'enhancerid' in item_item.keys():
                        if 'e_start' in item_item.keys() and 'e_end' in item_item.keys():
                            if item_item['e_start'] not in ['-', None, 'NA', '.'] and item_item['e_end'] not in ['-',
                                                                                                                 None,
                                                                                                                 'NA',
                                                                                                                 '.']:
                                tips = item_item['enhancerid'] + ',' + '[' + item_item['e_start'].replace("'",
                                                                                                          "") + ',' + \
                                       item_item['e_end'].replace("'", "") + ']' + ',targetgene'
                                temp_enhancer.append('Enhancer')
                                # print(item_item['e_start'])
                                # print(item_item['e_end'])
                                temp_enhancer_frag.append([int(item_item['e_start']), int(item_item['e_end'])])
                                temp_enhancer_tips.append(tips)
                    if 'promoterid' in item_item.keys():
                        if 'p_start' in item_item.keys() and 'p_end' in item_item.keys():
                            if item_item['p_start'] not in ['-', None, 'NA', '.'] and item_item['p_end'] not in ['-',
                                                                                                                 None,
                                                                                                                 'NA',
                                                                                                                 '.']:
                                tips = item_item['promoterid'] + ',' + '[' + item_item['p_start'].replace("'",
                                                                                                          "") + ',' + \
                                       item_item['p_end'].replace("'", "") + ']' + ',targetgene'
                                temp_enhancer.append('Promoter')
                                ####--------------------updata---------------------##########
                                temp_enhancer_frag.append([int(item_item['p_start']), int(item_item['p_end'])])
                                temp_enhancer_tips.append(tips)
            if temp_enhancer != [] and temp_enhancer_frag != [] and temp_enhancer_tips != []:
                temp_enhancer, temp_enhancer_frag, temp_enhancer_tips = self.drop_duplication(temp_enhancer,
                                                                                              temp_enhancer_frag,
                                                                                              temp_enhancer_tips)
                enhancer.append(temp_enhancer)
                enhancer.append(temp_enhancer_frag)
                enhancer.append(temp_enhancer_tips)

            if temp_promoter != [] and temp_promoter_frag != [] and temp_promoter_tips != []:
                temp_promoter, temp_promoter_frag, temp_promoter_tips = self.drop_duplication(temp_promoter,
                                                                                              temp_promoter_frag,
                                                                                              temp_promoter_tips)
                promoter.append(temp_promoter)
                promoter.append(temp_promoter_frag)
                promoter.append(temp_promoter_tips)

        return [promoter, enhancer]

    def get_DNM_data(self):
        res = []
        if 'DNM' in self.gene_data.keys():
            for item_item in self.gene_data['DNM']:
                if isinstance(item_item['Exonic Func'], str):
                    s = item_item['Position'] + ',' + item_item['Variant'] + ',' + item_item['Exonic Func']
                elif isinstance(item_item['Exonic Func'], list):
                    s = item_item['Position'] + ',' + item_item['Variant'] + ',' + "".join(item_item['Exonic Func'])
                # if item_item['AAChange_refGene or dist_to_genes'] !='NA':
                # 	s+=','
                # 	s+=item_item['AAChange_refGene or dist_to_genes']
                else:
                    if isinstance(item_item['Func refGene'], str):
                        s = item_item['Position'] + ',' + item_item['Variant'] + ',' + item_item['Func refGene']
                    elif isinstance(item_item['Func refGene'], list):
                        s = item_item['Position'] + ',' + item_item['Variant'] + ',' + "".join(
                            item_item['Func refGene'])
                # if item_item['AAChange_refGene or dist_to_genes'] !='NA':
                # 	s+=','
                # 	s+=item_item['AAChange_refGene or dist_to_genes']
                res.append([int(item_item['Position']), 'DNMs', s])
        else:
            res.append([])
        return res

    def str_to_int(self, c_str):

        many_str_list = c_str.split(',')

        many_int_list = []

        for item in many_str_list:
            for item_item in item.split('_'):
                many_int_list.append(int(item_item.replace('"', '')))

        sort_many_int_list = sorted(many_int_list)

        res = [sort_many_int_list[0], sort_many_int_list[-1]]

        return res

    def str_to_list(self, str):
        list_1D = str.split(',')
        list_2D = [item.split('_') for item in list_1D]
        return list_2D

    def get_Strand(self):
        strand_list = []
        if 'Trans_Ref' in self.gene_data.keys():
            for item in self.gene_data['Trans_Ref']:
                strand_list.append(item['strand'])
        if 'Trans_Gencode' in self.gene_data.keys():
            for item in self.gene_data['Trans_Gencode']:
                strand_list.append(item['strand'])
        strand_set_list = list(set(strand_list))
        if len(strand_set_list) != 1:
            print('转录本存在不同的转录方向！！')
        return strand_list[0]

    def GetExonRegion(self, exon_str):
        exon_str_list = exon_str.split(',')
        exon_list = []
        for item in exon_str_list:
            exon_list.append(item.split('_'))
        del exon_str_list

        start_list = [int(item[0].replace('"', '').replace("'", "")) for item in exon_list]
        end_list = [int(item[1].replace('"', '').replace("'", "")) for item in exon_list]
        min_value = min(min(start_list), min(end_list))
        max_value = max(max(start_list), max(end_list))
        return [min_value, max_value]

    def GetExonAndIntron(self, row, strand):
        if strand == '+':
            if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':
                if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':
                    ei = [self.str_to_int(row['utr5_exon_region'])[1], self.str_to_int(row['utr3_exon_region'])[0]]
                else:
                    if type(row['coding_exon_region']) == str and row['coding_exon_region'] != 'NA':
                        ei = [self.str_to_int(row['utr5_exon_region'])[1],
                              self.GetExonRegion(row['coding_exon_region'])[1]]
                    else:
                        ei = []
            else:
                if type(row['coding_exon_region']) == str and row['coding_exon_region'] != 'NA':
                    if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':
                        ei = [self.GetExonRegion(row['coding_exon_region'])[0],
                              self.str_to_int(row['utr3_exon_region'])[0]]
                    else:
                        ei = self.GetExonRegion(row['coding_exon_region'])
                else:
                    ei = []
        else:
            if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':
                if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':
                    ei = [self.str_to_int(row['utr3_exon_region'])[1], self.str_to_int(row['utr5_exon_region'])[0]]
                else:
                    if type(row['coding_exon_region']) == str and row['coding_exon_region'] != 'NA':
                        ei = [self.str_to_int(row['utr3_exon_region'])[1],
                              self.GetExonRegion(row['coding_exon_region'])[1]]
                    else:
                        ei = []
            else:
                if type(row['coding_exon_region']) == str and row['coding_exon_region'] != 'NA':
                    if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':
                        ei = [self.GetExonRegion(row['coding_exon_region'])[0],
                              self.str_to_int(row['utr5_exon_region'])[0]]
                    else:
                        ei = self.GetExonRegion(row['coding_exon_region'])
                else:
                    ei = []
        return ei

    def get_all_trans_region(self):
        sam = []

        strand = self.get_Strand()
        if 'Trans_Ref' in self.gene_data.keys():
            for row in self.gene_data['Trans_Ref']:
                sam.append(row['TranscriptID'])
                sam.append(self.GetExonAndIntron(row, strand))
        if 'Trans_Gencode' in self.gene_data.keys():
            for row in self.gene_data['Trans_Gencode']:
                sam.append(row['TranscriptID'])
                sam.append(self.GetExonAndIntron(row, strand))
        return sam

    def get_all_trans_count(self):
        sam = []

        strand = self.get_Strand()
        if 'Trans_Ref' in self.gene_data.keys():
            for row in self.gene_data['Trans_Ref']:
                sam.append(row['TranscriptID'])
                sam.append(self.GetExonAndIntron(row, strand))
        if 'Trans_Gencode' in self.gene_data.keys():
            for row in self.gene_data['Trans_Gencode']:
                sam.append(row['TranscriptID'])
                sam.append(self.GetExonAndIntron(row, strand))
        return len(sam)

    def GetAllGeneRegion(self):
        strand = self.get_Strand()
        trans_data = []
        if 'Trans_Ref' in self.gene_data.keys():
            for row in self.gene_data['Trans_Ref']:
                temp = []
                temp.append(row['TranscriptID'])
                temp.append(self.GetExonAndIntron(row, strand))
                if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':
                    temp.append(self.str_to_int(row['utr3']))
                else:
                    temp.append([])
                if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':
                    temp.append(self.str_to_int(row['utr5_exon_region']))
                else:
                    temp.append([])
                trans_data.append(temp)
        if 'Trans_Gencode' in self.gene_data.keys():
            for row in self.gene_data['Trans_Gencode']:
                temp = []
                temp.append(row['TranscriptID'])
                temp.append(self.GetExonAndIntron(row, strand))
                if type(row['utr3_exon_region']) == str and row['utr3_exon_region'] != 'NA':
                    temp.append(self.str_to_int(row['utr3_exon_region']))
                else:
                    temp.append([])
                if type(row['utr5_exon_region']) == str and row['utr5_exon_region'] != 'NA':
                    temp.append(self.str_to_int(row['utr5_exon_region']))
                else:
                    temp.append([])
                trans_data.append(temp)
        #####去除外显子和utr都是空的转录本#####
        res_trans_data = []
        for item in trans_data:
            if item[1] == [] and item[2] == [] and item[3] == []:
                pass
            else:
                res_trans_data.append(item)
        return res_trans_data


class Data_handing(object):

    def __init__(self, id):

        data_query = DataQuery("Genes")
        gene_rec = data_query.FindByID(id)
        get_data = GetData(gene_rec)

        self.trans_data = get_data.GetAllGeneRegion()
        self.regulatory_element_data = get_data.get_ep_data()
        self.dnm_data = get_data.get_DNM_data()
        self.Sym, self.exton, self.utr3, self.utr5 = range(4)
        self.promoter, self.enhancer = range(2)
        self.sym, self.frag, self.tips = range(3)
        self.Start, self.End = range(2)
        self.count = get_data.get_all_trans_count()

    def hb_list_2D(self, test):
        ####合并相邻区间的二维数组#####
        i = 0
        l = len(test)
        while i < l - 1:
            if test[i][1] == test[i + 1][0]:
                test[i] = [test[i][0], test[i + 1][1]]
                test.pop(i + 1)
                l = l - 1
            else:
                i += 1
        return test

    def hb_list_3D(self, list1):

        for i in range(len(list1)):
            if list1[i] != []:
                list1[i] = self.hb_list_2D(list1[i])
        return list1

    def get_all_region(self):
        #####获取所有区域#####
        all_region = []
        for item in self.trans_data:
            if item[self.exton] != []:
                all_region.append(item[self.exton])
            if item[self.utr3] != []:
                all_region.append(item[self.utr3])
            if item[self.utr5] != []:
                all_region.append(item[self.utr5])

        for item in self.regulatory_element_data:
            if item != []:
                for item_item in item[self.frag]:
                    if item_item != []:
                        all_region.append(item_item)
        return all_region

    def drop_duplicate(self, one_list):
        #####去除所有区域中的重复段#####
        temp_list = []
        for one in one_list:
            if one not in temp_list:
                temp_list.append(one)
        return temp_list

    def sort_list(self, all_region):
        #####对所有的区域list根据第一个元素大小进行排序#####
        l = len(all_region)
        all_region = sorted(all_region, key=lambda x: x[0])
        for ii in range(l - 1):
            assert all_region[ii][self.Start] <= all_region[ii + 1][self.Start]
        return all_region

    def cut_fragment(self, all_region):
        #####将所有区域切分成若干个不重复，不交叉的小段#####
        all_s = [item[self.Start] for item in all_region]
        all_e = [item[self.End] for item in all_region]
        all_se = []
        for item in chain(all_s, all_e):
            all_se.append(item)
        all_se = sorted(set(all_se))
        a = all_se[:-1]
        b = all_se[1:]
        all_frag = []
        for x, y in zip(a, b):
            all_frag.append([x, y])

        return all_frag

    def get_sum(self, x_list, n):
        ####求一个list的前n项和#####
        return sum(x_list[:n])

    def get_every_frag_dnm_numbers(self, all_frag, DNM):

        DNM_list = [item[0] for item in DNM]
        DNM_list = list(set(DNM_list))
        DNM_list = sorted(DNM_list)
        num = [0] * len(all_frag)
        i = 0
        for item in all_frag:
            kk = 0
            for item_item in DNM_list:
                if item_item >= item[self.Start] and item_item <= item[self.End]:
                    num[i] += 1
                kk += 1
            i += 1

        return num

    def scale_fragment(self, all_frag, DNM):
        ####规定一个新的片段，规定所有小段（包括外显子和内含子的长度均为20）#####

        num = self.get_every_frag_dnm_numbers(all_frag, DNM)
        # ll = [20] * len(all_frag)
        ll = []
        pe = []
        if self.regulatory_element_data[0] != []:
            promoter_frag = self.regulatory_element_data[0][self.frag]
            for item in promoter_frag:
                pe.append(item)
        if self.regulatory_element_data[1] != []:
            enhancer_frag = self.regulatory_element_data[1][self.frag]
            for item in enhancer_frag:
                pe.append(item)
        # for item in chain(promoter_frag, enhancer_frag):
        # 	pe.append(item)
        pe_drop_dupliction = []
        for item in pe:
            if item not in pe_drop_dupliction:
                pe_drop_dupliction.append(item)
        flag = [0] * len(all_frag)
        for index, item in enumerate(all_frag):
            for item1 in pe_drop_dupliction:
                if item[0] >= item1[0] and item[1] <= item1[1]:
                    flag[index] = 1
        for item1, item2 in zip(flag, num):
            if item1 == 1:
                ll.append(10)
            else:
                if item2 < 3:
                    ll.append(22)
                else:
                    ll.append(item2 * 10 + 2)
            # ll.append(20)
        re_a = [self.get_sum(ll, n) for n in range(len(ll))]
        re_b = [self.get_sum(ll, n) for n in range(1, len(ll) + 1)]
        scale_frag = []
        for x, y in zip(re_a, re_b):
            scale_frag.append([x, y])
        return scale_frag

    def count_exton_region_in_fragment(self, all_frag, scale_frag):
        #####遍历所有外显子区域，统计出所有小段出现在外显子的位置，并将新的小段（自定义间距后的）放到对应位置#####
        ae = list(item[self.exton] for item in self.trans_data)
        count = []
        count1 = []
        for i, item in enumerate(ae):
            temp1 = []
            temp2 = []
            if item == []:
                temp1.append([])
                temp2.append([])
                count.append(temp1)
                count1.append(temp2)
            else:
                for j, item2 in enumerate(all_frag):
                    if item2[self.Start] >= item[self.Start] and item2[self.End] <= item[self.End]:
                        temp1.append(scale_frag[j])
                        temp2.append(all_frag[j])
                count.append(temp1)
                count1.append(temp2)
        sort_count = count
        for index, item in enumerate(sort_count):
            if item != [[]]:
                sort_count[index] = sorted(item, key=lambda x: x[0])

        count = self.hb_list_3D(count)
        count1 = self.hb_list_3D(count1)
        try:
            for index, item in enumerate(count1):
                if item != [[]]:
                    count1[index] = sorted(item, key=lambda x: x[0])
        except:
            pass
        return count, count1

    def count_utr_region_in_fragment(self, all_frag, scale_frag):
        #####遍历所有utr区域，统计出所有小段出现在utr的位置，并将新的小段（自定义间距后的）放到对应位置#####
        ae_utr = []
        for item in self.trans_data:
            temp = []
            if item[self.utr3] != []:  # !=[None,None]
                temp.append(item[self.utr3])
            if item[self.utr5] != []:
                temp.append(item[self.utr5])
            ae_utr.append(temp)
        count = []
        count1 = []
        for item in ae_utr:
            temp1 = []
            temp2 = []
            if item == [[]] or item == []:
                temp1.append([])
                temp2.append([])
                count.append(temp1)
                count1.append(temp2)
            else:
                for i, item1 in enumerate(item):
                    for j, item2 in enumerate(all_frag):
                        if item2[self.Start] >= item1[self.Start] and item2[self.End] <= item1[self.End]:
                            temp1.append(scale_frag[j])
                            temp2.append(all_frag[j])
                count.append(temp1)
                count1.append(temp2)
        sort_count = count
        for index, item in enumerate(sort_count):
            if item != [[]] and item != []:
                sort_count[index] = sorted(item, key=lambda x: x[0])

        count = self.hb_list_3D(count)
        count1 = self.hb_list_3D(count1)
        for index, item in enumerate(count1):
            if item != [[]] and item != []:
                count1[index] = sorted(item, key=lambda x: x[0])
        return count, count1

    def count_promoter_region_in_fragment(self, all_frag, scale_frag):
        #####遍历所有启动子区域，统计出所有小段出现在启动子的位置，并将新的小段（自定义间距后的）放到对应位置#####
        if self.regulatory_element_data[0] != []:
            ae_promoter = self.regulatory_element_data[self.promoter][self.frag]
            count = []
            count1 = []
            for i, item in enumerate(ae_promoter):
                temp = []
                temp1 = []
                for j, item2 in enumerate(all_frag):
                    if item2[self.Start] >= item[self.Start] and item2[self.End] <= item[self.End]:
                        temp.append(scale_frag[j])
                        temp1.append(all_frag[j])
                count.append(temp)
                count1.append(temp1)
            count = self.hb_list_3D(count)
            count1 = self.hb_list_3D(count1)
            return count, count1

    def count_enhancer_region_in_fragment(self, all_frag, scale_frag):
        #####遍历所有增强子区域，统计出所有小段出现在启动子的位置，并将新的小段（自定义间距后的）放到对应位置#####
        if self.regulatory_element_data[1] != []:
            ae_enhancer = self.regulatory_element_data[self.enhancer][self.frag]
            count = []
            count1 = []
            for i, item in enumerate(ae_enhancer):
                temp = []
                temp1 = []
                for j, item2 in enumerate(all_frag):
                    if item2[self.Start] >= item[self.Start] and item2[self.End] <= item[self.End]:
                        temp.append(scale_frag[j])
                        temp1.append(all_frag[j])
                count.append(temp)
                count1.append(temp1)
            count = self.hb_list_3D(count)
            count1 = self.hb_list_3D(count1)
            return count, count1

    def convert_trans_to_xy(self, count, count1):
        #####将转录本（utr，外显子内含子）片段准换成作画需要的坐标#####
        y = [item[0] for item in self.trans_data if not (item[1] == [] and item[2] == [] and item[3] == [])]
        xy = []
        for item, yy, z in zip(count, y, count1):
            for item_item, item_tips in zip(item, z):
                if item_item != [] and item_item != [[]]:
                    temp = [[item_item[0], yy, item_tips[0]], [item_item[1], yy, item_tips[1]]]
                    xy.append(temp)
        # final_xy = []
        # for item in xy:
        # 	for item_item in item:
        # 		final_xy.append(item_item)
        return xy

    def convert_utr_to_xy(self, count, count1):
        #####将转录本（utr，外显子内含子）片段准换成作画需要的坐标#####
        y = [item[0] for item in self.trans_data if not (item[1] == [] and item[2] == [] and item[3] == [])]
        xy = []
        for item, yy, z in zip(count, y, count1):
            if item != [[]]:
                for item_item, item_tips in zip(item, z):
                    temp = [[item_item[0], yy, item_tips[0]], [item_item[1], yy, item_tips[1]]]
                    xy.append(temp)
        # final_xy = []
        # for item in xy:
        # 	for item_item in item:
        # 		final_xy.append(item_item)
        return xy

    def convert_regulatory_elements_to_xy(self, count, p_or_e):
        #####将调控原件（启动子，增强子）片段准换成作画需要的坐标#####
        xy = []
        if p_or_e == 'Promoter':
            tips = self.regulatory_element_data[self.promoter][self.tips]
        elif p_or_e == 'Enhancer':
            tips = self.regulatory_element_data[self.enhancer][self.tips]
        else:
            tips = 'Error'
        for i, item in enumerate(count):
            for item_item in item:
                temp = [[item_item[self.Start], p_or_e, tips[i]], [item_item[self.End], p_or_e, tips[i]]]
                xy.append(temp)
        return xy

    def DNM_sort_by_site(self, DNM):
        if DNM != [[]]:
            sorted_DNM = sorted(DNM, key=lambda x: x[0])
            return sorted_DNM
        else:
            return []

    def mapping_mutation_to_frag(self, all_frag, scale_frag, DNM=[]):
        DNM_list = [item[0] for item in DNM]
        DNM_tips = [item[1] for item in DNM]
        un_sorted_DNM_hover = [item[2] for item in DNM]
        DNM_hover = sorted(un_sorted_DNM_hover, key=lambda x: x[0])
        num = [0] * len(all_frag)
        i = 0
        DNM_frag = []
        for item in all_frag:
            temp = []
            kk = 0
            for item_item in DNM_list:
                if item_item >= item[self.Start] and item_item <= item[self.End]:
                    num[i] += 1
                    temp1 = []
                    temp1.append(item_item)
                    temp1.append(DNM_tips[kk])
                    temp1.append(DNM_hover[kk])
                    temp.append(temp1)
                kk += 1
            DNM_frag.append(temp)
            i += 1
        DNM = []
        j = 0
        for item in num:
            if item != 0:
                start = scale_frag[j][self.Start] + 2
                temp = []
                for k in range(item):
                    temp1 = []
                    temp1.append(start)
                    temp1.append(start + 3)
                    temp1.append(DNM_frag[j][k][0])
                    temp1.append(DNM_frag[j][k][1])
                    temp1.append(DNM_frag[j][k][2])
                    temp.append(temp1)
                    start += 10
                DNM.append(temp)
            j += 1
        final_DNM = []
        for item in DNM:
            for item_item in item:
                final_DNM.append(item_item)
        return final_DNM

    def convert_dnms_to_xy(self, dnm_data):
        xy = []
        for item in dnm_data:
            temp = [[item[0], item[3], item[4]], [item[1], item[3], item[4]]]
            xy.append(temp)
        return xy


class PlotData(object):

    def __init__(self, ID):
        data_handing = Data_handing(ID)
        self.count = data_handing.count

        all_region = data_handing.get_all_region()
        all_region = data_handing.drop_duplicate(all_region)
        all_region = data_handing.sort_list(all_region)

        dnm_data = data_handing.DNM_sort_by_site(data_handing.dnm_data)
        all_frag = data_handing.cut_fragment(all_region)
        scale_frag = data_handing.scale_fragment(all_frag, dnm_data)

        exton_count, exton_count1 = data_handing.count_exton_region_in_fragment(all_frag, scale_frag)
        self.exton_plot_data = data_handing.convert_trans_to_xy(exton_count, exton_count1)

        utr_count, utr_count1 = data_handing.count_utr_region_in_fragment(all_frag, scale_frag)
        self.utr_plot_data = data_handing.convert_utr_to_xy(utr_count, utr_count1)

        if data_handing.regulatory_element_data[0] != []:
            promoter_count, promoter_count1 = data_handing.count_promoter_region_in_fragment(all_frag, scale_frag)
            self.promoter_plot_data = data_handing.convert_regulatory_elements_to_xy(promoter_count, 'Promoter')
        else:
            self.promoter_plot_data = None

        if data_handing.regulatory_element_data[1] != []:
            enhancer_count, enhancer_count1 = data_handing.count_enhancer_region_in_fragment(all_frag, scale_frag)
            self.enhancer_plot_data = data_handing.convert_regulatory_elements_to_xy(enhancer_count, 'Enhancer')
        else:
            self.enhancer_plot_data = None

        final_dnm = data_handing.mapping_mutation_to_frag(all_frag, scale_frag, dnm_data)
        self.dnm_plot_data = data_handing.convert_dnms_to_xy(final_dnm)


class Plot(object):

    def __init__(self, ID):
        self.plot_data = PlotData(ID)
        self.count = self.plot_data.count

    def get_DNM_color(self, s_type):
        if s_type in ['frameshift deletion', 'frameshift insertion', 'frameshift substitution',
                      'splice-site mutation', 'stopgain', 'stoploss'] or s_type.startswith('frameshift'):
            color = 'red'
        elif s_type in ['nonframeshift deletion', 'nonframeshift insertion',
                        'nonframeshift substitution', 'nonsynonymous SNV', 'strat gain',
                        'stoploss'] or s_type.startswith('nonframeshift'):
            color = 'pink'
        elif s_type in ['synonymous SNV', 'exonic', 'coding complex']:
            color = 'purple'
        elif s_type in ['unknown']:
            color = 'yellow'
        else:
            color = 'blue'
        return color

    def get_promoter_color(self, text):
        s = text.split(',')[-1]
        if s == 'permissive':
            color = 'rgb(234,255,0)'
        else:
            color = 'rgb(255,165,0)'
        return color

    def get_enhancer_color(self, text):
        s = text.split(',')[-1]
        if s == 'targetgene':
            color = 'rgb(0,100,0)'
        else:
            color = 'rgb(144,238,144)'
        return color

    def run(self):

        trace = []
        for item in self.plot_data.exton_plot_data:
            trace_item = Scatter(
                visible=True,
                hoverinfo='text',
                hoverlabel={
                    'font': {
                        'size': 10
                    }
                },
                showlegend=False,
                mode='lines',
                x=[item[0][0], item[1][0]],
                y=[item[0][1], item[1][1]],
                text=str(item[0][2]) + '-' + str(item[1][2]),
                line=dict(
                    color='rgb(72,130,180)',
                    shape='linear',
                    width=10,
                    simplify=True
                ),
            )
            trace.append(trace_item)

        for item in self.plot_data.utr_plot_data:
            trace_item = Scatter(
                visible=True,
                hoverinfo='text',
                hoverlabel={
                    'font': {
                        'size': 10
                    }
                },
                showlegend=False,
                mode='lines',
                x=[item[0][0], item[1][0]],
                y=[item[0][1], item[1][1]],
                text=str(item[0][2]) + '-' + str(item[1][2]),
                line=dict(
                    color='gray',
                    shape='linear',
                    width=5,
                    # simplify=True
                ),
            )
            trace.append(trace_item)

        if self.plot_data.promoter_plot_data != None:
            for item in self.plot_data.promoter_plot_data:
                trace_item = Scatter(
                    visible=True,
                    hoverinfo='text',
                    hoverlabel={
                        'font': {
                            'size': 10
                        }
                    },
                    showlegend=False,
                    mode='lines',
                    x=[item[0][0], item[1][0]],
                    y=[item[0][1], item[1][1]],
                    text=str(item[0][2]).replace(',robust', '').replace(',permissive', '').replace(',targetgene',
                                                                                                   '').replace('local',
                                                                                                               ''),
                    line=dict(
                        color=self.get_promoter_color(str(item[0][2])),
                        shape='linear',
                        width=10,
                        simplify=True
                    ),
                )
                trace.append(trace_item)

        if self.plot_data.enhancer_plot_data != None:
            for item in self.plot_data.enhancer_plot_data:
                trace_item = Scatter(
                    visible=True,
                    hoverinfo='text',
                    hoverlabel={
                        'font': {
                            'size': 10
                        }
                    },
                    showlegend=False,
                    mode='lines',
                    x=[item[0][0], item[1][0]],
                    y=[item[0][1], item[1][1]],
                    text=str(item[0][2]).replace(',targetgene', '').replace('local', ''),
                    line=dict(
                        color=self.get_enhancer_color(str(item[0][2])),
                        shape='linear',
                        width=10,
                        simplify=True
                    ),
                )
                trace.append(trace_item)

        for item in self.plot_data.dnm_plot_data:
            type = item[0][2].split(',')[2]
            c = self.get_DNM_color(type)
            trace_item = Scatter(
                visible=True,
                hoverinfo='text',
                hoverlabel={
                    'font': {
                        'size': 10
                    }
                },
                showlegend=False,
                mode='lines',
                x=[item[0][0], item[1][0]],
                y=[item[0][1], item[1][1]],
                text=str(item[0][2]),
                line=dict(
                    color=c,
                    shape='linear',
                    width=10,
                    simplify=True
                ),
            )
            trace.append(trace_item)

        layouts = go.Layout(
            paper_bgcolor='rgb(249, 249, 249)',
            plot_bgcolor='rgb(249, 249, 249)',
            # height=600,
            width=800,
            # title='Transcript DNM Visualizations',
            # titlefont=dict(size=25),
            hovermode='closest',
            margin=go.Margin(  # x,y轴label距离图纸四周的距离
                l=110,
                r=5,
                # b=50,
                t=10,
                pad=0
            ),
            spikedistance=0,
            hoverdistance=2,
            hoverlabel=dict(
                # bgcolor='rgb(199,237,204,0)',
                # bordercolor='white'
                # opacity=0.5
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                showticklabels=False,
                autorange=True,
                dtick=100,
            ),
            yaxis=dict(
                titlefont=dict(
                    family='Arial, sans-serif',
                    size=18,
                    color='lightgrey'
                ),

                showticklabels=True,
                tickangle=360,
                tickfont=dict(
                    family='Arial, serif',
                    size=10,
                    color='black'
                ),
                exponentformat='e',
                showexponent='All'
            )

        )
        figs = go.Figure(data=trace, layout=layouts)
        # plotly.offline.plot(figs, show_link=False)
        try:
            return plotly.offline.plot(figs, show_link=False, output_type="div"
                                       # , include_plotlyjs=False
                                       )
        except:
            return '<div>There is no corresponding data published yet, we will update it when such data available. </div>'


def main(ID):
    ID = str(ID)
    plot = Plot(ID)
    return plot.run()


if __name__ == '__main__':
    main(57680)
