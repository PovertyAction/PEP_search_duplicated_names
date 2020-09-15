import pandas as pd
import numpy as np
from metaphone import doublemetaphone

class FullName:
  def __init__(self, first_name, middle_name, surname, second_surname):
    self.first_name = first_name
    self.middle_name = middle_name
    self.surname = surname
    self.second_surname = second_surname
    

  def print_name(self):
    print("first_name: %s, surname: %s" %(self.first_name, self.surname))

  def to_str(self):
    return ("%s %s" %(self.first_name, self.surname))

  # def to_str(self):
  #   full_name_string = ''
  #   for var in [self.first_name, self.middle_name, self.surname, self.second_surname]:
  #     if var:
  #       full_name_string = full_name_string + var + " "

  def matches_name_with_doublemetaphone(self, fullname):
    #Phonetic match using double metaphone 
    #Considers first_name and surname only

    if(doublemetaphone(self.first_name) == doublemetaphone(fullname.first_name) and \
    doublemetaphone(self.surname) == doublemetaphone(fullname.surname)):
      return True
    else:
      return False

def create_list_names(df, columns):

  names_list = []

  first_name_column, middle_name_column, last_name_column, second_last_name_column, sex_column = columns
  
  df_with_names = df[df[first_name_column]!='']

  for index, row in df_with_names.iterrows():
    full_name = FullName(row[first_name_column], row[middle_name_column], row[last_name_column], row[second_last_name_column])
  
    names_list.append(full_name)

  return names_list
 
def name_in_list(list_names, name):
  for name_in_list in list_names:
    if name.matches_name_with_doublemetaphone(name_in_list):
      return True
  return False

def search_names_intersection(dataset_path, source_columns, columns_to_check_list):
  '''
  Check which names in columns_to_check already exist in source_columns
  '''
  #Load dataset
  df = pd.read_stata(dataset_path)

  #Create list of names in source_columns
  existing_names = create_list_names(df, source_columns)

  #Create list of names in columns_to_check
  all_names_to_check = []
  for columns_to_check in columns_to_check_list:
    names_to_check = create_list_names(df, columns_to_check)

    #Add names to all_names_to_check if they dont exist
    for name in names_to_check:
      if not name_in_list(all_names_to_check, name):
        all_names_to_check.append(name)

  #Traverse all_names_to_check and check if they already exist in existing_names
  matches_results = []
  for name_to_check in all_names_to_check:
    found_match = False
    
    for existing_name in existing_names:
      if(name_to_check.matches_name_with_doublemetaphone(existing_name)):
        # print("%s is already in database" % name_to_check.to_str())
        matches_results.append([name_to_check.to_str(), 'Yes', existing_name.to_str()])
        found_match = True
        break #Do not keep looking in other existing names

    #If we got here, there was no match with any of existing names in database
    if not found_match:
      matches_results.append([name_to_check.to_str(), 'No', np.nan])


  #Create an output database of matches_results
  matches_df = pd.DataFrame()
  matches_df = matches_df.append(matches_results)
  matches_df.columns=['Name', 'Exists in database', 'Matches with']
  print(matches_df)