# coding: utf-8
from algorithm4 import ToPublic
#from et import ExecuteTime
from tool import Tools
import json
import os
import os.path
import copy
import time


class Scanning(object):
    def __init__(self, private_vcpus=0,
                 private_instance={"X_Small": 1, "Small": 4, "Medium": 8, "Large": 10, "X_Large": 24, "XX_Large": 50},
                 public_clouds=[{"cloud_provider": "Aliyun", "cpu": {"Small": 1, "Medium": 2, "Large": 4,"X_Large":8,"XX_Large":16,"3X_Large":32},
                                 "price_per_hour": {"Small": 0.277, "Medium": 0.557, "Large": 1.117,"X_Large":2.555,"XX_Large":5.12,"3X_Large":10.241}, "bandwith": 5.0,
                                 "transfer_cost": 0.0}
                                ]):
        """

        :type
        private_vcpus：公有云cpu资源数
        private_instance： 私有云不同虚拟机类型cpu数
        public_clouds: cloud_provider:公有云提供商名称
                       cpu：不同虚拟机类型cpu数
                       price_per_hour：不同虚拟机类型每小时价格（元）
                       bandwith：带宽（G/s)
                       transfer_cost:带宽价格（元/G)
        """
        self.private_instance = private_instance
        private_instance=sorted(private_instance.iteritems(), key=lambda d: d[1])
        self.instance_type = [key for key,value in private_instance]
        self.public_clouds = public_clouds
        self.public_clouds_list = self.get_public_clouds_list()
        self.public_instances = self.get_public_instances()
        self.vcpu_dict=self.get_vcpu_dict()
        self.bandwith_dict=self.get_bandwith_dict()
        self.execution_cost_dict=self.get_execution_cost_dict()
        self.tar_dict=self.get_tar_dict()
        self.tooli = Tools(self.bandwith_dict,self.vcpu_dict)
        #self.sort_queue = self.tooli.queue_mlf()
        self.sort_queue = []
        self.deadline = "ture"
        self.private_resource = private_vcpus

    def scan(self,a_app):
        #self.sort_queue = self.tooli.get_new_queue(self.sort_queue)
        self.sort_queue.append(a_app)
        timestamp=time.time()
        timestamp=1500367968
        instance_number={}
        pubins_dict={}
        instance_number["private_cloud"] = {}
        pro_dict=self.tooli.get_proapp(self.sort_queue,timestamp)
        for a in self.sort_queue:
            a_id = a["app_id"]
            a_now = copy.deepcopy(a)  # 原始应用副本
            ins_of_task={}
            while a["DAG"]:
                Li = self.tooli.get_enter_tasks(a)
                self.deadline = "ture"
                for taski in Li:
                    # get instance type it causing smallest weight(p, it, i) within Tol_WTi
                    if self.tooli.private_Tol_Tr(a,pro_dict) > 0:  # 应用在私有云里可以完成
                        smallest_weight = float("inf")
                        find_instance = "False"
                        for it in self.instance_type:
                            # print "ExecuteTime,Tol_WTi",ExecuteTime().exe_time("private_cloud",it,a["load"][taski]),self.tooli.private_Tol_WTi(a, taski)
                            if (self.exe_time("private_cloud", it, a["load"][taski]) < self.tooli.private_Tol_WTi(
                                    a, taski, pro_dict) and
                                        self.weight("private_cloud", it, a["load"][taski]) < smallest_weight and
                                        self.private_resource >= self.vcpu_dict[("private_cloud", it)]):
                                smallest_weight = self.weight("private_cloud", it, a["load"][taski])
                                instance = it
                                find_instance = "Ture"
                        if find_instance == "False":
                            instance = ""
                    else:
                        instance = ""
                    if instance:
                        #print "application%s:schedule task%s to instance type %s" % (a["app_id"], taski, instance)
                        ins_of_task[taski] = instance
                        self.private_resource -= self.vcpu_dict[("private_cloud", instance)]
                    else:
                        print "schedule application%s to public" % (a["app_id"])
                        pubins_dict=ToPublic(a_now, self.public_clouds_list, self.public_instances,self.bandwith_dict,self.vcpu_dict,self.execution_cost_dict,self.tar_dict,pro_dict).direct()
                        self.deadline = 'false'
                        break
                if self.deadline == 'false':
                    self.sort_queue = filter(lambda x: x["app_id"] != a_id, self.sort_queue)  # 同下
                    break
                elif len(ins_of_task)==len(a["load"]):

                    for key,value in ins_of_task.items():
                        print "application%s:schedule task%s to instance type %s" % (a["app_id"], key, value)
                        if value in instance_number["private_cloud"].keys():
                            instance_number["private_cloud"][value] += 1

                        else:
                            instance_number["private_cloud"][value] = 1


                for v in a["DAG"].keys():
                    if v in Li:
                        del a["DAG"][v]
            self.sort_queue = filter(lambda x: x["app_id"] != a_id, self.sort_queue)  # 实时的应用队列
        instance_number = dict(instance_number,**pubins_dict)
        return instance_number





    def weight(self,provider, instance, loadi):
        return self.vcpu_dict[("private_cloud", instance)] * self.exe_time(provider, instance, loadi)

    def get_public_clouds_list(self):
        list = []
        for cloud in self.public_clouds:
            list.append(cloud["cloud_provider"])
        return list

    def get_public_instances(self):
        dict = {}
        for cloud in self.public_clouds:
            cpu_dict=sorted(cloud["cpu"].iteritems(), key=lambda d: d[1])
            dict[cloud["cloud_provider"]] = [key for key,value in cpu_dict]
        return dict

    def get_vcpu_dict(self):
        dict = {}
        for key,value in self.private_instance.items():
            dict[("private_cloud", key)] = value
        for cloud in self.public_clouds:
            for key,value in cloud["cpu"].items():
                dict[(cloud["cloud_provider"], key)] = value
        return dict

    def get_bandwith_dict(self):
        dict = {}
        for cloud in self.public_clouds:
            dict[cloud["cloud_provider"]] = cloud["bandwith"]
        return dict

    def get_execution_cost_dict(self):
        dict = {}
        for cloud in self.public_clouds:
            for key, value in cloud["price_per_hour"].items():
                dict[(cloud["cloud_provider"], key)] = value
        return dict

    def get_tar_dict(self):
        dict = {}
        for cloud in self.public_clouds:
            dict[cloud["cloud_provider"]] = cloud["transfer_cost"]
        return dict

    def exe_time(self,provider, instancetype, taskload):
        return float(taskload) / self.vcpu_dict[(provider, instancetype)]






if __name__ == "__main__":
    mttest = Scanning()
    while "ture":
        print "run scan!"
        res_dict=mttest.scan()
        print res_dict
        time.sleep(20)
