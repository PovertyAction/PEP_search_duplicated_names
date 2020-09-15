import names_duplicates as duplicates

if __name__== "__main__":

	#Load file
	dataset_path = './example_db.csv' 

	#Select colums with names already in the database
	source_columns = ['first_name_1','first_name_2','last_name']

	#Select columns with names we would like to check if they already exist in database
	columns_to_check = [['reffered_1_fn_1','reffered_1_fn_1_2','reffered_1_ln'],['reffered_2_fn_1','reffered_2_fn_2','reffered_2_ln'],['reffered_3_fn_1','reffered_3_fn_2','reffered_3_ln']]	
	
	#Find duplicates
	duplicates.search_names_intersection(dataset_path, source_columns, columns_to_check)
