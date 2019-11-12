import copy
import math
from Environment import environment
import copy
class RCR3:

    def __init__(self,populations,system_ID,problem_ID,Problem_Length,Is_ten_Folder=None):

        self.Problem_Id=problem_ID
       
        self.Problem_Length=Problem_Length

        self.system_ID=system_ID

        if Is_ten_Folder==None:
            self.env=environment(True,self.Problem_Id,self.Problem_Length)
            if self.Problem_Id>3:
                self.env.Initial_Real_Value(self.Problem_Id)
        else:
            self.env=environment(True,self.Problem_Id,self.Problem_Length)
            self.env.Is_tenfolder=True
            self.env.folder_Address=Is_ten_Folder.Train_Address
            self.env.Initial_Real_Value(self.Problem_Id)

            self.Test_env=environment(True,self.Problem_Id,self.Problem_Length)
            self.Test_env.Is_tenfolder=True
            self.Test_env.folder_Address=Is_ten_Folder.Test_Address
            self.Test_env.Initial_Real_Value(self.Problem_Id)

        self.Is_Boolean_Domain=True

        self.Implement_Diversity_Razor(populations)

        support_cluster,opposite_cluster=self.Cluster(populations)

        self.result=self.Polymorphism_Razor(support_cluster,opposite_cluster)

        #self.Print_Rule_Set(result)
        
        self.final_acc=self.Accuracy_Test(self.result)
        self.final_size=len(self.result)
        print(self.final_acc)
        self.un_cover_count,self.correct,self.error=self.Final_Accuracy_Test(self.result)

        if Is_ten_Folder!=None:
            self.final_test_accuracy=self.Accuracy_Test_tenfolders(self.result)

        #print("test Accuracy",self.final_test_accuracy)

    ########################################################
    ############            Diversity Razor        #########
    ########################################################

    def Razor_Accuracy(self,population):
        remove_list=[]


        for id in range (0,len(population)):
            # 1 XCS 0 UCS
            if population[id][11] * population[id][12]!=0 or population[id][11]+population[id][12]==0:
                remove_list.append(id)



        count=0

        for id in remove_list:
            population.pop(id-count)
            count+=1

    def Implement_Diversity_Razor(self,populations):
        self.Problem_Length=len(populations[0][0][0])

        #for i in range(0,1):
        #    population=populations[1]
        for population in populations:
            #print (len(population))

            self.Add_additional_column_count(population)
            self.Accuracy_Test(population)
            self.Razor_Accuracy(population)
            #print (len(population))

    #add additional column
    def Add_additional_column_count(self,population):
        #return the sum of the product
        total=0
        for rule in population:
            #column 11 correct match
            #column 12 incorrect match
            #numerosity*fitness UCS 2 numerosity 3 fitness
            correct=0
            incorrect=0 
            temp=[]          
            rule.append(correct)
            rule.append(incorrect)
            rule.append(temp)
        return total

    ###################################################################
    ############            Acuracy Test                      #########
    ################################################################### 

    def Accuracy_Test(self,population):
        correct=0
        un_cover_count=0
        error=0

        for id in range(0,len(self.env.state)):
            Match_Set=self.getMatchSet(self.env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.env.executeAction_supervisor(self.Problem_Id,self.env.state[id])
            else:
                action=self.env.actions[id]

            if P_action==None:
                un_cover_count+=1

            #Incorrect match
            if P_action!=None and P_action!=action:
                error+=1
                

            if P_action==action:
                correct+=1

            for id in Match_Set:
                if population[id][1]==action:
                    #correct
                    population[id][11]+=1
                else:
                    #incorrect
                    population[id][12]+=1

        accu=1.0*correct/len(self.env.state)
        print('Size',len(population))
        print('Uncover',un_cover_count)
        print('correct',correct)
        print('error',error)
        print(accu)
        return accu

    def getMatchSet(self,state,population):
        match_set=[]
        #print "begin"
        for i in range(0,len(population)):
            #0: condition
            if(self.isConditionMatched(population[i][0],state)):
                #add matching classifier to the matchset
                match_set.append(i)
        return match_set

    def Prediction(self,match_set,population):
        actions_value=[]
        for i in range(0,self.env.real_actions):
            actions_value.append(0)

        for id in match_set:
            #1: action 2:numerosity 3: # 3: fitness (0UCS, 1XCS)
            if self.system_ID==0:
                actions_value[population[id][1]]+=population[id][2]*population[id][3]
            # 6 prediction 4 fitness
            elif self.system_ID==1:
                actions_value[population[id][1]]+=population[id][6]*population[id][4]

        #deault maxi
        
        max_id=0
        max_value=actions_value[0]
      

        for i in range(1,self.env.real_actions):
            if actions_value[i]>max_value:
                max_value=actions_value[i]
                max_id=i


        if len(match_set)==0:
        #if max_value==0:
            max_id=None
        return max_id

    #Judge whether condition is matched
    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

    def Print_Rule_Set(self,population):
        for rule in population:
            print (rule)


    ########################################################
    ############           Cluster                 #########
    ######################################################## 

    #judge whether two condition is same
    def Is_Same_Condition(self,c1,c2):
        for i in range(0,len(c1)):
            if c1[i] != c2[i]:
                return False
        return True

    #judge is exist
    def Is_Same_Rule(self,R1,R2):
        if R1[1]!=R2[1]:
            return False
        else:
            #condition 0
            if self.Is_Same_Condition(R1[0],R2[0]):
                return True
            else:
                return False

    def Initial_Cluster(self):
        cluster=[]
        for i in range(0,self.Problem_Length+1):
            p=[]
            cluster.append(p)
        return cluster

    def calculate_cluster_level(self,condition):
        id=0
        for cod in condition:
            if cod=='#':
                id+=1
        return id

    def Is_Exist_Level(self,cluster,rule):
        for id in range(0,len(cluster)):
            if self.Is_Same_Rule(cluster[id],rule):
                return id
        return None
    
    def Cluster(self,Populations_Set):
        support_cluster=self.Initial_Cluster()
        opposite_cluster=self.Initial_Cluster()
        for population in Populations_Set:
            for rule in population:
                #0 condition
                level=self.calculate_cluster_level(rule[0])
                #UCS
                if self.system_ID==0:
                    id= self.Is_Exist_Level(support_cluster[level],rule)
                    if id !=None:
                        #numerosity 2
                        support_cluster[level][id][2]+=rule[2]
                        #exp 9
                        support_cluster[level][id][9]+=rule[9]
                    else:
                        support_cluster[level].append(rule)
                #XCS
                elif self.system_ID==1:
                    #6 Prediction
                    if rule[6]==1000:
                        id= self.Is_Exist_Level(support_cluster[level],rule)
                        if id !=None:
                            #numerosity 2
                            support_cluster[level][id][2]+=rule[2]
                            #exp 7
                            support_cluster[level][id][7]+=rule[7]
                        else:
                            support_cluster[level].append(rule)
                    elif rule[6]==0:
                        rule[6]=-1000
                        id= self.Is_Exist_Level(opposite_cluster[level],rule)
                        if id !=None:
                            #numerosity 2
                            opposite_cluster[level][id][2]+=rule[2]
                            #exp 7
                            opposite_cluster[level][id][7]+=rule[7]
                        else:
                            opposite_cluster[level].append(rule)


        #self.print_cluster(cluster)
        return support_cluster,opposite_cluster

    def print_cluster(self,clusters):
        for id in range(0,len(clusters)):
            print(id,"=======================")
            for rule in clusters[id]:
                print(rule)   

   ###################################################################
   ############            Razor in Polymorphism             #########
   ################################################################### 


    #check whether gener rule is more gener
    def Is_More_general_Subsumption(self,gener_condition,specific_condition):
         for i in range(0,len(gener_condition)):
             if gener_condition[i] !='#' and gener_condition[i]!=specific_condition[i]:
                 return False
         return True

    
     

    #check whether gener rule is more gener
    def Sub_sumption(self,cluster):

         for level in range(len(cluster)-1,0,-1):
             for g_rule in cluster[level]:
                 
                 for C_level in range(level-1,-1,-1):
                     remove_list=[]
                     for S_id in range(0,len(cluster[C_level])):
                         #0 condition
                         if self.Is_More_general_Subsumption(g_rule[0],cluster[C_level][S_id][0]):
                             remove_list.append(S_id)
                     count=0
                     for r_id in remove_list:
                         cluster[C_level].pop(r_id-count)
                         count+=1

    def Polymorphism_Razor(self,support_cluster,opposite_cluster):
        self.Sub_sumption(support_cluster)
        self.Sub_sumption(opposite_cluster)
        self.MatchList_Generator(support_cluster)
        self.MatchList_Generator(opposite_cluster)
        self.Merge_Process(support_cluster)
        self.Merge_Process(opposite_cluster)
        population=[]

        self.Create_Population(support_cluster,population)
        self.Create_Population(opposite_cluster,population)
        print(len(population))
        return population




    def Create_Population(self,cluster,population):
        for i in range(0,len(cluster)):
                for rule in cluster[i]:
                    rule[13]=[]
                    population.append(rule)


    def MatchList_Generator(self,cluster):

        for id in range(0,len(self.env.state)):
            for i in range(0,len(cluster)):
                for rule in cluster[i]:
                    #0: condition
                    if(self.isConditionMatched(rule[0],self.env.state[id])):
                        rule[13].append(id)

    def Merge_Process(self,cluster):
        Present_list=[]
        
        for i in range(len(cluster)-1,-1,-1):
            remove_list=[]
            for rule_id in range(0,len(cluster[i])):
                remove=True
                for id in cluster[i][rule_id][13]:
                    if not id in Present_list:
                        Present_list.append(id)
                        remove=False
                if remove:
                    remove_list.append(rule_id)

            count=0
            for dele in remove_list:
                cluster[i].pop(dele-count)
                count+=1

    def Final_Accuracy_Test(self,population):
        correct=0
        un_cover_count=0
        error=0

        for id in range(0,len(self.env.state)):
            Match_Set=self.getMatchSet(self.env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.env.executeAction_supervisor(self.Problem_Id,self.env.state[id])
            else:
                action=self.env.actions[id]

            if P_action==None:
                un_cover_count+=1

            if P_action!=None and P_action!=action:
                error+=1

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.env.state)
        #print('Uncover',un_cover_count)
        #print('correct',correct)
        #print('error',error)
        #print('size',len(population))
        return un_cover_count,correct,error

    def Accuracy_Test_tenfolders(self,population):
        correct=0
        for id in range(0,len(self.Test_env.state)):
            Match_Set=self.getMatchSet(self.Test_env.state[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.Test_env.executeAction_supervisor(self.Problem_Id,self.Test_env.state[id])
            else:
                action=self.Test_env.actions[id]

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.Test_env.state)
        return accu
