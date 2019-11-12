class Read_UCS_Population:
    def __init__(self,Address):
        self.population=[]
        self.micro_size=0
        self.Read(Address)
        
        #self.Print_Population()
        #print (self.micro_size)

    def Create_new_Single_Rule(self,condition,action,numerosity,fit,acc,Ssize,D_V,match_c,correct_c):
        # States of Attributes Specified in classifier (Ternary)
        # 0: condition 
        #class
        # 1: action 
        # The number of rule copies stored in the population.  (Indirectly stored as incremented numerosity)
        # 2: numerosity
        # Classifier fitness - initialized to a constant initial fitness value 
        # 3: fitness
        # Classifier accuracy - Accuracy calculated using only instances in the dataset which this rule matched.
        # 4: accuracy
        # A parameter used in deletion which reflects the size of match sets within this rule has been included.
        # 5: aveActionSetSize
        # The current deletion weight for this classifier.
        # 6: deletionvote
        # Time since rule last in a correct set.
        # 7: timeStampGA
        # Iteration in which the rule first appeared.
        # 8: initiTieStamp
        # Known in many LCS implementations as experience i.e. the total number of times this classifier was in a match set
        # 9: match count
        # The total number of times this classifier was in a correct set
        # 10 correct count

        rule=[]
        rule.append(condition) #0 condition
        rule.append(action) #1 action
        rule.append(numerosity) #2 numerosity
        rule.append(fit) #3 fitness
        rule.append(acc) #4 accuracy
        rule.append(Ssize) #5 aveActionSetSize
        rule.append(D_V) #6 deletionvote
        rule.append(1) #7 timeStampGA
        rule.append(1) # 8 initiTieStamp
        rule.append(match_c) # 9 match count
        rule.append(correct_c) # 10 correct count

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
            raw= infor.split('\n')[0].split('->')
            condition=raw[0]
            condition=self.read_condition(condition)
            #actions and parameters
            a_p=raw[1]
            val=self.read_details(a_p)
            rule=self.Create_new_Single_Rule(condition,val[0],val[1],val[2],val[3],val[4],val[5],val[8],val[9])
            self.micro_size+=val[1]
            self.population.append(rule)

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

    def read_details(self,a_p):
        s_values=a_p.split(' ')[0:-1]

        a_p_list=[]
        for val in s_values:
            if '.' in val:
                a_p_list.append(float(val))
            else:
                a_p_list.append(int(val))

        #print a_p_list
        return a_p_list

    ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
                  "Fit:", round(self.population[id][3],2),"Acc:", round(self.population[id][4],2))