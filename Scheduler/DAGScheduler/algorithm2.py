# coding: utf-8
#from cost import Cost
from tool import Tools
#from et import ExecuteTime


class PublicScheduling(object):
    def __init__(self,application,public_clouds,instances,execute_cost,taf,cpu,bandwith,pro_dict):
        self.application=application
        self.public_clouds=public_clouds
        self.potential_cost={}
        self.instances_of_public=instances
        self.execute_cost = execute_cost
        self.taf = taf
        self.cpu=cpu
        self.bandwith = bandwith
        self.pro_dict=pro_dict

    def scheduling(self):
        for public_cloud in self.public_clouds:
            self.potential_cost[(self.application["app_id"],public_cloud)]=self.costdata(self.application,public_cloud)
        clouds_schehuler = {}
        for public_cloud in self.public_clouds:

            costcom_ins=self.costcom(self.application, public_cloud)
            self.potential_cost[(self.application["app_id"],public_cloud)]=self.potential_cost[(self.application["app_id"], public_cloud)]\
                                                                          +costcom_ins[0]

            clouds_schehuler[public_cloud]=costcom_ins[1]

        min_cost = float("inf")
        for public_cloud in self.public_clouds:
            if min_cost>self.potential_cost[(self.application["app_id"],public_cloud)]:
                min_cost=self.potential_cost[(self.application["app_id"],public_cloud)]
                self.provider = public_cloud
        if min_cost >= float("inf"):
            print "The status of application %s is disable!" % self.application["app_id"]
        else:

            return self.provider,clouds_schehuler[self.provider]

    def exe_time(self,provider,instancetype,taskload):
        return float(taskload) / self.cpu[(provider,instancetype)]

    def costdata(self,app,cloud):
        return app["size"]*self.taf[cloud]

    def costcom(self,appl,pubcloud):
        res=[]
        instance_of_task={}
        cost=0
        for task in appl["DAG"].keys():
            ctask=float("inf")
            cheapestit = "None"
            for it in self.instances_of_public[pubcloud]:
                #print "ExecuteTime2",self.exe_time(pubcloud,it,appl["load"][task])
                #print "task,exetime,wti",task,self.exe_time(pubcloud,it,appl["load"][task]),Tools(self.bandwith,self.cpu).public_Tol_WTi(appl,task,pubcloud,self.pro_dict)
                if self.exe_time(pubcloud,it,appl["load"][task])<Tools(self.bandwith,self.cpu).public_Tol_WTi(appl,task,pubcloud,self.pro_dict):
                    if (self.execute_cost[(pubcloud,it)]*self.exe_time(pubcloud,it,appl["load"][task]))<ctask:
                        ctask=self.execute_cost[(pubcloud,it)]*self.exe_time(pubcloud,it,appl["load"][task])
                        cheapestit=it
                        #print "pubcloud,it,cost",pubcloud,it,ctask
            cost+=ctask
            instance_of_task[task]=cheapestit
        res.append(cost)
        res.append(instance_of_task)
        #print "cloud,cost", pubcloud,cost
        return res




            
    
            
        
