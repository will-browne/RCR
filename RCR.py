import copy
import math
from Environment import environment

class RCR:

    def __init__(self,populations,system_ID,problem_ID,Problem_Length,Is_ten_Folder=None):

        self.Problem_Id=problem_ID
       
        self.Problem_Length=Problem_Length

        #self.env=environment(True,self.Problem_Id,self.Problem_Length)

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


        self.superior_percent=0.8

        self.Is_Boolean_Domain=True

        subsets=self.Implement_Diversity_Razor(populations)

        cluster=self.Cluster(subsets)

        self.result=self.Polymorphism_Razor(cluster)

        #self.Print_Rule_Set(result)

        #self.env=environment(True,self.Problem_Id,self.Problem_Length)
        self.final_acc=self.Accuracy_Test(self.result)
        self.final_size=len(self.result)
        #print(self.final_acc)
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
            if self.system_ID==0:
                #4 accuracy UCS
                if population[id][4]<1.0:
                    remove_list.append(id)
            elif self.system_ID==1:
                #3 accuracy XCS
                if population[id][3]<1.0:
                    remove_list.append(id)

        count=0
        for id in remove_list:
            population.pop(id-count)
            count+=1

    def Remove_Inferior_Rules(self,population):
        sub_set=[]
        total_product=self.Add_additional_column_product(population)
        #ranked by product #11 size of matched instances (XCS UCS)
        population.sort(key=lambda x:x[11],reverse=True)
        #11 threshold value
        superior_threshold=len(population)*self.superior_percent
        #print superior_threshold
        #print total_product
        total_number=0


        for rule in population:
            
            total_number+=1


            #1 XCS only keep the positive rules
            if self.system_ID==1:
                if rule[6]==1000:
                    sub_set.append(rule)
                if self.Is_Boolean_Domain:
                    if rule[6]==0:
                        rule[6]=1000
                        if rule[1]==0:
                            rule[1]=1
                        else:
                            rule[1]=0
                        sub_set.append(rule)


            #0 UCS
            elif self.system_ID==0:
                sub_set.append(rule)

            if total_number>superior_threshold:
                break
        

        return sub_set

    #add additional column
    def Add_additional_column_product(self,population):
        #return the sum of the product
        total=0
        for rule in population:
            #column 11
            #numerosity*fitness UCS 2 numerosity 3 fitness
            if self.system_ID==0:
                product= round(rule[2]*rule[3],2)
                total+=product
            #XCS 2 numerosity 4 fitness
            elif self.system_ID==1:
                product=round(rule[2]*rule[4],2)
                total+=product
           

            rule.append(product)
        return total

    def Implement_Diversity_Razor(self,populations):

        self.Problem_Length=len(populations[0][0][0])
        subsets=[]
        #for i in range(0,1):
        #    population=populations[1]
        for population in populations:
            print(self.Accuracy_Test(population))
            self.Razor_Accuracy(population)
            subsets.append(self.Remove_Inferior_Rules(population))
        return subsets

    ########################################################
    ############            Clustering             #########
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
        cluster=self.Initial_Cluster()
        for population in Populations_Set:
            for rule in population:
                #0 condition
                level=self.calculate_cluster_level(rule[0])
                id= self.Is_Exist_Level(cluster[level],rule)
                if id !=None:
                    #UCS
                    if self.system_ID==0:
                        #numerosity 2
                        cluster[level][id][2]+=rule[2]
                        #exp 9
                        cluster[level][id][9]+=rule[9]
                    #XCS
                    elif self.system_ID==1:
                         #numerosity 2
                        cluster[level][id][2]+=rule[2]
                        #exp 7
                        cluster[level][id][7]+=rule[7]

                else:
                    cluster[level].append(rule)

        #self.print_cluster(cluster)
        return cluster

    def print_cluster(self,clusters):
        for id in range(0,len(clusters)):
            print(id,"=======================")
            for rule in clusters[id]:
                print(rule)


    ###################################################################
    ############            Razor in Polymorphism             #########
    ################################################################### 


    #check whether two rules conflit
    def Over_lapping_Outer(self,condition_1, condition_2):
        for i in range(0,len(condition_1)):
            if condition_1[i] !='#' and condition_2[i]!='#' and condition_1[i]!=condition_2[i]:
                return False
        return True

    #initial the error list
    def Initial_Error_List_Outer(self):
        result=[]
        
        for i in range(0,self.Problem_Length+1):
            temp=[]
            result.append(temp)
        return result



    def Error_Detection_Low_Top(self,cluster):
        # initial the error list
        error_list=self.Initial_Error_List_Outer()

        for i in range(1,len(cluster)):
            # judge wether is unvalied
            
            for rule_h in range(0,len(cluster[i])):
                #using error score or not
                error_score=0


                for j in range(0,i): 
                    if  rule_h in error_list[i]: 
                        break
                    else:       
                        for rule_l in range(0,len(cluster[j])):
                            if not rule_l in error_list[j]:
                                #same action 1
                                #6 critical state of gener explore state
                                #if population[j][rule_l][6]==True:
                                if cluster[i][rule_h][1] != cluster[j][rule_l][1]:
                                    if self.Over_lapping_Outer(cluster[i][rule_h][0],cluster[j][rule_l][0]):
                                        #0 UCS 10 correct match 1 XCS 7 experience
                                            if self.system_ID==0:
                                                error_score+=cluster[j][rule_l][10]
                                                if error_score>cluster[i][rule_h][10]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break


                                            elif self.system_ID==1:
                                                error_score+=cluster[j][rule_l][7]
                                                if error_score>cluster[i][rule_h][7]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break

                                            


        for i in range(1,len(error_list)):
            if len(error_list[i])!=0:
                count=0
                del_list=copy.deepcopy(error_list[i])
                del_list.sort()
                for dele in del_list:
                    cluster[i].pop(dele-count)
                    count+=1


    def Error_Detection_same_level(self,cluster):
        # initial the error list
        error_list=self.Initial_Error_List_Outer()

        for i in range(1,len(cluster)):
            # judge wether is unvalied
            
            for rule_h in range(0,len(cluster[i])):
                #using error score or not
                error_score=0


                for j in range(i,i+1): 
                    if  rule_h in error_list[i]: 
                        break
                    else:       
                        for rule_l in range(0,len(cluster[j])):
                            if not rule_l in error_list[j]:
                                #same action 1
                                #6 critical state of gener explore state
                                #if population[j][rule_l][6]==True:
                                if cluster[i][rule_h][1] != cluster[j][rule_l][1]:
                                    if self.Over_lapping_Outer(cluster[i][rule_h][0],cluster[j][rule_l][0]):
                                        #0 UCS 10 correct match 1 XCS 7 experience
                                            if self.system_ID==0:
                                                error_score+=cluster[j][rule_l][10]
                                                if error_score>cluster[i][rule_h][10]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break


                                            elif self.system_ID==1:
                                                error_score+=cluster[j][rule_l][7]
                                                if error_score>cluster[i][rule_h][7]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break

                                            


        for i in range(1,len(error_list)):
            if len(error_list[i])!=0:
                count=0
                del_list=copy.deepcopy(error_list[i])
                del_list.sort()
                for dele in del_list:
                    cluster[i].pop(dele-count)
                    count+=1


    def Error_Detection_Top_Low(self,cluster):
        # initial the error list
        error_list=self.Initial_Error_List_Outer()

        for i in range(0,len(cluster)-1):
            # judge wether is unvalied
            
            for rule_h in range(0,len(cluster[i])):
                #using error score or not
                error_score=0


                for j in range(i,len(cluster)): 
                    if  rule_h in error_list[i]: 
                        break
                    else:       
                        for rule_l in range(0,len(cluster[j])):
                            if not rule_l in error_list[j]:
                                #same action 1
                                #6 critical state of gener explore state
                                #if population[j][rule_l][6]==True:
                                if cluster[i][rule_h][1] != cluster[j][rule_l][1]:
                                    if self.Over_lapping_Outer(cluster[i][rule_h][0],cluster[j][rule_l][0]):
                                        #0 UCS 10 correct match 1 XCS 7 experience
                                            if self.system_ID==0:
                                                error_score+=cluster[j][rule_l][10]
                                                if error_score>cluster[i][rule_h][10]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break


                                            elif self.system_ID==1:
                                                error_score+=cluster[j][rule_l][7]
                                                if error_score>cluster[i][rule_h][7]:
                                                #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                    error_list[i].append(rule_h)
                                                    break

                                            

        for i in range(1,len(error_list)):
            if len(error_list[i])!=0:
                count=0
                del_list=copy.deepcopy(error_list[i])
                del_list.sort()
                for dele in del_list:
                    cluster[i].pop(dele-count)
                    count+=1



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


    def Find_None_Overlapping_Set(self,clustered):
        maximumID=0
        maximumValue=0
        for i in range(0,len(clustered)):
            #Sum of Numerosity ,both XCS and UCS numerosity is stored at 2
            sum_numerosity=0
            for rule in clustered[i]:
                sum_numerosity+=rule[2]
            if sum_numerosity>maximumValue:
                maximumValue=sum_numerosity
                maximumID=i

        total_size=math.pow(2,self.Problem_Length)
        clustered[maximumID].sort(key=lambda x:x[2],reverse=True)

        for rule in clustered[maximumID]:
            represent_size=0
            subset=[]
            represent_size=self.Count_Represent_Size(rule[0])
            subset.append(rule)
            for candidate_rule in clustered[maximumID]:
                #if not self.Over_lapping_Outer(rule[0],candidate_rule[0]):
                if not self.Does_OverLapping(candidate_rule, subset):
                    subset.append(candidate_rule)
                    represent_size+=self.Count_Represent_Size(candidate_rule[0])

                if represent_size==total_size:
                    break
            
            if represent_size==total_size:
                    break

        if represent_size==total_size:
            return subset
        else:
            return None

    def Count_Represent_Size(self,encoding):
        size=1
        count=0
        for att in encoding:
            if att=='#':
                count+=1
        size=size*math.pow(2,count)
        return size

    
    def Does_OverLapping(self,candidate_rule, rule_set):
        for rule in rule_set:
            if self.Over_lapping_Outer(rule[0],candidate_rule[0]):
                return True
        return False

    def Polymorphism_Razor(self,cluster):
        self.Error_Detection_Low_Top(cluster)
        self.Error_Detection_same_level(cluster)
        self.Error_Detection_Top_Low(cluster)
        self.Sub_sumption(cluster)
        subset=self.Find_None_Overlapping_Set(cluster)
        if subset!=None:
            return subset
        else:
            sub_set=[]
            for i in range(0,len(cluster)):
                for rule in cluster[i]:
                    sub_set.append(rule)
            return sub_set
        #self.print_cluster(cluster)

    def Print_Rule_Set(self,population):
        for rule in population:
            print (rule)


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

            if P_action!=None and P_action!=action:
                error+=1

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.env.state)
        print('Uncover',un_cover_count)
        print('correct',correct)
        print('error',error)
        print('size',len(population))
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
            max_id=None
        return max_id

    #Judge whether condition is matched
    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

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