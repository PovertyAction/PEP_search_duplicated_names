import names_duplicates as duplicates

if __name__== "__main__":

  #Load file
  dataset_path = 'X:\\Box Sync\\CP_Projects\\IPA_COL_Projects\\3_Ongoing Projects\\IPA_COL_PEP\\07_Questionnaires&Data\\Baseline_Quant\\03_DataManagement\\02 Data backup and storage\\2. rawdata\\Survey\\stata databases\\encuesta_cuantitativa_bidpep - Copy.dta'

  #Select colums with names already in the database
  source_columns = ['full_name','full_name','full_name','full_name', 'demo_102_1']

  #Select columns with names we would like to check if they already exist in database
  columns_to_check = [['rds6_name1_1','rds6_name2_1','rds6_lastname1_1', 'rds6_lastname2_1', 'rds6_gender_1'],['rds6_name1_2','rds6_name2_2','rds6_lastname1_2', 'rds6_lastname2_2', 'rds6_gender_2'],['rds6_name1_3','rds6_name2_3','rds6_lastname1_3', 'rds6_lastname2_3', 'rds6_gender_3']]  
  
  #Find duplicates
  duplicates.search_names_intersection(dataset_path, source_columns, columns_to_check)
