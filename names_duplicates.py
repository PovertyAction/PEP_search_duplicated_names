import pandas as pd
import numpy as np
from metaphone import doublemetaphone

class FullName:
  def __init__(self, first_name=None, middle_name=None, surname=None, second_surname=None, fullname=None, case_id = None, surveyed_or_hm = None, case_id_who_reffered=None, submissiondate=None):
    self.first_name = first_name
    self.middle_name = middle_name
    self.surname = surname
    self.second_surname = second_surname
    self.fullname = fullname

    self.case_id = case_id
    self.surveyed_or_hm = surveyed_or_hm

    self.case_id_who_reffered = case_id_who_reffered

    self.submissiondate = submissiondate

  def to_str(self):
    if(self.fullname):
      return self.fullname.lower()
    else:
      str_name = self.first_name
      if(self.middle_name):
        str_name += " "+self.middle_name
      if(self.surname):
        str_name += " "+self.surname
      if(self.second_surname):
        str_name += " "+ self.second_surname
      return str_name.lower()

  def get_doublemetaphone_list(self, include_middle_name_and_second_surname=True):
    if self.fullname:
      doublemetaphone_list = [doublemetaphone(name_part) for name_part in self.fullname.split(" ")]
    else:
      doublemetaphone_list = []
      doublemetaphone_list.append(doublemetaphone(self.first_name))
      if(include_middle_name_and_second_surname and self.middle_name):
        doublemetaphone_list.append(doublemetaphone(self.middle_name))
      if(self.surname):
        doublemetaphone_list.append(doublemetaphone(self.surname))
      if(include_middle_name_and_second_surname and self.second_surname):
        doublemetaphone_list.append(doublemetaphone(self.second_surname))

    return doublemetaphone_list

  def matches_with_doublemetaphone(self, existing_name):
    #Check if first name and last name metaphones exist in existing_name metaphone
    
    existing_name_metaphones = existing_name.get_doublemetaphone_list()

    #If we have the name disaggregated by different names, check only first name and surname
    if not self.fullname:
      if doublemetaphone(self.first_name) in existing_name_metaphones and doublemetaphone(self.surname) in existing_name_metaphones:
        return True
      else:
        return False

    #If we have the name in complete form, check that all its metaphone components are in the existing name emtaphone components
    else:
      name_doublemetaphone_list = self.get_doublemetaphone_list()

      all_name_doublemetaphone_in_existing_name =  all(elem in existing_name_metaphones for elem in name_doublemetaphone_list)

      return all_name_doublemetaphone_in_existing_name


  # def matches_name_with_jarowinkler(self, existing_name):

  #   jaro_distance = distance.get_jaro_distance(self.to_str(), existing_name.to_str(), winkler=True)

  #   if(jaro_distance>0.8):
  #     print("%s and %s: %f" % (self.to_str(), existing_name.to_str(), jaro_distance))

  #     print(distance.get_jaro_distance("felipe hernan alamos illanes", "felipe alamos", winkler=True))


  #     return True


def create_list_names_based_on_one_column(df, fullname_column):

  names_list = []
  
  #Remove columns with no fullname
  df = df[df[fullname_column]!='']
  
  for index, row in df.iterrows():
    if(fullname_column == 'full_name'):
      surveyed_or_hm = 'Encuestada'
    else:
      surveyed_or_hm = 'Miembra de hogar'

    full_name = FullName(fullname= row[fullname_column], case_id = row['caseid'], surveyed_or_hm = surveyed_or_hm, submissiondate=row['submissiondate'])
  
    names_list.append(full_name)

  return names_list

def create_list_names_based_on_many_columns(df, columns):

  names_list = []

  #Get columns associated with each part of name
  fn_c, mn_c, ln_c, sln_c, sex_c = columns
  
  #Filter out empty lists
  df_with_names = df[df[fn_c]!='']

  for index, row in df_with_names.iterrows():
    full_name = FullName(first_name = row[fn_c], middle_name = row[mn_c], surname= row[ln_c], second_surname = row[sln_c], case_id_who_reffered = row['caseid'], submissiondate=row['submissiondate'])

    names_list.append(full_name)

  return names_list
 
def name_in_list(list_names, name):
  for name_in_list in list_names:
    if name.matches_with_doublemetaphone(name_in_list):
      return True
  return False

def get_existing_names_in_db(df, source_columns):

  all_names = []
  for source_column in source_columns:
    
    names_to_add = create_list_names_based_on_one_column(df, source_column)

    #Add names to all_names if they dont exist
    for name in names_to_add:
      if not name_in_list(all_names, name):
        all_names.append(name)

  return all_names

def get_names_to_check(df, columns_to_check_list):
  all_names_to_check = []
  for columns_to_check in columns_to_check_list:
    names_to_check = create_list_names_based_on_many_columns(df, columns_to_check)

    #Add names to all_names_to_check if they dont exist
    for name in names_to_check:
      if not name_in_list(all_names_to_check, name):
        all_names_to_check.append(name)
  return all_names_to_check

