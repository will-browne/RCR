These compaction algorithms are based on the provided XCS and UCS. Readers can explain the Read_UCS_population.py or Read_XCS_Population to make the compact algorithms to support their own version.
 



Compaction:

Step 1: import Compaction
Step 
2: Instantiating the Compaction class

Sample:          Compaction(A folder storing the populations for compaction,
                                
                            System type: 0 :UCS 1:XCS,
                                 
                            Problem type: 0: MUX 1:Carry 2:Even parity 3: Majority-On
                                 
                            Number of features,
                                  
                            A list for identifying the compaction algorithms are going to run e.g. [0,1,3]  0: CRA 1: FU1 2: FU3 3: CRA2 4: k1 5: QRC 6: PDRC 7: RCR 8: RCR2 9:RCR3,
                                               Address of file for testing (only for real value domains) default:none ,
                  
                            Whether activate 10 folders cross-validation only for real value domains) default: False)

Results from the compaction algorithms will be stored in the Result folder.


Visualization:
Step 1: import Visualize_value_pattern
Step 2: Instantiating the Visualize_value_pattern class



In Value_knowledge class
when self.attribute_List=self.Calculate_Attribute_importance_distribution_Value() the visualization is AFVM
when self.attribute_List=self.Calculate_Attribute_importance_distribution_PureImportance() the visualization is AFIM

sample: Visualize_value_pattern(the address for the compacted population,
                                a list of plausible actions e.g. in Boolean domains this will be [0,1],
                                the address for storing the output visualizations)