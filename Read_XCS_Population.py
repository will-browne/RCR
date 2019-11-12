 
class Read_XCS_Population:
    def __init__(self,Address):
        self.population=[]
        self.micro_size=0
        self.Read(Address)
        #self.Print_Population()

    def Create_new_Single_Rule(self,condition,action,numerosity,acc,fit,P_E,Pre,Exp,Ssize):
        # States of Attributes Specified in classifier (Ternary)
        # 0: condition 
        #class
        # 1: action 
        # The number of rule copies stored in the population.  (Indirectly stored as incremented numerosity)
        # 2: numerosity
        
        # Classifier accuracy - Accuracy calculated using only instances in the dataset which this rule matched.
        # 3: accuracy
        # Classifier fitness - initialized to a constant initial fitness value 
        # 4: fitness
       
       
        # 5: Prediction Error
        # The Error of the prediction.
        # 6: Prediction
        # The prediction 0 minimum 1000 maximum.
        # 7: Experience
        # Trained times.
        # 8: AxtionSetSize
        # Niches
        # 9: Negative prediction
        # The total number of times this classifier was in a incorrect set
        # 10 Positive prediction
        #The total number of times this classifier was in a correct set
        rule=[]
        rule.append(condition) #0 condition
        rule.append(action) #1 action
        rule.append(numerosity) #2 numerosity
        rule.append(acc) #3 Accuracy
        rule.append(fit) #4 Fitness
        rule.append(P_E) #5 Prediction Error
        rule.append(Pre) #6 Prediction
        rule.append(Exp) #7 Experience
        rule.append(Ssize) # 8 ActionSetSize
        rule.append(0) # 9 Negative Prediction
        rule.append(0) # 10 Positive Prediction

        return rule

    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self,address):
        informations=self.Read_Information(address)
        for infor in informations:
            raw= infor.split('\n')[0].split(' ----> ')
            condition_action=raw[0].split(' : ')
            condition=self.read_condition(condition_action[0])
            action=int(condition_action[1])
            #print condition,len(condition)
            


            parameters=raw[1]
            
            val=self.read_details(parameters)
            rule=self.Create_new_Single_Rule(condition,action,val[0],val[1],val[2],val[3],val[4],val[5],val[6])
            self.micro_size+=val[1]
            self.population.append(rule)

    #read the condition part
    def read_condition(self,condition_list):
        conditions=condition_list.split(' ')[0:-1]
        condition=[]
        for cod in conditions:
            if cod!='#':
                if not '.' in cod:
                    condition.append(int(cod))
                else:
                    condition.append(float(cod))
            else:
                condition.append(cod)
        #print condition
        return condition


    #read the parameters
    def read_details(self,parameters):
        P_values=parameters.split(' ')
        parameters_list=[]

        parameter_list=[1,3,5,8,10,12,14]
        a_p_list=[]
        s_values=[]
        for i in range(0,len(P_values)):
            if i in parameter_list:
                s_values.append(P_values[i])
        for val in s_values:
            if '.' in val:
                a_p_list.append(float(val))
            else:
                a_p_list.append(int(val))

        return a_p_list

     ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
                  "Fit:", round(self.population[id][4],2),"Acc:", round(self.population[id][3],2))