def search_names_intersection(dataset_path):
  '''
  Check which names in columns_to_check already exist in database
  '''

  #LOAD AND FILTER DATASET
  #Load dataset
  df = pd.read_stata(dataset_path)

  #Filter df to only those with final_status=1 and collection_wave piloto2
  df = df[df['final_status']=='1']
  df = df[df['collection_wave']=='piloto2']

  #GET NAMES ALREADY EXISTING IN DATABASE

  #Select colums where we capture names already in database
  #We capture for sure from 'full_name' column.
  #We also consider members of hh. 
  max_n_hh_memb = int(df['hh_members'].max())
  source_columns = ['full_name']
  for i in range(1,max_n_hh_memb+1):
    col_name_member_i = 'name_'+str(i)
    source_columns.append(col_name_member_i)

  #Create list of names in source_columns
  existing_names = get_existing_names_in_db(df, source_columns)


  #GET NAMES THAT WE WANT TO CHECK IF THEY ALREADY EXIST IN DATABASE

  #Select columns with names we would like to check if they already exist in database
  columns_to_check_list = [['rds6_name1_1','rds6_name2_1','rds6_lastname1_1', 'rds6_lastname2_1', 'rds6_gender_1'],['rds6_name1_2','rds6_name2_2','rds6_lastname1_2', 'rds6_lastname2_2', 'rds6_gender_2'],['rds6_name1_3','rds6_name2_3','rds6_lastname1_3', 'rds6_lastname2_3', 'rds6_gender_3']]  

  #Create list of names in columns_to_check
  all_names_to_check = get_names_to_check(df, columns_to_check_list)

  #FIND INTERSECTION BETWEEN TWO GROUPS OF NAMES

  #Traverse all_names_to_check and see if they already exist in existing_names
  matches_results = []
  for name_to_check in all_names_to_check:
    found_match = False
    
    #Check if name_to_check matches with any of the existing_names
    for existing_name in existing_names:
      if(name_to_check.matches_with_doublemetaphone(existing_name)):
        # print("%s is already in database" % name_to_check.to_str())
        matches_results.append([name_to_check.to_str(), name_to_check.get_doublemetaphone_list(include_middle_name_and_second_surname=False),name_to_check.case_id_who_reffered, name_to_check.submissiondate,'Si', existing_name.to_str(), existing_name.get_doublemetaphone_list(include_middle_name_and_second_surname=False), existing_name.surveyed_or_hm, existing_name.case_id, existing_name.submissiondate, name_to_check.submissiondate < existing_name.submissiondate])
        found_match = True
        break #Do not keep looking in other existing names

    #If we got here, there was no match with any of existing names in database
    if not found_match:
      matches_results.append([name_to_check.to_str(), name_to_check.get_doublemetaphone_list(include_middle_name_and_second_surname=False), name_to_check.case_id_who_reffered, name_to_check.submissiondate,'No',  np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])

  #SAVE OUTPUT
  #Create an output database of matches_results
  matches_df = pd.DataFrame()
  matches_df = matches_df.append(matches_results)
  matches_df.columns=['Nombre Referido', 'Metaphone Referido', 'Referido en case id', 'Fecha referido:', 'Match?', 'Nombre Match', 'Methaphone_match','Match encuestada o hh memb.', 'Match caseid', 'Submissiondate match', 'Match posterior a referral?']
  
  # matches_df.to_csv('duplicates.csv', index=False)
  print(matches_df)

  return matches_df

def save_df_to_excel(saving_path, matches_df):

  writer = pd.ExcelWriter(saving_path, engine='xlsxwriter')

  # Convert the dataframe to an XlsxWriter Excel object.
  matches_df.to_excel(writer, sheet_name='Sheet1', index=False)

  # Get the xlsxwriter workbook and worksheet objects.
  workbook  = writer.book
  worksheet = writer.sheets['Sheet1']

  header_format = workbook.add_format({
      # 'bold': True,
      'text_wrap': True,
      'align': 'justify'})

  # Set the column width and format.
  worksheet.set_column('A:K', 20)#, header_format)

  # Close the Pandas Excel writer and output the Excel file.
  writer.save()



if __name__== "__main__":

  #Load file
  dataset_path = 'X:\\Box Sync\\CP_Projects\\IPA_COL_Projects\\3_Ongoing Projects\\IPA_COL_PEP\\07_Questionnaires&Data\\Baseline_Quant\\03_DataManagement\\02 Data backup and storage\\2. rawdata\\Survey\\stata databases\\encuesta_cuantitativa_bidpep.dta'
  
  #Find duplicates
  matches_df = search_names_intersection(dataset_path)

  save_df_to_excel("./results.xlsx", matches_df)