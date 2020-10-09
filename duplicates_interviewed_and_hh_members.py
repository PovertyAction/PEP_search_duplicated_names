import pandas as pd
from metaphone import doublemetaphone

def search_duplicates(dataset_path):
  '''
  Looks for duplicates between surveyed people and members of hh already interviewed
  '''

  #Load dataset
  df = pd.read_stata(dataset_path)

  #Task 1: Detect if person being interviewed was already named as a hh member in a previous survey
  #Strategy, loop over all rows, and:
  #1.1. Look at survey person and check if they are already in the list of hh members with a diff caseid.
  #1.2. Save hh_member in list if all_hh_members

  all_hh_members = []
  all_interviewed_people = {}
  interviewed_people_already_hh_member = {}

  for index, row in df.iterrows():
      caseid = row['caseid']

      #1.1 Check if surveyed person already exists in hh_member with a diff caseid
      fullname_interviewed_person = row['full_name']
      dm_interviewed_person = [doublemetaphone(w)[0] for w in fullname_interviewed_person.split(' ')]

      for hh_member in all_hh_members:
          #If doublemetaphone of fn and ln of hh member in dm_interviewed_person
          if hh_member['dm_fn'] in dm_interviewed_person and hh_member['dm_ln'] in dm_interviewed_person:
              if hh_member['case_id'] != caseid:
                  #Found someone! Lets check we havent already identified this person
                  if(fullname_interviewed_person not in interviewed_people_already_hh_member.keys()):
                      interviewed_people_already_hh_member[fullname_interviewed_person] =        {'fullname_interviewed':fullname_interviewed_person,
                      'caseid_interviewed':caseid,
                      'duplicated_with_hh_member':hh_member['full_name'],
                      'caseid_hh_member':hh_member['case_id']}
                  break #No need to continue looking at other hh_members

      #1.2 Add hh member to list of hh members
      fn_hh_member = row['name1']
      ln_hh_member = row['lastname1']
      fullname_hh_member = row['name']

      all_hh_members.append({'case_id':caseid,
                             'first_name':fn_hh_member,                       'dm_fn':doublemetaphone(fn_hh_member)[0],
                             'last_name':ln_hh_member,
                             'dm_ln':doublemetaphone(ln_hh_member)[0],
                             'full_name':fullname_hh_member})

      #Lastly, add fullname_interviewed_person to list of interviewed people. We will use this later
      #Use dictionary to avoid repetitions
      all_interviewed_people[fullname_interviewed_person] = {'fullname':fullname_interviewed_person,
      'caseid':caseid, 'dm':dm_interviewed_person}



  #Save output
  results_df = pd.DataFrame(columns=['Nombre encuestado', 'CaseId encuestado', 'Match con miembro hogar', 'CaseId miembro hogar'])
  for key, interviewed_people in interviewed_people_already_hh_member.items():
      results_df = results_df.append({
      'Nombre encuestado':interviewed_people['fullname_interviewed'],
      'CaseId encuestado':interviewed_people['caseid_interviewed'],
      'Match con miembro hogar':interviewed_people['duplicated_with_hh_member'],
      'CaseId miembro hogar':interviewed_people['caseid_hh_member']}, ignore_index=True)
  results_df.to_csv("Encuestados_que_ya_figuraban_en_un_hogar.csv", index=False)

  print(interviewed_people_already_hh_member)
  print(results_df)
  print("")

  #Task 2: Detect if a person being named as a hh member was already interviewed
  hh_member_already_interviewed = {}

  for index, row in df.iterrows():
      caseid = row['caseid']
      fn_hh_member = row['name1']
      ln_hh_member = row['lastname1']
      fullname_hh_member = row['name']

      #Check if hh member matches with any interviewed person
      for interviewed_person_fullname, interviewed_person in all_interviewed_people.items():
          if doublemetaphone(fn_hh_member)[0] in interviewed_person['dm'] and doublemetaphone(ln_hh_member)[0] in interviewed_person['dm']:
              if caseid != interviewed_person['caseid']:
                  #Check we havent already identified this person
                  if fullname_hh_member not in hh_member_already_interviewed.keys():
                      hh_member_already_interviewed[fullname_hh_member] =        {'fullname_hh_member':fullname_hh_member,
                      'caseid_hh_member':caseid,
                      'duplicated_with_interviewed':interviewed_person_fullname,
                      'caseid_interviewed':interviewed_person['caseid']}
                  break #No need to continue looking at other interviewed_people

  #Save output
  results_df = pd.DataFrame(columns=['Nombre miembro hh', 'CaseId miembro hogar', 'Match con entrevistado', 'CaseId entrevistado'])
  for key, hh_member in hh_member_already_interviewed.items():
        results_df = results_df.append({
        'Nombre miembro hh':hh_member['fullname_hh_member'],
        'CaseId miembro hogar':hh_member['caseid_hh_member'],
        'Match con entrevistado':hh_member['duplicated_with_interviewed'],
        'CaseId entrevistado':hh_member['caseid_interviewed']}, ignore_index=True)
  results_df.to_csv("Miembros_hogar_ya_encuestados.csv", index=False)

  print(hh_member_already_interviewed)
  print(results_df)

  return "'Encuestados_que_ya_figuraban_en_un_hogar.csv' and 'Miembros_hogar_ya_encuestados.csv'"

if __name__ == '__main__':
    file_path = "X:\PII\encuesta_cuantitativa_bidpep_cleaned_piloto2 - Copy.dta"
    search_duplicates(file_path)
