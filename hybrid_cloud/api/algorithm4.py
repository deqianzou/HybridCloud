# coding: utf-8
from algorithm2 import PublicScheduling
#from et import ExecuteTime
from tool import Tools


class ToPublic(object):
    def __init__(self,impra_app,pub_clouds,public_cloud_instance,bandwith,cpu,execute_cost,taf,pro_dict):
        self.impra_app=impra_app
        self.pub_clouds=pub_clouds
        self.instances_of_public = public_cloud_instance
        self.bandwith = bandwith
        self.cpu = cpu
        self.execute_cost=execute_cost
        self.taf=taf
        self.pro_dict=pro_dict

    def exe_time(self, provider, instancetype, taskload):
         return float(taskload) / self.cpu[(provider, instancetype)]


    def direct(self):
        ins_dict={}
        provider,instance_of_task=PublicScheduling(self.impra_app,self.pub_clouds,self.instances_of_public,self.execute_cost,self.taf,self.cpu,self.bandwith,self.pro_dict).scheduling()
        if provider is not None:
            ins_dict[provider]={}
            #instance_of_task=PublicScheduling(self.impra_app,self.pub_clouds,self.instances_of_public,self.execute_cost,self.taf,self.cpu,self.bandwith,self.pro_dict).costcom(self.impra_app,provider)[1]
            #print instance_of_task
            tasks=sorted(self.impra_app["DAG"].keys(),key=lambda x:int(x[1: ]))
            for taski in tasks:
                instance=instance_of_task[taski]
                print "application%s:schedule %s on service %s from %s" % (self.impra_app["app_id"], taski, instance, provider)
                if instance in ins_dict[provider].keys():
                    ins_dict[provider][instance] += 1
                else:
                    ins_dict[provider][instance] = 1
            return ins_dict




                # for it in self.instances_of_public[provider]:
                #
                #     if (float(self.impra_app["load"][taski])/self.cpu[(provider,it)])<Tools(self.bandwith,self.cpu ).public_Tol_WTi(self.impra_app,taski,provider,self.pro_dict) and \
                #     (self.execute_cost[(provider, it)] * self.exe_time(provider, it,self.impra_app["load"][taski])) < mincost:
                #         print "application%s:schedule %s on service %s from %s" % (self.impra_app["app_id"],taski,it,provider)
                #         find_instance="ture"
                #         break
                # if find_instance!="ture":
                #     print "The status of application%s is disable" % self.impra_app["app_id"]
                #     break

