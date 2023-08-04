from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql
import pandas as pd
import re
from tkinter import messagebox
from datetime import datetime
from sqlalchemy import create_engine
from string import ascii_lowercase as alc
import matplotlib.pyplot as plt
import traceback
import math
import numpy as np
import os.path 
import glob

#https://www.bing.com/videos/search?q=tkiner+python&docid=607990399693972571&mid=5011DB274D7235DB11195011DB274D7235DB1119&view=detail&FORM=VIRE
#https://www.pythontutorial.net/tkinter/tkinter-validation/

root = Tk()
root.title('JES Database Access')
# root.iconbitmap(r'JES_logo.ico')
root.geometry("800x800")

# Creating a Label Widget
Data_upload_label = Label(root, text = "Upload Sample Data Here", font = 'bold').place(relx=0.5, rely=0.025, anchor=CENTER)
Failure_Log_label = Label(root, text = "Log Sample Failures Here", font = 'bold').place(relx=0.5, rely=0.3, anchor=CENTER)
Maccor_file_label = Label(root, text = "Maccor Testing Here", font = 'bold').place(relx=0.5, rely=0.45, anchor=CENTER)
Plot_data_label = Label(root, text = "Pull and Plot Data Here", font = 'bold').place(relx=0.5, rely=0.6, anchor=CENTER)
Error_handling_label = Label(root, text = "Error Handling Here", font = 'bold').place(relx=0.5, rely=0.75, anchor=CENTER)

version_label = Label(root, text = "Version 27, 03-20-2023").place(relx=0.08, rely=0.98, anchor=CENTER)

# Validation for text entry
def callback_date(input):
	date_pattern = r'\d{4}-\d{2}-\d{2}'
	if re.fullmatch(date_pattern, input) is None:
		return False
	else:

		return True

def callback_time(input):
	id_pattern = r'\d{2}:\d{2}:\d{2}'
	if re.fullmatch(id_pattern, input) is None:
		return False
	else:
		return True

def callback_int(input):
	try:
		int(input)
		return True
	except:
		return False

def callback_float(input):
	try:
		float(input)
		return True
	except:
		return False

def invalid_date():
	messagebox.showerror('date error', 'Make sure you are entering the date in the format "YYYY-MM-DD"')

def invalid_int():
	messagebox.showerror('int error', 'Make sure you are entering an integer')

def invalid_float():
    messagebox.showerror('float error', 'Make sure you are entering a number')

def invalid_time():
    messagebox.showerror('time error', 'Make sure you are entering the time in the format "HH:MM:SS"')

# MW and mol information

MW = {'Li2B4O7': 169.233, 'SiO2': 60.083, 'B2O3': 69.617, 'Li2O': 29.999, 'Li2CO3': 74.008, 'LiBO2': 49.808, 'Li3BO3': 79.807, 'Li2O2': 45.998, 'LiOH': 24.007, 'K2CO3' : 138.2046, 'MoO3': 143.947, 'V2O5': 181.878, 'NbO': 108.90537, 'LiCl': 42.45, 'Na2SO4': 142.0455, 'Li2SO4' : 110.066, 'LiI': 133.9045, 'Li3N': 35.007, 'Al2O3': 101.960076, 'C': 12.011, 'LiF': 25.99840316, 'Li2SiO3': 90.082, 'Li4SiO4': 120.081, 'B2S3': 117.83, 'SiS2': 92.225, 'Li2S': 46.07, 'LiPO3': 85.970762, 'SiI4': 535.703, 'SiCl4': 169.885, 'P2O3.5N': 131.951024, 'GeS2': 136.77, 'LiTSFI': 287.155419, 'LiBr': 86.9, 'S': 28.0855, 'B': 10.811, 'LiBF4': 93.804, 'BN': 24.817, 'LiPF6': 151.964181, 'SiO' : 44.085}

mol = {'Li2B4O7': [2, 4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
'SiO2': [0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'B2O3': [0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li2O': [2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
'Li2CO3': [2, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiBO2': [1, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li3BO3': [3, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li2O2': [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiOH': [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
'K2CO3' : [0, 0, 0, 3, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'MoO3': [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'V2O5': [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
'NbO': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
'LiCl': [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Na2SO4': [0, 0, 0, 4, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li2SO4' : [2, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiI': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
'Li3N': [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
'Al2O3': [0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
'C': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiF': [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li2SiO3': [2, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li4SiO4': [4, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'B2S3': [0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'SiS2': [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'Li2S': [2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiPO3': [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
'SiI4': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
'SiCl4': [0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'P2O3.5N': [0, 0, 0, 3.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0],
'GeS2': [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
'LiTSFI': [1, 0, 0, 4, 2, 0, 6, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
'LiBr': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
'S': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'B':[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'LiBF4': [1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
'BN':[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
'LiPF6':[1, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
'SiO': [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

element_label = ['Li', 'B', 'Si', 'O', 'C', 'Cl', 'F', 'S', 'Na', 'K', 'Mo', 'V', 'I', 'N', 'Al', 'Nb', 'P', 'H', 'Ge', 'Br']
compounds = pd.DataFrame.from_dict(mol, orient='index', columns = element_label)
compounds['MW'] = pd.Series(MW)

materials_list = ['Li2B4O7', 'SiO2', 'B2O3', 'Li2O', 'Li2CO3', 'LiBO2', 'Li3BO3', 'Li2O2', 'LiOH', 'K2CO3', 'MoO3', 'V2O5', 'NbO', 'LiCl', 'Na2SO4', 'Li2SO4', 'LiI', 'Li3N', 'Al2O3', 'C', 'LiF', 'Li2SiO3', 'Li4SiO4', 'B2S3', 'SiS2', 'Li2S', 'LiPO3', 'SiI4', 'SiCl4', 'P2O3.5N', 'GeS2', 'LiTSFI', 'LiBr', 'S', 'B', 'LiBF4', 'BN', 'LiPF6', 'SiO']

# Submit commands for Data Entry Tables
def submit_llzo():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			cursor.execute("Insert into LLZO values (%s, %s, %s, %s, %s);",
				(llzo_id.get(),
				date_made.get(),
				date_rm.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			llzo_id.delete(0, END)
			#date_made.delete(0, END)
			#date_rm.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		cursor.close()
		conn.commit()
		conn.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_Li3BO3():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			cursor.execute("Insert into Li3BO3 values (%s, %s, %s, %s, %s);",
				(li3bo3_id.get(),
				date_made.get(),
				i_o.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			li3bo3_id.delete(0, END)
			#date_made.delete(0, END)
			i_o.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def subtract_starting_material_mass(mat_dict):
	# connect to db
	engine = create_engine("mysql+pymysql://JESAdmin:&JeS2022**Z@192.168.0.39:3306/cells")
	connection = engine.connect()

	# Get existing masses
	query = 'SELECT * FROM cells.starting_materials order by date desc;'
	existing = connection.execute(query).fetchone()

	updated = {list(mat_dict.keys())[i]: [m - list(mat_dict.values())[i]] for i, m in enumerate(existing[1:])}

	updated['date'] = str(datetime.now(tz=None).strftime("%Y-%m-%d %H:%M:%S"))

	# Convert dict to df
	updated = pd.DataFrame.from_dict(updated)

	# Insert into DB
	updated.to_sql("starting_materials", con = engine, if_exists = "append", index=False)


def submit_lbcso_glass():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		materials_wt_list = [li2b4o7_wt_pct.get(), sio2_wt_pct.get(), b2o3_wt_pct.get(), 0, li2co3_wt_pct.get(), libo2_wt_pct.get(), li3bo3_wt_pct.get(), li2o2_wt_pct.get(), 0, 0, 0, 0, 0, 0, 0, li2so4_wt_pct.get(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		materials_wt_list = ['0' if mat == '' else float(mat) for mat in materials_wt_list]

		materials_mass_list = [float(mat)*float(total_mass.get()) for mat in materials_wt_list]

		if float(materials_wt_list[1]) == float(materials_wt_list[2]):
			glass_type = '50/50'
		elif float(materials_wt_list[1]) > float(materials_wt_list[2]):
			glass_type = 'Baseline'
		else:
			glass_type = None

		materials_mol_list = []

		for i, mat in enumerate(materials_mass_list):
			materials_mol_list.append(mat/compounds.loc[materials_list[i], 'MW'])

		element_mol_list = compounds.loc[:, element_label].transpose().dot(pd.Series(materials_mol_list, index = materials_list))

		total_mols = element_mol_list.sum()

		element_mol_pct = [float(el)/float(total_mols) for el in element_mol_list]


		try:
			cursor.execute("Insert into glass values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(glass_id.get(),
				glass_type,
				date_made.get(),
				None,
				materials_wt_list[0],
				materials_mass_list[0], 
				materials_wt_list[1],
				materials_mass_list[1], 
				materials_wt_list[2],
				materials_mass_list[2],
				materials_wt_list[3],
				materials_mass_list[3],
				materials_wt_list[4],
				materials_mass_list[4], 
				materials_wt_list[5],
				materials_mass_list[5], 
				materials_wt_list[6],
				materials_mass_list[6],
				materials_wt_list[7],
				materials_mass_list[7],
				materials_wt_list[8],
				materials_mass_list[8], 
				materials_wt_list[9],
				materials_mass_list[9],
				materials_wt_list[10],
				materials_mass_list[10],
				materials_wt_list[11],
				materials_mass_list[11], 
				materials_wt_list[12],
				materials_mass_list[12],
				materials_wt_list[13],
				materials_mass_list[13],
				materials_wt_list[14],
				materials_mass_list[14], 
				materials_wt_list[15],
				materials_mass_list[15], 
				materials_wt_list[16],
				materials_mass_list[16],
				materials_wt_list[17],
				materials_mass_list[17],
				materials_wt_list[18],
				materials_mass_list[18], 
				materials_wt_list[19],
				materials_mass_list[19],
				materials_wt_list[20],
				materials_mass_list[20], 
				materials_wt_list[21],
				materials_mass_list[21], 
				materials_wt_list[22],
				materials_mass_list[22],
				materials_wt_list[23],
				materials_mass_list[23],
				materials_wt_list[24],
				materials_mass_list[24], 
				materials_wt_list[25],
				materials_mass_list[25], 
				materials_wt_list[26],
				materials_mass_list[26],
				materials_wt_list[27],
				materials_mass_list[27],
				materials_wt_list[28],
				materials_mass_list[28], 
				materials_wt_list[29],
				materials_mass_list[29],
				materials_wt_list[30],
				materials_mass_list[30],
				materials_wt_list[31],
				materials_mass_list[31],
				materials_wt_list[32],
				materials_mass_list[32],
				materials_wt_list[33],
				materials_mass_list[33],
				materials_wt_list[34],
				materials_mass_list[34],
				materials_wt_list[35],
				materials_mass_list[35],
				materials_wt_list[36],
				materials_mass_list[36],
				materials_wt_list[37],
				materials_mass_list[37],
				materials_wt_list[38],
				materials_mass_list[38],
				element_mol_pct[0],
				element_mol_pct[1],
				element_mol_pct[2],
				element_mol_pct[3],
				element_mol_pct[4],
				element_mol_pct[5],
				element_mol_pct[6],
				element_mol_pct[7],
				element_mol_pct[8],
				element_mol_pct[9],
				element_mol_pct[10],
				element_mol_pct[11],
				element_mol_pct[12],
				element_mol_pct[13],
				element_mol_pct[14],
				element_mol_pct[15],
				element_mol_pct[16],
				element_mol_pct[17],
				element_mol_pct[18],
				element_mol_pct[19],
				furnace_temp.get(),
				furnace_time.get(),
				None,
				None,
				li3bo3_id.get(),
				None,
				None,
				total_mass.get(),
				None,
				None,
				num_melts.get(),
				comments.get(),
				initial.get()))

			if date_rm.get() != '':
				cursor.execute("update glass set date_rm = %s where glass_id = %s", (date_rm.get(), glass_id.get()))
		
			# Clear text boxes
			glass_id.delete(0, END)
			#date_made.delete(0, END)
			#li3bo3_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

			# Update starting material mass records
			mat_dict = dict(zip(materials_list, materials_mass_list))
			subtract_starting_material_mass(mat_dict)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()

	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_LIBOSS_glass(code):

	if initial.get():

		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		if code == 'Exp':
			mat_list = [mat1.get(), mat2.get(), mat3.get(), mat4.get(), mat5.get(), mat6.get(), mat7.get(), mat8.get(), mat9.get()]
			mat_mass_list = [mat1_mass.get(), mat2_mass.get(), mat3_mass.get(), mat4_mass.get(), mat5_mass.get(), mat6_mass.get(), mat7_mass.get(), mat8_mass.get(), mat9_mass.get()]
			mf = mass_factor
			total = mf*float(total_mass.get())
			prep = preparation.get()
			code = name.get()
		else:
			mat_list = [mat1, mat2, mat3, mat4, mat5, mat6, mat7, mat8, mat9]
			mat_mass_list = [mat1_mass, mat2_mass, mat3_mass, mat4_mass, mat5_mass, mat6_mass, mat7_mass, mat8_mass, mat9_mass]
			mf = float(mass_factor.get())
			total = float(mf)*total_mass
			prep = preparation

		if recovery.get() != '':
			rec = float(recovery.get())/total*100
		else:
			rec = None

		mat_list = [None if mat == 'None' else mat for mat in mat_list]
		mat_list = list(filter(lambda item: item is not None, mat_list))

		mat_mass_list = [None if mat == '' else float(mat)*mf for mat in mat_mass_list]
		mat_mass_list = list(filter(lambda item: item is not None, mat_mass_list))

		ind = []

		for mat in mat_list:
			ind.append(materials_list.index(mat))

		materials_mass_list = [0]*39
		for i, m in zip(ind, mat_mass_list):
			materials_mass_list[i] = m

		materials_wt_list = [float(mat)/total for mat in materials_mass_list]
		
		materials_mol_list = []

		for i, mat in enumerate(materials_mass_list):
			materials_mol_list.append(mat/compounds.loc[materials_list[i], 'MW'])

		element_mol_list = compounds.loc[:, element_label].transpose().dot(pd.Series(materials_mol_list, index = materials_list))

		total_mols = element_mol_list.sum()

		element_mol_pct = [float(el)/float(total_mols) for el in element_mol_list]


		try:
			cursor.execute("Insert into glass values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(glass_id.get(),
				code,
				date_made.get(),
				prep,
				materials_wt_list[0],
				materials_mass_list[0], 
				materials_wt_list[1],
				materials_mass_list[1], 
				materials_wt_list[2],
				materials_mass_list[2],
				materials_wt_list[3],
				materials_mass_list[3],
				materials_wt_list[4],
				materials_mass_list[4], 
				materials_wt_list[5],
				materials_mass_list[5], 
				materials_wt_list[6],
				materials_mass_list[6],
				materials_wt_list[7],
				materials_mass_list[7],
				materials_wt_list[8],
				materials_mass_list[8], 
				materials_wt_list[9],
				materials_mass_list[9],
				materials_wt_list[10],
				materials_mass_list[10],
				materials_wt_list[11],
				materials_mass_list[11], 
				materials_wt_list[12],
				materials_mass_list[12],
				materials_wt_list[13],
				materials_mass_list[13],
				materials_wt_list[14],
				materials_mass_list[14], 
				materials_wt_list[15],
				materials_mass_list[15], 
				materials_wt_list[16],
				materials_mass_list[16],
				materials_wt_list[17],
				materials_mass_list[17],
				materials_wt_list[18],
				materials_mass_list[18], 
				materials_wt_list[19],
				materials_mass_list[19],
				materials_wt_list[20],
				materials_mass_list[20], 
				materials_wt_list[21],
				materials_mass_list[21], 
				materials_wt_list[22],
				materials_mass_list[22],
				materials_wt_list[23],
				materials_mass_list[23],
				materials_wt_list[24],
				materials_mass_list[24], 
				materials_wt_list[25],
				materials_mass_list[25], 
				materials_wt_list[26],
				materials_mass_list[26],
				materials_wt_list[27],
				materials_mass_list[27],
				materials_wt_list[28],
				materials_mass_list[28], 
				materials_wt_list[29],
				materials_mass_list[29],
				materials_wt_list[30],
				materials_mass_list[30],
				materials_wt_list[31],
				materials_mass_list[31],
				materials_wt_list[32],
				materials_mass_list[32],
				materials_wt_list[33],
				materials_mass_list[33],
				materials_wt_list[34],
				materials_mass_list[34],
				materials_wt_list[35],
				materials_mass_list[35],
				materials_wt_list[36],
				materials_mass_list[36],
				materials_wt_list[37],
				materials_mass_list[37],
				materials_wt_list[38],
				materials_mass_list[38],
				element_mol_pct[0],
				element_mol_pct[1],
				element_mol_pct[2],
				element_mol_pct[3],
				element_mol_pct[4],
				element_mol_pct[5],
				element_mol_pct[6],
				element_mol_pct[7],
				element_mol_pct[8],
				element_mol_pct[9],
				element_mol_pct[10],
				element_mol_pct[11],
				element_mol_pct[12],
				element_mol_pct[13],
				element_mol_pct[14],
				element_mol_pct[15],
				element_mol_pct[16],
				element_mol_pct[17],
				element_mol_pct[18],
				element_mol_pct[19],
				furnace_temp.get(),
				furnace_time.get(),
				None,
				None,
				None,
				None,
				'Fume Silica',
				total,
				None,
				rec,
				num_melts.get(),
				comments.get(),
				initial.get()))
		
			# Clear text boxes
			glass_id.delete(0, END)
			#date_made.delete(0, END)
			#li3bo3_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

			# Update starting material mass records
			mat_dict = dict(zip(materials_list, materials_mass_list))
			subtract_starting_material_mass(mat_dict)
		
		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()

	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

# def submit_LIBOSS_add():
# 	if initial.get():
# 		# Connect to DB
# 		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
# 		cursor = conn.cursor()

# 		mat = material.get()
# 		mat_mass = float(mass_liboss.get()) / float(ratio_1.get()) * float(ratio_2.get())

# 		cursor.execute('select glass_type from glass where glass_id like %s', liboss_base.get())
# 		glass_type = cursor.fetchone()["glass_type"] + ' ' + ratio_1.get() + ':' + ratio_2.get() + ' '+ mat

# 		cursor.execute('select li2s_mass, b2s3_mass, b_mass, s_mass, lii_mass, sio2_mass from glass where glass_id like %s', liboss_base.get())
# 		result = cursor.fetchone()
# 		materials_mass_list = [result["li2s_mass"], result["b2s3_mass"], result["b_mass"], result["s_mass"], result["lii_mass"], result["sio2_mass"], mat_mass]
# 		materials_mass_list = ['0' if mat == '' else mat for mat in materials_mass_list]

# 		total = float(materials_mass_list[0]) + float(materials_mass_list[1]) + float(materials_mass_list[2]) + float(materials_mass_list[3]) + float(materials_mass_list[4]) + float(materials_mass_list[5]) + float(materials_mass_list[6])
# 		materials_wt_list = [float(mat)/total for mat in materials_mass_list]

# 		str1 = mat + '_wt_pct'
# 		str2 = mat + '_mass'

# 		cursor.execute('select b2s3_id from glass where glass_id like %s', liboss_base.get())
# 		b2s3_id = cursor.fetchone()["b2s3_id"]

# 		query = "Insert into glass (glass_id, glass_type, liboss_base, date_made, li2s_wt_pct, b2s3_wt_pct, b_wt_pct, s_wt_pct, lii_wt_pct, sio2_wt_pct, {}, li2s_mass, b2s3_mass, b_mass, s_mass, lii_mass, sio2_mass, {}, b2s3_id, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(str1, str2)

# 		try:
# 			cursor.execute(query,
# 				(glass_id.get(),
# 				glass_type,
# 				liboss_base.get(),
# 				date_made.get(),
# 				materials_wt_list[0], 
# 				materials_wt_list[1], 
# 				materials_wt_list[2], 
# 				materials_wt_list[3],
# 				materials_wt_list[4],
# 				materials_wt_list[5],
# 				materials_wt_list[6],
# 				materials_mass_list[0], 
# 				materials_mass_list[1], 
# 				materials_mass_list[2], 
# 				materials_mass_list[3],
# 				materials_mass_list[4],
# 				materials_mass_list[5],
# 				materials_mass_list[6],
# 				b2s3_id,
# 				comments.get(),
# 				initial.get()))

# 			# Clear text boxes
# 			glass_id.delete(0, END)
# 			comments.delete(0, END)
# 			initial.delete(0, END)

# 		except:
# 			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
# 		# Close connection
# 		conn.commit()
# 		conn.close()
# 		cursor.close()

# 		# Update starting material mass records
# 		mat_dict = dict(zip(materials_list, materials_mass_list))
# 		subtract_starting_material_mass(mat_dict)

# 	else:
# 		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

# def submit_LIBOSS_glass(pct):
# 	if initial.get():
# 		# Connect to DB
# 		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
# 		cursor = conn.cursor()

# 		if recovery.get() != '':
# 			rec = float(recovery.get())/float(total_mass.get())*100
# 		else:
# 			rec = None
		
# 		if (mat1.get() == 'None') and (mat2.get() == 'None'):
# 			materials_mass_list = [li2s_mass.get(), b2s3_mass.get(), b_mass.get(), s_mass.get(), lii_mass.get(), sio2_mass.get()]
# 			materials_mass_list = ['0' if mat == '' else float(mat)/100 for mat in materials_mass_list]

# 			materials_wt_list = [float(mat)*float(total_mass.get()) for mat in materials_mass_list]

# 			glass_type = str(pct) + 'Experimental LIBOSS'

# 			try:
# 				cursor.execute("Insert into glass (glass_id, glass_type, date_made, preparation, total_mass, li2s_wt_pct, b2s3_wt_pct, b_wt_pct, s_wt_pct, lii_wt_pct, sio2_wt_pct, li2s_mass, b2s3_mass, b_mass, s_mass, lii_mass, sio2_mass, b2s3_id, sio2_type, furnace_temp, furnace_time, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
# 					(glass_id.get(),
# 					glass_type,
# 					date_made.get(),
# 					preparation.get(),
# 					total_mass.get(),
# 					materials_wt_list[0], 
# 					materials_wt_list[1], 
# 					materials_wt_list[2], 
# 					materials_wt_list[3],
# 					materials_wt_list[4],
# 					materials_wt_list[5],
# 					materials_mass_list[0], 
# 					materials_mass_list[1], 
# 					materials_mass_list[2], 
# 					materials_mass_list[3],
# 					materials_mass_list[4], 
# 					materials_mass_list[5],
# 					b2s3_id.get(),
# 					sio2_type.get(),
# 					furnace_temp.get(),
# 					furnace_time.get(),
# 					comments.get(),
# 					initial.get()))

# 				# Clear text boxes
# 				glass_id.delete(3, END)
# 				comments.delete(0, END)
# 				initial.delete(0, END)

# 			except:
# 				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
# 			# Close connection
# 			conn.commit()
# 			conn.close()
# 			cursor.close()

# 		elif (mat1.get() == 'None') or (mat2.get() =='None'):

# 			if mat1.get() == 'None':
# 				material = mat2.get()
# 				material_mass = mat2_mass.get()
# 			elif mat2.get() == 'None':
# 				material = mat1.get()
# 				material_mass = mat1_mass.get()

# 			materials_mass_list = [li2s_mass.get(), b2s3_mass.get(), b_mass.get(), s_mass.get(), lii_mass.get(), sio2_mass.get(), material_mass]
# 			materials_mass_list = ['0' if mat == '' else float(mat) for mat in materials_mass_list]

# 			materials_wt_list = [float(mat)/float(total_mass.get()) for mat in materials_mass_list]

# 			glass_type = 'Experimental LIBOSS'

# 			str1 = material + '_wt_pct'
# 			str2 = material + '_mass'

# 			query = "Insert into glass (glass_id, glass_type, date_made, preparation, total_mass, li2s_wt_pct, b2s3_wt_pct, b_wt_pct, s_wt_pct, lii_wt_pct, sio2_wt_pct, {}, li2s_mass, b2s3_mass, b_mass, s_mass, lii_mass, sio2_mass, {}, b2s3_id, sio2_type, furnace_temp, furnace_time, recovery, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(str1, str2)

# 			try:
# 				cursor.execute(query,
# 					(glass_id.get(),
# 					glass_type,
# 					date_made.get(),
# 					preparation.get(),
# 					total_mass.get(),
# 					materials_wt_list[0], 
# 					materials_wt_list[1], 
# 					materials_wt_list[2], 
# 					materials_wt_list[3],
# 					materials_wt_list[4],
# 					materials_wt_list[5],
# 					materials_wt_list[6],
# 					materials_mass_list[0], 
# 					materials_mass_list[1], 
# 					materials_mass_list[2], 
# 					materials_mass_list[3],
# 					materials_mass_list[4], 
# 					materials_mass_list[5],
# 					materials_mass_list[6],
# 					b2s3_id.get(),
# 					sio2_type.get(),
# 					furnace_temp.get(),
# 					furnace_time.get(),
# 					rec,
# 					comments.get(),
# 					initial.get()))

# 				# Clear text boxes
# 				glass_id.delete(3, END)
# 				comments.delete(0, END)
# 				initial.delete(0, END)

# 			except:
# 				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
# 			# Close connection
# 			conn.commit()
# 			conn.close()
# 			cursor.close()
# 		else:
# 			materials_mass_list = [li2s_mass.get(), b2s3_mass.get(), b_mass.get(), s_mass.get(), lii_mass.get(), sio2_mass.get(), mat1_mass.get(), mat2_mass.get()]
# 			materials_mass_list = ['0' if mat == '' else float(mat) for mat in materials_mass_list]

# 			materials_wt_list = [float(mat)/float(total_mass.get()) for mat in materials_mass_list]

# 			glass_type = 'Experimental LIBOSS'

# 			str1 = mat1.get() + '_wt_pct'
# 			str2 = mat1.get() + '_mass'
# 			str3 = mat2.get() + '_wt_pct'
# 			str4 = mat2.get() + '_mass'

# 			query = "Insert into glass (glass_id, glass_type, date_made, preparation, total_mass, li2s_wt_pct, b2s3_wt_pct, b_wt_pct, s_wt_pct, lii_wt_pct, sio2_wt_pct, {}, {}, li2s_mass, b2s3_mass, b_mass, s_mass, lii_mass, sio2_mass, {}, {}, b2s3_id, sio2_type, furnace_temp, furnace_time, recovery, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(str1, str3, str2, str4)

# 			try:
# 				cursor.execute(query,
# 					(glass_id.get(),
# 					glass_type,
# 					date_made.get(),
# 					preparation.get(),
# 					total_mass.get(),
# 					materials_wt_list[0], 
# 					materials_wt_list[1], 
# 					materials_wt_list[2], 
# 					materials_wt_list[3],
# 					materials_wt_list[4],
# 					materials_wt_list[5],
# 					materials_wt_list[6],
# 					materials_wt_list[7],
# 					materials_mass_list[0], 
# 					materials_mass_list[1], 
# 					materials_mass_list[2], 
# 					materials_mass_list[3],
# 					materials_mass_list[4], 
# 					materials_mass_list[5],
# 					materials_mass_list[6],
# 					materials_mass_list[7],
# 					b2s3_id.get(),
# 					sio2_type.get(),
# 					furnace_temp.get(),
# 					furnace_time.get(),
# 					rec,
# 					comments.get(),
# 					initial.get()))

# 				# Clear text boxes
# 				glass_id.delete(3, END)
# 				comments.delete(0, END)
# 				initial.delete(0, END)

# 			except:
# 				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
# 			# Close connection
# 			conn.commit()
# 			conn.close()
# 			cursor.close()

# 	else:
# 		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')


def submit_ISU_glass():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		try:
			cursor.execute("Insert into glass (glass_id, glass_type, date_made, comments, initials) values (%s, %s, %s, %s, %s);",
				(glass_id.get(),
				'ISU',
				date_made.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			glass_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
		# Close connection
		conn.commit()
		conn.close()
		cursor.close()

	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_lnto():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			cursor.execute("Insert into LNTO values (%s, %s, %s, %s);",
				(lnto_id.get(),
				date_made.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			lnto_id.delete(0, END)
			#date_made.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_substrate_sputter():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		substrate_type = coating.get() + 'on' + base_foil.get()

		try:
			cursor.execute("Insert into cathode_substrate (substrate_id, substrate_type, base_foil, coating, date_made, sputter_duration, sputter_pressure, sputter_power, cleaning_time, blue, comments, initial) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(substrate_id.get(),
				substrate_type.get(),
				base_foil.get(),
				coating.get(),
				date_made.get(),
				sputter_duration.get(),
				sputter_pressure.get(),
				sputter_power.get(),
				cleaning_time.get(),
				blue.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			substrate_id.delete(0, END)
			substrate_id.insert(0, 'B23')
			sputter_pressure.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_substrate_cast():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		substrate_type = coating.get() + 'on' + base_foil.get() 

		try:
			cursor.execute("Insert into cathode_substrate (substrate_id, substrate_type, base_foil, coating, date_made, coating_mass, solvent_type, solvent_mass, casting_height, cure_temp, cure_time, comments, initial) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(substrate_id.get(),
				substrate_type.get(),
				base_foil.get(),
				coating.get(),
				date_made.get(),
				coating_mass.get(),
				solvent_type.get(),
				solvent_mass.get(),
				casting_height.get(),
				cure_temp.get(),
				cure_time.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			substrate_id.delete(0, END)
			substrate_id.insert(0, 'B23')
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_sulfide_cathode(code):
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		if float(active_material_vol_percent.get()) < 1:
			a_vol = active_material_vol_percent.get()*100
		else:
			a_vol = active_material_vol_percent.get()
		
		if float(cnt_wt_pct.get()) < 1:
			cnt_wt = str(float(cnt_wt_pct.get())*100)
		else:
			cnt_wt = cnt_wt_pct.get()

		if code == 'mix':
			name = description.get() + ' Sp Mix Sulfide'
		elif code == 'mill':
			name = description.get() + ' Milled Sulfide'

		try:
			cursor.execute("Insert into Cathode (cathode_id, cathode_type, date_made, particle_coating, casting_coating, active_material_vol, active_material_type, active_material_mass, packing_density, glass_id, Glass_mass, dispersant_type, dispersant_mass, solvent1_type, solvent1_mass, substrate_id, casting_temp, casting_bar_setting, casting_bar_type, estimated_thickness, heat_treatment_temp, heat_treatment_time, num_rolling_layers, roller, rolling_procedure, LNTO_coating, cnt_wt_pct, cnt_mass, samples_per_batch, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(cathode_id.get(),
				name,
				date_made.get(),
				particle_coating.get(),
				casting_coating.get(),
				a_vol,
				active_material_type.get(),
				active_material_mass.get(),
				packing_density.get(),
				Glass_id.get(),
				Glass_mass.get(),
				dispersant_type.get(),
				dispersant_mass.get(),
				solvent1_type.get(),
				solvent1_mass.get(),
				substrate_id.get(),
				casting_temp.get(),
				casting_bar_setting.get(),
				casting_bar_type.get(),
				estimate_cathode_thickness.get(),
				heat_treatment_temp.get(),
				heat_treatment_time.get(),
				num_rolling_layers.get(),
				roller.get(),
				rolling_procedure.get(),
				LNTO_coating.get(),
				cnt_wt,
				cnt_mass.get(),
				samples.get(),
				comments.get(),
				initial.get()))

			if composite_density.get() != '':
				cursor.execute("update cathode set composite_density = %s where cathode_id = %s", (composite_density.get(), cathode_id.get()))

			if silica_wt_pct.get() != '':
				cursor.execute("update cathode set silica_wt_pct = %s where cathode_id = %s", (silica_wt_pct.get(), cathode_id.get()))

			if silica_mass.get() != '':
				cursor.execute("update cathode set silica_mass = %s where cathode_id = %s", (silica_mass.get(), cathode_id.get()))
			
			if LNTO_id.get() != '':
				cursor.execute("update cathode set LNTO_id = %s where cathode_id = %s", (LNTO_id.get(), cathode_id.get()))

			if code == 'mix':
				cursor.execute("update cathode set mix_time = %s where cathode_id = %s", (mix_time.get(), cathode_id.get()))
				cursor.execute("update cathode set mix_speed = %s where cathode_id = %s", (mix_speed.get(), cathode_id.get()))
				cursor.execute("update cathode set mix_rounds = %s where cathode_id = %s", (mix_rounds.get(), cathode_id.get()))
			elif code == 'mill':
				cursor.execute("update cathode set milling_time = %s where cathode_id = %s", (milling_time.get(), cathode_id.get()))
				cursor.execute("update cathode set milling_speed = %s where cathode_id = %s", (milling_speed.get(), cathode_id.get()))
				cursor.execute("update cathode set balls_small_mass = %s where cathode_id = %s", (balls_small_mass.get(), cathode_id.get()))
				cursor.execute("update cathode set balls_large_mass = %s where cathode_id = %s", (balls_large_mass.get(), cathode_id.get()))
					
			# Clear text boxes
			cathode_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_baseline_cathode(code):
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		if code == 'mix':
			name =  description.get() + ' Sp Mix'
		elif code == 'mill':
			name = description.get() + ' Milled'

		if LLZO_mass == 0:
			LLZO_id_var = None
		else:
			LLZO_id_var = LLZO_id.get()

		try: 
			cursor.execute("Insert into Cathode (cathode_id, cathode_type, date_made, particle_coating, casting_coating, active_material_vol, active_material_type, active_material_mass, packing_density, llzo_id, LLZO_mass, glass_id, Glass_mass, dispersant_type, dispersant_mass, polymer_type, polymer_mass, plasticizer_type, plasticizer_mass, solvent1_type, solvent1_mass, solvent2_type, solvent2_mass, composite_density, substrate_id, casting_temp, casting_bar_setting, casting_bar_type, estimated_thickness, num_rolling_layers, roller, rolling_procedure, bisque_heating_temp, bisque_heating_time, sinter1_date, sinter1_heating_temp, sinter1_heating_time, samples_per_batch, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(cathode_id.get(),
				name,
				date_made.get(),
				particle_coating.get(),
				casting_coating.get(),
				active_material_vol_percent.get(),
				active_material_type.get(),
				active_material_mass.get(),
				packing_density.get(),
				LLZO_id_var,
				LLZO_mass.get(),
				Glass_id.get(),
				Glass_mass.get(),
				dispersant_type.get(),
				dispersant_mass.get(),
				polymer_type.get(),
				polymer_mass.get(),
				plasticizer_type.get(),
				plasticizer_mass.get(),
				solvent1_type.get(),
				solvent1_mass.get(),
				solvent2_type.get(),
				solvent2_mass.get(),
				composite_density.get(),
				substrate_id.get(),
				casting_temp.get(),
				casting_bar_setting.get(),
				casting_bar_type.get(),
				estimate_cathode_thickness.get(),
				num_rolling_layers.get(),
				roller.get(),
				rolling_procedure.get(),
				bisque_heating_temp.get(),
				bisque_heating_time.get(),
				sinter1_date.get(),
				sinter1_heating_temp.get(),
				sinter1_heating_time.get(),
				samples.get(),
				comments.get(),
				initial.get()))

			if sinter2_date.get() != '':
				cursor.execute("update cathode set sinter2_date = %s where cathode_id = %s", (sinter2_date.get(), cathode_id.get()))

			if sinter2_heating_temp.get() != '':
				cursor.execute("update cathode set sinter2_heating_temp = %s where cathode_id = %s", (sinter2_heating_temp.get(), cathode_id.get()))

			if sinter2_heating_time.get() != '':
				cursor.execute("update cathode set sinter2_heating_time = %s where cathode_id = %s", (sinter2_heating_time.get(), cathode_id.get()))

			if code == 'mix':
				cursor.execute("update cathode set mix_time = %s where cathode_id = %s", (mix_time.get(), cathode_id.get()))
				cursor.execute("update cathode set mix_speed = %s where cathode_id = %s", (mix_speed.get(), cathode_id.get()))
				cursor.execute("update cathode set mix_rounds = %s where cathode_id = %s", (mix_rounds.get(), cathode_id.get()))
			elif code == 'mill':
				cursor.execute("update cathode set milling_time = %s where cathode_id = %s", (milling_time.get(), cathode_id.get()))
				cursor.execute("update cathode set milling_speed = %s where cathode_id = %s", (milling_speed.get(), cathode_id.get()))
				cursor.execute("update cathode set balls_small_mass = %s where cathode_id = %s", (balls_small_mass.get(), cathode_id.get()))
				cursor.execute("update cathode set balls_large_mass = %s where cathode_id = %s", (balls_large_mass.get(), cathode_id.get()))

			# Clear text boxes
			cathode_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_sample(code, new_sample_id):
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			if tab.get() == 1:
				tab_var = 1
				tab_mat = tab_material.get()
			else:
				tab_mat = None
				tab_var = 0
		except:
			tab_mat = None
			tab_var = 0

		try:
			if cover.get() == 1:
				cover_var = 1
				cover_mat = cover_material.get()
				cover_thick = cover_thickness.get()
			else:
				cover_mat = None
				cover_thick = None
				cover_var = 0
		except:
			cover_mat = None
			cover_thick = None
			cover_var = 0

		try:
			if sleeve.get() == 1:
				sleeve_var = 1
				sleeve_mat = sleeve_material.get()
			else:
				sleeve_mat = None
				sleeve_var = 0
		except:
			sleeve_mat = None
			sleeve_var = 0

		try:
			stage_temperature = stage_temp.get()
		except:
			stage_temperature = None

		try:
			gb5_exposure = gb5_exp.get()
		except:
			gb5_exposure = None

		try:
			if cw.get() == 1:
				cw_var = 1
				cw_mat = cw_material.get()
			else:
				cw_mat = None
				cw_var = 0
		except:
			cw_mat = None
			cw_var = 0

		try:
			roller_var = roller_speed.get()
		except:
			roller_var = None

		try:
			o2_var = o2.get()
		except:
			o2_var = None

		try:
			h2o_var = h2o.get()
		except:
			h2o_var = None

		try:
			roller_gap = roll_gap.get()
		except:
			roller_gap = None

		try:
			roller_temp = roll_temp.get()
		except:
			roller_temp = None

		try:
			if muffle_furnace.get() == 1:
				muffle_furnace_var = 1
				muffle_furnace_temp_var = muffle_furnace_temp.get()
				muffle_furnace_time_var = muffle_furnace_time.get()
			else:
				muffle_furnace_temp_var = None
				muffle_furnace_var = 0
				muffle_furnace_time_var = None
		except:
			muffle_furnace_temp_var = None
			muffle_furnace_var = 0
			muffle_furnace_time_var = None

		try:
			hot_plate_temperature = hot_plate_temp.get()
		except:
			hot_plate_temperature = None

		if cathode_coating.get() == 'None':
			cc = None
			cb = None
		else:
			cc = cathode_coating.get()
			cb = coating_batch.get()

		
		query = "Insert into samples (sample_id, sample_type, date_made, cathode_id, separator_id, cathode_coating, coating_batch, furnace_temp, furnace_time, stage_temp, gb5_exposure, o2, h2o, roller_speed, roller_gap, roller_temp, tab, tab_material, cover, cover_material, cover_thickness, sleeve, sleeve_material, cathode_weight, cathode_weight_material, hot_plate_temp, muffle_furnace, muffle_furnace_temp, muffle_furnace_time, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
	
		try:
			cursor.execute(query,
				(sample_id.get(),
				code,
				date_made.get(),
				cathode_id.get(),
				glass_id.get(),
				cc,
				cb,
				furnace_temp.get(),
				furnace_time.get(),
				stage_temperature,
				gb5_exposure,
				o2_var,
				h2o_var,
				roller_var,
				roller_gap,
				roller_temp,
				tab_var,
				tab_mat,
				cover_var,
				cover_mat,
				cover_thick,
				sleeve_var,
				sleeve_mat,
				cw_var,
				cw_mat,
				hot_plate_temperature,
				muffle_furnace_var,
				muffle_furnace_temp_var,
				muffle_furnace_time_var,
				comments.get(),
				initial.get()))

			# messagebox.showinfo('Success!', 'Data successfully added to DB')

			# update sample_id
			if int(new_sample_id[-2:]) < 9:
				new_sample_id = sample_id.get()[0:-2] + '0' + str(int(sample_id.get()[-2:]) +  1)
			else:
				new_sample_id = sample_id.get()[0:-2] + str(int(sample_id.get()[-2:]) +  1)

			# Clear text boxes
			sample_id.delete(0, END)
			sample_id.insert(0, new_sample_id)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()

	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_anode():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		if end.get():
			index_list = list(range(int(start.get()), int(end.get())+1))
		else:
			index_list = [int(start.get())]

		sample_list = [sample_id.get() + str(i) if i >= 10 else sample_id.get() + '0' + str(i) for i in index_list]

		for sample in sample_list:
			cursor.execute("Select active_material_vol, active_material_type, estimated_thickness from cells.cathode where cathode_id like (select cathode_id from cells.samples where sample_id like (%s));", sample)
			result = cursor.fetchone()
			active_vol = result["active_material_vol"]
			active = result["active_material_type"]
			estimate_cathode_thickness = result['estimated_thickness']

			# Specific capacity in Ah/cm2/um
				# assume packing density is 0.8 for SC, 0.7 for Agl (3-16-2023)
			if active.__contains__('622') & active.__contains__('SC'):
				spec_cap = 0.000086
				packing_density = 0.8
			elif active.__contains__('622') & active.__contains__('Agl'):
				spec_cap = 0.000078
				packing_density = 0.7
			elif active.__contains__('631') & active.__contains__('SC'):
				spec_cap = 0.000089
				packing_density = 0.8
			elif active.__contains__('811') & active.__contains__('Agl'):
				spec_cap = 0.000096
				packing_density = 0.7
			elif active.__contains__('811') & active.__contains__('LiNbO'):
				spec_cap = 0.000097
				packing_density = 0.8
			elif active.__contains__('955') & active.__contains__('SC'):
				spec_cap = 0.000099
				packing_density = 0.8
			elif active.__contains__('111') & active.__contains__('Agl'):
				spec_cap = 0.000079
				packing_density = 0.7
			else:
				spec_cap = 0
				packing_density = 0

			expected_capacity = spec_cap * float(active_area_size.get())*estimate_cathode_thickness*packing_density*float(active_vol)/100
			try:
				cursor.execute("Update samples set anode_type = %s, active_area_size = %s, anode_thickness = %s, expected_capacity = %s, comments = concat(comments, %s), initials = concat(initials, '-', %s) where sample_id like %s;",
					(anode_type.get(),
					active_area_size.get(),
					anode_thickness.get(),
					expected_capacity,
					comments.get(),
					initial.get(),
					sample))

			except:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
				# error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
				# if re.match("Duplicate entry", error) is not None:
				# 	messagebox.showerror('Duplicate Entry Error', error)
				# else:
				# 	messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Clear text boxes
		sample_id.delete(0, END)
		comments.delete(0, END)
		initial.delete(0, END)

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')	

def submit_ac():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		index_list = list(range(int(start.get()), int(end.get())+1))
		sample_list = [sample_id.get() + str(i) if i >= 10 else sample_id.get() + '0' + str(i) for i in index_list]

		for sample in sample_list:

			try:
				cursor.execute("Update samples set anode_coating_type = %s, anode_coating_batch = %s, coated_anode_directly = %s, comments = concat(comments, %s), initials = concat(initials, '-', %s) where sample_id like %s;",
					(material.get(),
					anode_coating_batch.get(),
					coated_anode.get(),
					comments.get(),
					initial.get(),
					sample))

			except:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Clear text boxes
		sample_id.delete(0, END)
		comments.delete(0, END)
		initial.delete(0, END)

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')	

def submit_eis():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		if conductivity.get() == '':
			try:
				cond = (float(thickness.get())*0.0001)/(float(impedance.get())*float(area.get()))
				
				cursor.execute("Insert into eis_testing values (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
					(sample_id.get(),
					date_tested.get(),
					impedance.get(),
					thickness.get(),
					area.get(),
					cond,
					contact.get(),
					comments.get(),
					initial.get()))

				# Clear text boxes
				sample_id.delete(0, END)
				comments.delete(0, END)
				initial.delete(0, END)

			except:
				error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc()))
				if re.match("Duplicate entry", error.group(1)) is not None:
					messagebox.showerror('Duplicate Entry Error', error.group(1))
				else:
					messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

			# Close connection
			conn.commit()
			conn.close()
			cursor.close()
		else:
			try:

				cursor.execute("Insert into eis_testing (sample_id, date_tested, i_conductivity, contact, comments, initialS) values (%s, %s, %s, %s, %s, %s);",
					(sample_id.get(),
					date_tested.get(),
					conductivity.get(),
					contact.get(),
					comments.get(),
					initial.get()))

				# Clear text boxes
				sample_id.delete(0, END)
				comments.delete(0, END)
				initial.delete(0, END)

			except:
				error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc()))
				if re.match("Duplicate entry", error.group(1)) is not None:
					messagebox.showerror('Duplicate Entry Error', error.group(1))
				else:
					messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

			# Close connection
			conn.commit()
			conn.close()
			cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_Econd():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		if conductivity.get() == '':
			try:
				cond = (float(thickness.get())*0.0001)/((float(voltage.get())/float(current.get()))*float(area.get()))
				
				cursor.execute("Insert into E_conductivity values (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
					(sample_id.get(),
					date_tested.get(),
					voltage.get(),
					current.get(),
					thickness.get(),
					area.get(),
					cond,
					comments.get(),
					initial.get()))

				# Clear text boxes
				sample_id.delete(0, END)
				comments.delete(0, END)
				initial.delete(0, END)

			except:
				error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc()))
				if re.match("Duplicate entry", error.group(1)) is not None:
					messagebox.showerror('Duplicate Entry Error', error.group(1))
				else:
					messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

			# Close connection
			conn.commit()
			conn.close()
			cursor.close()
		else:
			try:

				cursor.execute("Insert into E_conductivity (sample_id, date_tested, e_conductivity, comments, initialS) values (%s, %s, %s, %s, %s);",
					(sample_id.get(),
					date_tested.get(),
					conductivity.get(),
					comments.get(),
					initial.get()))

				# Clear text boxes
				sample_id.delete(0, END)
				comments.delete(0, END)
				initial.delete(0, END)

			except:
				error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc()))
				if re.match("Duplicate entry", error.group(1)) is not None:
					messagebox.showerror('Duplicate Entry Error', error.group(1))
				else:
					messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

			# Close connection
			conn.commit()
			conn.close()
			cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_galvo():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		cd = float(current.get())/float(area.get())

		try:
			cursor.execute("Insert into galvo_test values (%s, %s, %s, %s, %s, %s, %s, %s);",
				(sample_id.get(),
				date_tested.get(),
				current.get(),
				area.get(),
				cd,
				num_cycles.get(),
				initial.get(),
				comments.get()))

			# Clear text boxes
			sample_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')


def submit_b2s3():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			cursor.execute("Insert into b2s3 values (%s, %s, %s, %s, %s, %s, %s, %s);",
				(sample_id.get(),
				date_made.get(),
				B_type.get(),
				prep_method.get(),
				heating_profile.get(),
				time_profile.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			sample_id.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)


		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

# def submit_pary():
# 	if initial.get():
# 		# Connect to DB
# 		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
# 		cursor = conn.cursor() 

# 		try:
# 			cursor.execute("Insert into parylene values (%s, %s, %s, %s, %s, %s);",
# 				(sample_id.get(),
# 				date_added.get(),
# 				thickness.get(),
# 				base_pressure.get(),
# 				comments.get(),
# 				initial.get()))

# 			# Clear text boxes
# 			sample_id.delete(0, END)
# 			comments.delete(0, END)
# 			initial.delete(0, END)
# 		except:
# 			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
# 			if re.match("Duplicate entry", error) is not None:
# 				messagebox.showerror('Duplicate Entry Error', error)
# 			else:
# 				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

# 		# Close connection
# 		conn.commit()
# 		conn.close()
# 		cursor.close()
# 	else:
# 		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_cc():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor()

		index_list = list(range(int(start.get()), int(end.get())+1))
		sample_list = [sample_id.get() + str(i) if i >= 10 else sample_id.get() + '0' + str(i) for i in index_list]

		for sample in sample_list:
			try:
				cursor.execute("Insert into current_collector values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
					(sample,
					date_added.get(),
					anode_cc.get(),
					anode_lead.get(),
					anode_attach.get(),
					cathode_cc.get(),
					cathode_lead.get(),
					cathode_attach.get(),
					comments.get(),
					initial.get()))

			except:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		conn.commit()
		conn.close()
		cursor.close()

		# Clear text boxes
		sample_id.delete(0, END)
		comments.delete(0, END)
		initial.delete(0, END)
	
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def submit_postA():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		if cathode_thickness.get() == '':
			cathode_thick = None
			infiltration_percent = None
		else:
			cathode_thick = cathode_thickness.get()
			infiltration_percent = (float(infiltration_depth.get()) / float(cathode_thickness.get()))*100

		try:
			cursor.execute("Insert into post_analysis (sample_id, fail_reason, sep_thickness, cathode_thickness, infiltration_depth_max, inflitration_percent_max, glass_appearance, bubbles, rxn_ring, Li_corrosion, Li_plating, Handling_cracks, comments, initials) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				(sample_id.get(),
				reason.get(),
				sep_thickness.get(),
				cathode_thick,
				infiltration_depth.get(),
				infiltration_percent,
				appearance.get(),
				bubbles.get(),
				rxn_ring.get(),
				Li_corrosion.get(),
				Li_plating.get(),
				cracked.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			sample_id.delete(0, END)
			initial.delete(0, END)

		except:
			messagebox.showerror('Data Entry Error', str(traceback.format_exc()))
				
		# Close connection
		conn.commit()
		conn.close()
		cursor.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

# Click commands for loading data entry tables
def LLZO_Click():
	global llzo_id
	global date_made
	global date_rm
	global comments
	global initial

	llzo = Toplevel()
	llzo.title("Enter LLZO data here")
	# llzo.iconbitmap(r'JES_logo.ico')
	reg_date=llzo.register(callback_date)
	reg_int=llzo.register(callback_int)
	reg_float=llzo.register(callback_float)
	inv_date = llzo.register(invalid_date)
	inv_int = llzo.register(invalid_int)
	inv_float = llzo.register(invalid_float)

	# User input box
	llzo_id_label = Label(llzo, text = "LLZO ID").grid(row = 0, column =0)
	llzo_id = Entry(llzo, width = 30)
	llzo_id.grid(row = 1, column =0)
	llzo_id.insert(0, 'B23')

	date_made_label = Label(llzo, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =1)
	date_made = Entry(llzo)
	date_made.grid(row = 1, column =1)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	date_rm_label = Label(llzo, text = "Date RM").grid(row = 0, column =2)
	date_rm = Entry(llzo)
	date_rm.grid(row = 1, column =2)
	date_rm.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_rm.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	# final_mass_label = Label(llzo, text = "Final Mass (g)").grid(row = 0, column =3)
	# final_mass = Entry(llzo)
	# final_mass.grid(row = 1, column =3)
	# final_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(llzo, text = "Comments").grid(row = 0, column =4)
	comments = Entry(llzo)
	comments.grid(row = 1, column =4)

	initial_label = Label(llzo, text = "Enter Initials Here").grid(row= 2, column = 1)
	initial = Entry(llzo)
	initial.grid(row = 3, column =1)

	button_submit = Button(llzo, text = "Upload Data", command=submit_llzo).grid(row = 3, column = 3)	
	
def Li3BO3_Click():
	global li3bo3_id
	global date_made
	global i_o
	global comments
	global initial

	Li3BO3 = Toplevel()
	Li3BO3.title("Enter Li3BO3 data here")
	# Li3BO3.iconbitmap(r'JES_logo.ico')
	reg_date=Li3BO3.register(callback_date)
	reg_int=Li3BO3.register(callback_int)
	reg_float=Li3BO3.register(callback_float)
	inv_date = Li3BO3.register(invalid_date)
	inv_int = Li3BO3.register(invalid_int)
	inv_float = Li3BO3.register(invalid_float)

	# User input box

	li3bo3_id_label = Label(Li3BO3, text = "Li3BO3 ID").grid(row = 0, column =0)
	li3bo3_id = Entry(Li3BO3, width = 30)
	li3bo3_id.grid(row = 1, column =0)
	li3bo3_id.insert(0, 'B23')

	date_made_label = Label(Li3BO3, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(Li3BO3)
	date_made.grid(row = 1, column =1)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	i_o_label = Label(Li3BO3, text = "Inside or Outside (i or o)?").grid(row = 0, column =2)
	i_o = Entry(Li3BO3)
	i_o.grid(row = 1, column =2)

	# final_mass_label = Label(Li3BO3, text = "Final Mass (g)").grid(row = 0, column =3)
	# final_mass = Entry(Li3BO3)
	# final_mass.grid(row = 1, column =3)
	# final_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(Li3BO3, text = "Comments").grid(row = 0, column =4)
	comments = Entry(Li3BO3)
	comments.grid(row = 1, column =4)

	initial_label = Label(Li3BO3, text = "Enter Initials Here").grid(row= 2, column = 1)
	initial = Entry(Li3BO3)
	initial.grid(row = 3, column =1)

	button_submit = Button(Li3BO3, text = "Upload Data", command=submit_Li3BO3).grid(row = 3, column = 3)	

def LBCSO_Baseline_Glass_Click():
	global glass_id
	global date_made
	global li3bo3_id
	global li3bo3_wt_pct
	global li2co3_wt_pct
	global li2so4_wt_pct
	global li2b4o7_wt_pct
	global sio2_wt_pct
	global li2o2_wt_pct
	global libo2_wt_pct
	global b2o3_wt_pct
	global total_mass
	global furnace_temp
	global furnace_time
	global num_melts
	global date_rm
	global comments
	global initial

	glass = Toplevel()
	glass.title("Enter Glass Parameters Here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	
	# User input box
	glass_id_label = Label(glass, text = "LBCSO ID").grid(row = 0, column =0)
	glass_id = Entry(glass, width = 15)
	glass_id.grid(row = 1, column =0, padx =5)
	glass_id.insert(0, 'B23')

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx =5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	li3bo3_id_label = Label(glass, text = "Li3BO3 ID").grid(row = 0, column =3)
	li3bo3_id = Entry(glass, width = 15)
	li3bo3_id.grid(row = 1, column =3, padx =5)
	li3bo3_id.insert(0, 'B23')

	li3bo3_wt_pct_label = Label(glass, text = "Li3BO3 wt%").grid(row = 0, column =4)
	li3bo3_wt_pct = Entry(glass, width = 15)
	li3bo3_wt_pct.grid(row = 1, column =4, padx =5)
	li3bo3_wt_pct.insert(0, 0.1075)
	li3bo3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2co3 = IntVar()
	# li2co3.set(1)
	# li2co3_label = Label(glass, text = "Li2CO3?").grid(row = 0, column =5)
	# li2co3_cb = Checkbutton(glass, variable=li2co3, onvalue=1, offvalue=0)
	# li2co3_cb.grid(row = 1, column =5)

	li2co3_wt_pct_label = Label(glass, text = "Li2CO3 wt%").grid(row = 0, column =6)
	li2co3_wt_pct = Entry(glass, width = 15)
	li2co3_wt_pct.grid(row = 1, column =6, padx =5)
	li2co3_wt_pct.insert(0, 0.3011)
	li2co3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2so4 = IntVar()
	# li2so4.set(1)
	# li2so4_label = Label(glass, text = "Li2SO4?").grid(row = 0, column =7)
	# li2so4_cb = Checkbutton(glass, variable=li2so4, onvalue=1, offvalue=0)
	# li2so4_cb.grid(row = 1, column =7)

	li2so4_wt_pct_label = Label(glass, text = "Li2SO4 wt%").grid(row = 0, column =8)
	li2so4_wt_pct = Entry(glass, width = 15)
	li2so4_wt_pct.grid(row = 1, column =8, padx =5)
	li2so4_wt_pct.insert(0, 0.4301)
	li2so4_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2b4o7 = IntVar()
	# li2b4o7.set(1)
	# li2b4o7_label = Label(glass, text = "Li2B4O7?").grid(row = 0, column =7)
	# li2b4o7_cb = Checkbutton(glass, variable=li2b4o7, onvalue=1, offvalue=0)
	# li2b4o7_cb.grid(row = 1, column =7)

	li2b4o7_wt_pct_label = Label(glass, text = "Li2B4O7 wt%").grid(row = 0, column =9)
	li2b4o7_wt_pct = Entry(glass, width = 15)
	li2b4o7_wt_pct.grid(row = 1, column =9, padx =5)
	li2b4o7_wt_pct.insert(0, 0.1613)
	li2b4o7_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# sio2 = IntVar()
	# sio2.set(0)
	# sio2_label = Label(glass, text = "SiO2?").grid(row = 0, column =9)
	# sio2_cb = Checkbutton(glass, variable=sio2, onvalue=1, offvalue=0)
	# sio2_cb.grid(row = 1, column =9)

	sio2_wt_pct_label = Label(glass, text = "SiO2 wt%").grid(row = 0, column =10)
	sio2_wt_pct = Entry(glass, width = 15)
	sio2_wt_pct.grid(row = 1, column =10, padx =5)
	sio2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2o2 = IntVar()
	# li2o2.set(0)
	# li2o2_label = Label(glass, text = "Li2O2?").grid(row = 0, column =11)
	# li2o2_cb = Checkbutton(glass, variable=li2o2, onvalue=1, offvalue=0)
	# li2o2_cb.grid(row = 1, column =11)

	li2o2_wt_pct_label = Label(glass, text = "Li2O2 wt%").grid(row = 0, column =12)
	li2o2_wt_pct = Entry(glass, width = 15)
	li2o2_wt_pct.grid(row = 1, column =12, padx =5)
	li2o2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# libo2 = IntVar()
	# libo2.set(0)
	# libo2_label = Label(glass, text = "LiBO2?").grid(row = 0, column =13)
	# libo2_cb = Checkbutton(glass, variable=libo2, onvalue=1, offvalue=0)
	# libo2_cb.grid(row = 1, column =13)

	libo2_wt_pct_label = Label(glass, text = "LiBO2 wt%").grid(row = 0, column =14)
	libo2_wt_pct = Entry(glass, width = 15)
	libo2_wt_pct.grid(row = 1, column =14, padx =5)
	libo2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# b2o3 = IntVar()
	# b2o3.set(0)
	# b2o3_label = Label(glass, text = "B2O3?").grid(row = 0, column =15)
	# b2o3_cb = Checkbutton(glass, variable=b2o3, onvalue=1, offvalue=0)
	# b2o3_cb.grid(row = 1, column =15)

	b2o3_wt_pct_label = Label(glass, text = "B2O3 wt%").grid(row = 0, column =16)
	b2o3_wt_pct = Entry(glass, width = 15)
	b2o3_wt_pct.grid(row = 1, column =16, padx =5)
	b2o3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 2, column =0)
	total_mass = Entry(glass, width = 15)
	total_mass.grid(row = 3, column =0, padx =5)
	total_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 2, column =1)
	furnace_temp = Entry(glass, width = 15)
	furnace_temp.insert(0, 850)
	furnace_temp.grid(row = 3, column =1, padx =5)

	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 2, column =3)
	furnace_time = Entry(glass, width = 15)
	furnace_time.insert(0, '00:07:00')
	furnace_time.grid(row = 3, column =3, padx =5)

	date_rm_label = Label(glass, text = "Date RM (YYYY-MM-DD)").grid(row = 2, column =4)
	date_rm = Entry(glass, width = 15)
	date_rm.insert(0, '')
	date_rm.grid(row = 3, column =4, padx =5)

	num_melts_label = Label(glass, text = "# Melts").grid(row = 2, column =5)
	num_melts = Entry(glass, width = 15)
	num_melts.grid(row = 3, column =5, padx =5)

	comments_label = Label(glass, text = "Comments").grid(row = 2, column =6)
	comments = Entry(glass, width = 15)
	comments.grid(row = 3, column =6, padx =5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 1)
	initial = Entry(glass)
	initial.grid(row = 5, column =1)

	button_submit = Button(glass, text = "Upload Data", command=submit_lbcso_glass).grid(row = 5, column = 3)

def LBCSO_5050_Glass_Click():
	global glass_id
	global date_made
	global li3bo3_id
	global li3bo3_wt_pct
	global li2co3_wt_pct
	global li2so4_wt_pct
	global li2b4o7_wt_pct
	global sio2_wt_pct
	global li2o2_wt_pct
	global libo2_wt_pct
	global b2o3_wt_pct
	global total_mass
	global furnace_temp
	global furnace_time
	global date_rm
	global num_melts
	global comments
	global initial

	glass = Toplevel()
	glass.title("Enter Glass Parameters Here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	
	# User input box
	glass_id_label = Label(glass, text = "LBCSO ID").grid(row = 0, column =0)
	glass_id = Entry(glass, width = 15)
	glass_id.grid(row = 1, column =0, padx =5)
	glass_id.insert(0, 'B23')

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx =5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	li3bo3_id_label = Label(glass, text = "Li3BO3 ID").grid(row = 0, column =3)
	li3bo3_id = Entry(glass, width = 15)
	li3bo3_id.grid(row = 1, column =3, padx =5)
	li3bo3_id.insert(0, 'B23')

	li3bo3_wt_pct_label = Label(glass, text = "Li3BO3 wt%").grid(row = 0, column =4)
	li3bo3_wt_pct = Entry(glass, width = 15)
	li3bo3_wt_pct.grid(row = 1, column =4, padx =5)
	li3bo3_wt_pct.insert(0, 0.1075)
	li3bo3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2co3 = IntVar()
	# li2co3.set(1)
	# li2co3_label = Label(glass, text = "Li2CO3?").grid(row = 0, column =5)
	# li2co3_cb = Checkbutton(glass, variable=li2co3, onvalue=1, offvalue=0)
	# li2co3_cb.grid(row = 1, column =5)

	li2co3_wt_pct_label = Label(glass, text = "Li2CO3 wt%").grid(row = 0, column =6)
	li2co3_wt_pct = Entry(glass, width = 15)
	li2co3_wt_pct.grid(row = 1, column =6, padx =5)
	li2co3_wt_pct.insert(0, 0.3656)
	li2co3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2so4 = IntVar()
	# li2so4.set(1)
	# li2so4_label = Label(glass, text = "Li2SO4?").grid(row = 0, column =7)
	# li2so4_cb = Checkbutton(glass, variable=li2so4, onvalue=1, offvalue=0)
	# li2so4_cb.grid(row = 1, column =7)

	li2so4_wt_pct_label = Label(glass, text = "Li2SO4 wt%").grid(row = 0, column =8)
	li2so4_wt_pct = Entry(glass, width = 15)
	li2so4_wt_pct.grid(row = 1, column =8, padx =5)
	li2so4_wt_pct.insert(0, 0.3656)
	li2so4_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2b4o7 = IntVar()
	# li2b4o7.set(1)
	# li2b4o7_label = Label(glass, text = "Li2B4O7?").grid(row = 0, column =7)
	# li2b4o7_cb = Checkbutton(glass, variable=li2b4o7, onvalue=1, offvalue=0)
	# li2b4o7_cb.grid(row = 1, column =7)

	li2b4o7_wt_pct_label = Label(glass, text = "Li2B4O7 wt%").grid(row = 0, column =9)
	li2b4o7_wt_pct = Entry(glass, width = 15)
	li2b4o7_wt_pct.grid(row = 1, column =9, padx =5)
	li2b4o7_wt_pct.insert(0, 0.1613)
	li2b4o7_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# sio2 = IntVar()
	# sio2.set(0)
	# sio2_label = Label(glass, text = "SiO2?").grid(row = 0, column =9)
	# sio2_cb = Checkbutton(glass, variable=sio2, onvalue=1, offvalue=0)
	# sio2_cb.grid(row = 1, column =9)

	sio2_wt_pct_label = Label(glass, text = "SiO2 wt%").grid(row = 0, column =10)
	sio2_wt_pct = Entry(glass, width = 15)
	sio2_wt_pct.grid(row = 1, column =10, padx =5)
	sio2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# li2o2 = IntVar()
	# li2o2.set(0)
	# li2o2_label = Label(glass, text = "Li2O2?").grid(row = 0, column =11)
	# li2o2_cb = Checkbutton(glass, variable=li2o2, onvalue=1, offvalue=0)
	# li2o2_cb.grid(row = 1, column =11)

	li2o2_wt_pct_label = Label(glass, text = "Li2O2 wt%").grid(row = 0, column =12)
	li2o2_wt_pct = Entry(glass, width = 15)
	li2o2_wt_pct.grid(row = 1, column =12, padx =5)
	li2o2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# libo2 = IntVar()
	# libo2.set(0)
	# libo2_label = Label(glass, text = "libo2?").grid(row = 0, column =13)
	# libo2_cb = Checkbutton(glass, variable=libo2, onvalue=1, offvalue=0)
	# libo2_cb.grid(row = 1, column =13)

	libo2_wt_pct_label = Label(glass, text = "LiBO2 wt%").grid(row = 0, column =14)
	libo2_wt_pct = Entry(glass, width = 15)
	libo2_wt_pct.grid(row = 1, column =14, padx =5)
	libo2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# b2o3 = IntVar()
	# b2o3.set(0)
	# b2o3_label = Label(glass, text = "B2O3?").grid(row = 0, column =15)
	# b2o3_cb = Checkbutton(glass, variable=b2o3, onvalue=1, offvalue=0)
	# b2o3_cb.grid(row = 1, column =15)

	b2o3_wt_pct_label = Label(glass, text = "B2O3 wt%").grid(row = 0, column =16)
	b2o3_wt_pct = Entry(glass, width = 15)
	b2o3_wt_pct.grid(row = 1, column =16, padx =5)
	b2o3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 2, column =0)
	total_mass = Entry(glass, width = 15)
	total_mass.grid(row = 3, column =0, padx =5)
	total_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 2, column =1)
	furnace_temp = Entry(glass, width = 15)
	furnace_temp.insert(0, 750)
	furnace_temp.grid(row = 3, column =1, padx =5)

	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 2, column =3)
	furnace_time = Entry(glass, width = 15)
	furnace_time.insert(0, '00:10:00')
	furnace_time.grid(row = 3, column =3, padx =5)

	date_rm_label = Label(glass, text = "Date RM (YYYY-MM-DD)").grid(row = 2, column =4)
	date_rm = Entry(glass, width = 15)
	date_rm.insert(0, '')
	date_rm.grid(row = 3, column =4, padx =5)

	num_melts_label = Label(glass, text = "# Melts").grid(row = 2, column =5)
	num_melts = Entry(glass, width = 15)
	num_melts.grid(row = 3, column =5, padx =5)

	comments_label = Label(glass, text = "Comments").grid(row = 2, column =6)
	comments = Entry(glass, width = 15)
	comments.grid(row = 3, column =6, padx =5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 1)
	initial = Entry(glass)
	initial.grid(row = 5, column =1)

	button_submit = Button(glass, text = "Upload Data", command=submit_lbcso_glass).grid(row = 5, column = 3)

# def LIBOSS_Click(pct):
# 	global glass_id
# 	global date_made
# 	global preparation
# 	global li2s_wt_pct
# 	global b2s3_wt_pct
# 	global b2s3_id
# 	global b_wt_pct
# 	global s_wt_pct
# 	global lii_wt_pct
# 	global sio2_wt_pct
# 	global sio2_type
# 	global mat
# 	global mat_wt_pct
# 	global total_mass
# 	global furnace_temp
# 	global furnace_time
# 	global comments
# 	global initial

# 	glass = Toplevel()
# 	glass.title("Enter " + str(pct) + "% LIBOSS Parameters Here")
# 	# glass.iconbitmap(r'JES_logo.ico')
# 	reg_date=glass.register(callback_date)
# 	reg_int=glass.register(callback_int)
# 	reg_float=glass.register(callback_float)
# 	inv_date = glass.register(invalid_date)
# 	inv_int = glass.register(invalid_int)
# 	inv_float = glass.register(invalid_float)

# 	if pct ==13:
# 		li2s_auto = 25.625
# 		b2s3_auto = 0
# 		lii_auto = 15.625
# 		sio2_auto = 0
# 		li2b4o7_auto = 33.75
# 		sis2_auto = 25.0
# 	elif pct ==16:
# 		li2s_auto = 1
# 		b2s3_auto = 1
# 		lii_auto = 1
# 		sio2_auto = 1
# 	elif pct ==30:
# 		li2s_auto = 1
# 		b2s3_auto = 1
# 		lii_auto = 1
# 		sio2_auto = 1
# 	elif pct ==34:
# 		li2s_auto = 15.4
# 		b2s3_auto = 33.0
# 		lii_auto = 34.8
# 		sio2_auto =16.8
# 	elif pct ==37:
# 		li2s_auto = 1
# 		b2s3_auto = 1
# 		lii_auto = 1
# 		sio2_auto =1
# 	elif pct ==54:
# 		li2s_auto = 1
# 		b2s3_auto = 1
# 		lii_auto = 1
# 		sio2_auto =1
# 	else:
# 		li2s_auto = 0
# 		b2s3_auto = 0
# 		lii_auto = 0
# 		sio2_auto = 0

	
# 	# User input box
# 	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =0)
# 	glass_id = Entry(glass, width = 15)
# 	glass_id.grid(row = 1, column =0, padx =5)
# 	glass_id.insert(0, 'B23')

# 	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
# 	date_made = Entry(glass, width = 15)
# 	date_made.grid(row = 1, column =1, padx =5)
# 	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
# 	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

# 	preparation_options = ['Select', 'Ampule', 'GC Crucible in Ampule', 'Carbonized Ampule']

# 	preparation_label = Label(glass, text = "Preparation Method").grid(row = 0, column =2)
# 	preparation = ttk.Combobox(glass, value = preparation_options)
# 	preparation.current(0)
# 	preparation.grid(row = 1, column =2, padx = 5)

# 	li2s_wt_pct_label = Label(glass, text = "Li2S wt%").grid(row = 0, column =3)
# 	li2s_wt_pct = Entry(glass, width = 15)
# 	li2s_wt_pct.grid(row = 1, column =3, padx =5)
# 	li2s_wt_pct.insert(0, li2s_auto)
# 	li2s_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	b2s3_wt_pct_label = Label(glass, text = "B2S3 wt%").grid(row = 0, column =4)
# 	b2s3_wt_pct = Entry(glass, width = 15)
# 	b2s3_wt_pct.grid(row = 1, column =4, padx =5)
# 	b2s3_wt_pct.insert(0, b2s3_auto)
# 	b2s3_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	b2s3_id_label = Label(glass, text = "B2S3_id").grid(row = 0, column =5)
# 	b2s3_id = Entry(glass, width = 15)
# 	b2s3_id.grid(row = 1, column =5, padx =5)
# 	b2s3_id.insert(0, b2s3_auto)
# 	b2s3_id.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	b_wt_pct_label = Label(glass, text = "B wt%").grid(row = 0, column =6)
# 	b_wt_pct = Entry(glass, width = 15)
# 	b_wt_pct.grid(row = 1, column =6, padx =5)
# 	b_wt_pct.insert(0, 0)
# 	b_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	s_wt_pct_label = Label(glass, text = "S wt%").grid(row = 0, column =7)
# 	s_wt_pct = Entry(glass, width = 15)
# 	s_wt_pct.grid(row = 1, column =7, padx =5)
# 	s_wt_pct.insert(0, 0)
# 	s_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	lii_wt_pct_label = Label(glass, text = "LiI wt%").grid(row = 0, column =8)
# 	lii_wt_pct = Entry(glass, width = 15)
# 	lii_wt_pct.grid(row = 1, column =8, padx =5)
# 	lii_wt_pct.insert(0, lii_auto)
# 	lii_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	sio2_wt_pct_label = Label(glass, text = "SiO2 wt%").grid(row = 0, column =9)
# 	sio2_wt_pct = Entry(glass, width = 15)
# 	sio2_wt_pct.grid(row = 1, column =9, padx =5)
# 	sio2_wt_pct.insert(0, sio2_auto)
# 	sio2_wt_pct.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	sio2_type_label = Label(glass, text = "SiO2 Type").grid(row = 2, column =0)
# 	sio2_type = Entry(glass, width = 15)
# 	sio2_type.grid(row = 3, column =0, padx =5)
# 	sio2_type.insert(0, 'Fume Silica')

# 	mat_options = ['None', 'Li2B4O7', 'Li3BO3', 'LiBO2', 'SiS2']

# 	mat1_label = Label(glass, text = "Select an Additive:").grid(row = 2, column =1)
# 	mat1 = ttk.Combobox(glass, value = mat_options)
# 	mat1.current(1)
# 	mat1.grid(row = 3, column =1, padx = 5)

# 	mat1_wt_pct_label = Label(glass, text = "Additive wt%").grid(row = 2, column =2)
# 	mat1_wt_pct = Entry(glass, width = 15)
# 	mat1_wt_pct.insert(0, li2b4o7_auto)
# 	mat1_wt_pct.grid(row = 3, column =2, padx =5)

# 	mat2_options = ['None', 'Li2B4O7', 'Li3BO3', 'LiBO2', 'SiS2']
# 	mat2_label = Label(glass, text = "Select an Additive:").grid(row = 2, column =3)
# 	mat2 = ttk.Combobox(glass, value = mat_options)
# 	mat2.current(4)
# 	mat2.grid(row = 3, column =3, padx = 5)

# 	mat2_wt_pct_label = Label(glass, text = "Additive wt%").grid(row = 2, column =4)
# 	mat2_wt_pct = Entry(glass, width = 15)
# 	mat2_wt_pct.grid(row = 3, column =4, padx =5)

# 	total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 2, column =5)
# 	total_mass = Entry(glass, width = 15)
# 	total_mass.grid(row = 3, column =5, padx =5)
# 	total_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 2, column =6)
# 	furnace_temp = Entry(glass, width = 15)
# 	furnace_temp.insert(0, 840)
# 	furnace_temp.grid(row = 3, column =6, padx =5)

# 	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 2, column =7)
# 	furnace_time = Entry(glass, width = 15)
# 	furnace_time.insert(0, '00:10:00')
# 	furnace_time.grid(row = 3, column =7, padx =5)

# 	comments_label = Label(glass, text = "Comments").grid(row = 2, column =8)
# 	comments = Entry(glass, width = 15)
# 	comments.grid(row = 3, column =8, padx =5)

# 	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 1)
# 	initial = Entry(glass)
# 	initial.grid(row = 5, column =1)

# 	button_submit = Button(glass, text = "Upload Data", command=lambda: submit_LIBOSS_glass(pct)).grid(row = 5, column = 4)

def ISU_Glass_Click():
	global glass_id
	global date_made
	global comments
	global initial

	glass = Toplevel()
	glass.title("Enter Glass Parameters Here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	
	# User input box
	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =0)
	glass_id = Entry(glass, width = 15)
	glass_id.grid(row = 1, column =0, padx =5)
	glass_id.insert(0, 'JES6-')

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx =5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	comments_label = Label(glass, text = "Comments").grid(row = 0, column =2)
	comments = Entry(glass, width = 15)
	comments.grid(row = 1, column =2, padx =5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 1)
	initial = Entry(glass)
	initial.grid(row = 5, column =1)

	button_submit = Button(glass, text = "Upload Data", command=submit_ISU_glass).grid(row = 5, column = 2)

# def LIBOSS_Add_Click():
# 	global glass_id
# 	global date_made
# 	global liboss_base
# 	global material
# 	global mass_liboss
# 	global ratio_1
# 	global ratio_2
# 	global initial
# 	global comments

# 	liboss_add = Toplevel()
# 	liboss_add.title("LIBOSS Batch Type")

# 	reg_date=liboss_add.register(callback_date)
# 	reg_int=liboss_add.register(callback_int)
# 	reg_float=liboss_add.register(callback_float)
# 	inv_date = liboss_add.register(invalid_date)
# 	inv_int = liboss_add.register(invalid_int)
# 	inv_float = liboss_add.register(invalid_float)

# 	# User input box
# 	glass_id_label = Label(liboss_add, text = "Glass ID").grid(row = 0, column =0)
# 	glass_id = Entry(liboss_add, width = 15)
# 	glass_id.grid(row = 1, column =0, padx =5)
# 	glass_id.insert(0, 'B23')

# 	date_made_label = Label(liboss_add, text = "Date Made").grid(row = 0, column =1)
# 	date_made = Entry(liboss_add, width = 15)
# 	date_made.grid(row = 1, column =1, padx =5)
# 	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
# 	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

# 	liboss_base_label = Label(liboss_add, text = "LIBOSS Base ID").grid(row = 0, column =2)
# 	liboss_base = Entry(liboss_add, width = 15)
# 	liboss_base.grid(row = 1, column =2, padx =5)
# 	liboss_base.insert(0, 'B23')

# 	material_options = materials_list
	
# 	material_label = Label(liboss_add, text = "Select a Material:").grid(row = 0, column =3)
# 	material = ttk.Combobox(liboss_add, value = material_options)
# 	material.current(0)
# 	material.grid(row = 1, column =3, padx = 5)

# 	mass_liboss_label = Label(liboss_add, text = "LIBOSS Mass (g)").grid(row = 0, column =4)
# 	mass_liboss = Entry(liboss_add, width = 15)
# 	mass_liboss.grid(row = 1, column =4, padx =5)

# 	ratio_1_label = Label(liboss_add, text = "Ratio of LIBOSS").grid(row = 0, column =5)
# 	ratio_1 = Entry(liboss_add, width = 5)
# 	ratio_1.grid(row = 1, column =5, padx =5)

# 	colon = Label(liboss_add, text = ":").grid(row = 1, column = 6)

# 	ratio_2_label = Label(liboss_add, text = "Ratio of Additive").grid(row = 0, column =7)
# 	ratio_2 = Entry(liboss_add, width = 5)
# 	ratio_2.grid(row = 1, column =7, padx =5)

# 	comments_label = Label(liboss_add, text = "Comments").grid(row = 0, column =8)
# 	comments = Entry(liboss_add, width = 15)
# 	comments.grid(row = 1, column =8, padx =5)

# 	initial_label = Label(liboss_add, text = "Enter Initials Here").grid(row= 4, column = 1)
# 	initial = Entry(liboss_add)
# 	initial.grid(row = 5, column =1)

# 	button_submit = Button(liboss_add, text = "Upload Data", command=submit_LIBOSS_add).grid(row = 5, column = 2)

def LIBOSS_Click(code):
	global glass_id
	global date_made
	global preparation
	global mat1
	global mat1_mass
	global mat2
	global mat2_mass
	global li2s_mass
	global mat3
	global mat3_mass
	global mat4
	global mat4_mass
	global mat5
	global mat5_mass
	global mat6
	global mat6_mass
	global mat7
	global mat7_mass
	global mat8
	global mat8_mass
	global mat9
	global mat9_mass
	global mass_factor
	global total_mass
	global furnace_temp
	global furnace_time
	global recovery
	global b2s3_id
	global num_melts
	global comments
	global initial
	global name

	glass = Toplevel()
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)

	# User input box
	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =0)
	glass_id = Entry(glass, width = 15)
	glass_id.grid(row = 2, column =0, padx =5)
	glass_id.insert(0, 'B23')

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 2, column =1, padx =5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))


	if code in ['JESBOS1', 'JESBOS2']:
		glass.title("Enter JESBOS Parameters Here")

		if code == 'JESBOS1':
			mat_mass = [6.99, 1.77, 4.5, 1.35, 14.61]
		elif code == 'JESBOS2':
			mat_mass = [6, 6, 3.6, 1.8, 17.4]

		preparation = 'Crucible'

		mat1 = 'LiBO2'
		mat1_mass = mat_mass[0]

		mat2 = 'LiI'
		mat2_mass = mat_mass[1]

		mat3 = 'SiS2'
		mat3_mass = mat_mass[2]

		mat4 = 'Li2S'
		mat4_mass = mat_mass[3]

		total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 0, column =3)
		total_mass_label = Label(glass, text = str(mat_mass[-1]) + "  x").grid(row = 2, column =3)

		mass_factor_label = Label(glass, text = "Batch Size", width = 15).grid(row = 0, column =4)
		mass_factor = Entry(glass, width = 5)
		mass_factor.insert(0, 1)
		mass_factor.grid(row = 2, column =4, padx = 5)

		total_mass = mat_mass[-1]

		mat5 = 'None'
		mat6 = 'None'
		mat7 = 'None'
		mat8 = 'None'
		mat9 = 'None'

		mat5_mass = ''
		mat6_mass = ''
		mat7_mass = ''
		mat8_mass = ''
		mat9_mass = ''

		furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 0, column =5)
		furnace_temp = Entry(glass, width = 15)
		furnace_temp.insert(0, 850)
		furnace_temp.grid(row =2, column =5, padx =5)

		furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 0, column =6)
		furnace_time = Entry(glass, width = 15)
		furnace_time.insert(0, '00:15:00')
		furnace_time.grid(row = 2, column =6, padx =5)

		recovery_label = Label(glass, text = "Recovered Mass (g)").grid(row = 0, column =7)
		recovery = Entry(glass, width = 15)
		recovery.grid(row = 2, column =7, padx =5)

		b2s3_id_label = Label(glass, text = "B2S3_id").grid(row = 0, column =8)
		b2s3_id = Entry(glass, width = 15)
		b2s3_id.grid(row = 2, column =8, padx =5)
		b2s3_id.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		sis2_id_label = Label(glass, text = "SiS2_id").grid(row = 0, column =9)
		sis2_id = Entry(glass, width = 15)
		sis2_id.grid(row = 2, column =9, padx =5)
		sis2_id.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		num_melts_label = Label(glass, text = "# Melts").grid(row = 0, column =10)
		num_melts = Entry(glass, width = 15)
		num_melts.grid(row = 2, column =10, padx =5)

		comments_label = Label(glass, text = "Comments").grid(row = 0, column =11, columnspan = 2)
		comments = Entry(glass, width = 30)
		comments.grid(row = 2, column =11, columnspan = 2, padx =5)

	elif code in ['JES5', 'JES5.16', 'JES5.16b', 'JES5.16c', 'JES5.16d']:
		glass.title("Enter JES5.16 Parameters Here")

		preparation = 'Crucible'

		if code == 'JES5.16':
			mat_mass = [0.08, 1.56, 2.32, 2.32, 0.72, 0.24, 7.24]
		elif code == 'JES5.16b':
			mat_mass = [0.4, 0, 3.48, 3.48, 1.08, 1.2, 9.64]
		elif code == 'JES5.16c':
			mat_mass = [0.06, 1.17, 1.74, 1.74, 1.08, 0.18, 5.97]
		elif code == 'JES5.16d':
			mat_mass = [0.05, 0.975, 1.45, 1.45, 1.35, 0.15, 5.43]
		elif code == 'JES5':
			mat_mass = [0, 0, 4.35, 4.35, 1.35, 0, 10.05]

		mat1 = 'LiCl'
		mat1_mass = mat_mass[0]

		mat2 = 'LiI'
		mat2_mass = mat_mass[1]

		mat3 = 'SiS2'
		mat3_mass = mat_mass[2]

		mat4 = 'Li2S'
		mat4_mass = mat_mass[3]

		mat5 = 'LiPO3'
		mat5_mass = mat_mass[4]

		mat6 = 'LiBr'
		mat6_mass = mat_mass[5]

		total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 0, column =3)
		total_mass_label = Label(glass, text = str(mat_mass[-1]) + "  x").grid(row = 2, column =3)

		mass_factor_label = Label(glass, text = "Batch Size", width = 15).grid(row = 0, column =4)
		mass_factor = Entry(glass, width = 5)
		mass_factor.insert(0, 1)
		mass_factor.grid(row = 2, column =4, padx = 5)

		total_mass = mat_mass[-1]

		mat7 = 'None'
		mat8 = 'None'
		mat9 = 'None'

		mat7_mass = ''
		mat8_mass = ''
		mat9_mass = ''

		furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 0, column =5)
		furnace_temp = Entry(glass, width = 15)
		furnace_temp.insert(0, 850)
		furnace_temp.grid(row =2, column =5, padx =5)

		furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 0, column =6)
		furnace_time = Entry(glass, width = 15)
		furnace_time.insert(0, '00:10:00')
		furnace_time.grid(row = 2, column =6, padx =5)

		recovery_label = Label(glass, text = "Recovered Mass (g)").grid(row = 0, column =7)
		recovery = Entry(glass, width = 15)
		recovery.grid(row = 2, column =7, padx =5)

		b2s3_id_label = Label(glass, text = "B2S3_id").grid(row = 0, column =8)
		b2s3_id = Entry(glass, width = 15)
		b2s3_id.grid(row = 2, column =8, padx =5)
		b2s3_id.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		sis2_id_label = Label(glass, text = "SiS2_id").grid(row = 0, column =9)
		sis2_id = Entry(glass, width = 15)
		sis2_id.grid(row = 2, column =9, padx =5)
		sis2_id.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		num_melts_label = Label(glass, text = "# Melts").grid(row = 0, column =10)
		num_melts = Entry(glass, width = 15)
		num_melts.grid(row = 2, column =10, padx =5)

		comments_label = Label(glass, text = "Comments").grid(row = 0, column =11, columnspan = 2)
		comments = Entry(glass, width = 30)
		comments.grid(row = 2, column =11, columnspan = 2, padx =5)

	elif code == 'Exp':
		glass.title("Enter Glass Parameters Here")

		preparation_options = ['Select', 'Ampule', 'Crucible']

		preparation_label = Label(glass, text = "Preparation Method").grid(row = 0, column =2)
		preparation = ttk.Combobox(glass, value = preparation_options, width = 15)
		preparation.current(0)
		preparation.grid(row = 2, column =2, padx = 5)

		mat_options = materials_list[:]
		mat_options.append('None')

		mat1_label = Label(glass, text = "Material 1:").grid(row = 0, column =3)
		mat1 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat1.current(39)
		mat1.grid(row = 1, column =3, padx = 5)

		mat1_mass = Entry(glass, width = 15)
		mat1_mass.grid(row = 2, column =3, padx =5)

		mat2_label = Label(glass, text = "Material 2:").grid(row = 0, column =4)
		mat2 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat2.current(39)
		mat2.grid(row = 1, column =4, padx = 5)

		# mat2_mass_label = Label(glass, text = "Material 2 Mass (g)").grid(row = 2, column =3)
		mat2_mass = Entry(glass, width = 15)
		mat2_mass.grid(row = 2, column =4, padx =5)

		mat3_label = Label(glass, text = "Material 3:").grid(row = 0, column =5)
		mat3 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat3.current(39)
		mat3.grid(row = 1, column =5, padx = 5)

		# mat3_mass_label = Label(glass, text = "Material 3 Mass (g)").grid(row = 0, column =5)
		mat3_mass = Entry(glass, width = 15)
		mat3_mass.grid(row = 2, column =5, padx =5)

		mat4_label = Label(glass, text = "Material 4:").grid(row = 0, column =6)
		mat4 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat4.current(39)
		mat4.grid(row = 1, column =6, padx = 5)

		# mat4_mass_label = Label(glass, text = "Material 4 Mass (g)").grid(row = 2, column =6)
		mat4_mass = Entry(glass, width = 15)
		mat4_mass.grid(row = 2, column =6, padx =5)

		mat5_label = Label(glass, text =  "Material 5:").grid(row = 0, column =7)
		mat5 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat5.current(39)
		mat5.grid(row = 1, column =7, padx = 5)

		# mat5_mass_label = Label(glass, text = "Material 5 Mass (g)").grid(row = 2, column =7)
		mat5_mass = Entry(glass, width = 15)
		mat5_mass.grid(row = 2, column =7, padx =5)

		mat6_label = Label(glass, text = "Material 6:").grid(row = 0, column =8)
		mat6 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat6.current(39)
		mat6.grid(row = 1, column =8, padx = 5)

		# mat6_mass_label = Label(glass, text = "Material 6 Mass (g)").grid(row = 0, column =8)
		mat6_mass = Entry(glass, width = 15)
		mat6_mass.grid(row = 2, column =8, padx =5)

		mat7_label = Label(glass, text = "Material 7:").grid(row = 0, column =9)
		mat7 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat7.current(39)
		mat7.grid(row = 1, column =9, padx = 5)

		# mat7_mass_label = Label(glass, text = "Material 7 Mass (g)").grid(row = 2, column =9)
		mat7_mass = Entry(glass, width = 15)
		mat7_mass.grid(row = 2, column =9, padx =5)

		mat8_label = Label(glass, text = "Material 8:").grid(row = 0, column =10)
		mat8 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat8.current(39)
		mat8.grid(row = 1, column =10, padx = 5)

		# mat8_mass_label = Label(glass, text = "Material 8 Mass (g)").grid(row = 2, column =10)
		mat8_mass = Entry(glass, width = 15)
		mat8_mass.grid(row = 2, column =10, padx= 5)

		mat9_label = Label(glass, text = "Material 9:").grid(row = 0, column =11)
		mat9 = ttk.Combobox(glass, value = mat_options, width = 15)
		mat9.current(39)
		mat9.grid(row = 1, column =11, padx = 5)

		# mat9_mass_label = Label(glass, text = "Material 9 Mass (g)").grid(row = 0, column =11)
		mat9_mass = Entry(glass, width = 15)
		mat9_mass.grid(row = 2, column =11, padx =5)

		total_mass_label = Label(glass, text = "Total Mass (g)").grid(row = 3, column =0)
		total_mass = Entry(glass, width = 15)
		total_mass.grid(row = 4, column =0, padx =5)
		total_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		mass_factor = 1

		furnace_temp_label = Label(glass, text = "Furnace Temp °C").grid(row = 3, column =1)
		furnace_temp = Entry(glass, width = 15)
		furnace_temp.insert(0, 850)
		furnace_temp.grid(row =4, column =1, padx =5)

		furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 3, column =2)
		furnace_time = Entry(glass, width = 15)
		furnace_time.insert(0, '00:10:00')
		furnace_time.grid(row = 4, column =2, padx =5)

		recovery_label = Label(glass, text = "Recovered Mass (g)").grid(row = 3, column =3)
		recovery = Entry(glass, width = 15)
		recovery.grid(row = 4, column =3, padx =5)

		name_label = Label(glass, text = "Exp Glass Name").grid(row = 3, column =4)
		name = Entry(glass, width = 15)
		name.grid(row = 4, column =4, padx =5)

		# b2s3_id_label = Label(glass, text = "B2S3_id").grid(row = 3, column =4)
		# b2s3_id = Entry(glass, width = 15)
		# b2s3_id.grid(row = 4, column =4, padx =5)

		# sis2_id_label = Label(glass, text = "SiS2_id").grid(row = 3, column =5)
		# sis2_id = Entry(glass, width = 15)
		# sis2_id.grid(row = 4, column =5, padx =5)

		num_melts_label = Label(glass, text = "# Melts").grid(row = 3, column =6)
		num_melts = Entry(glass, width = 15)
		num_melts.grid(row = 4, column =6, padx =5)

		comments_label = Label(glass, text = "Comments").grid(row = 3, column =7, columnspan = 2)
		comments = Entry(glass, width = 30)
		comments.grid(row = 4, column =7, columnspan = 2, padx =5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 5, column = 1)
	initial = Entry(glass)
	initial.grid(row = 6, column =1)

	button_submit = Button(glass, text = "Upload Data", command=lambda:submit_LIBOSS_glass(code)).grid(row = 6, column = 3)

# def LIBOSS_Glass_Click():
# 	liboss = Toplevel()
# 	liboss.title("LIBOSS Batch Type")
# 	liboss.geometry("450x200")

# 	liboss_label = Label(liboss, text = "Select LIBOSS Batch Type Here:", font = 'bold').place(relx=0.5, rely=0.3, anchor=CENTER)
# 	pct_13 = Button(liboss, text = "13%", command= lambda: LIBOSS_Click(13), width = 12).place(relx = 0.25, rely = 0.5, anchor= CENTER)
# 	pct_16 = Button(liboss, text = "16%", command= lambda: LIBOSS_Click(16), width = 12).place(relx = 0.5, rely = 0.5, anchor= CENTER)
# 	pct_30 = Button(liboss, text = "30%", command= lambda: LIBOSS_Click(30), width = 12).place(relx = 0.75, rely = 0.5, anchor= CENTER)
# 	pct_34 = Button(liboss, text = "34%", command= lambda: LIBOSS_Click(34), width = 12).place(relx = 0.25, rely = 0.65, anchor= CENTER)
# 	pct_37 = Button(liboss, text = "37%", command= lambda: LIBOSS_Click(37), width = 12).place(relx = 0.5, rely = 0.65, anchor= CENTER)
# 	pct_54 = Button(liboss, text = "54%", command= lambda: LIBOSS_Click(54), width = 12).place(relx = 0.75, rely = 0.65, anchor= CENTER)
# 	experiment = Button(liboss, text = "Experiments", command= LIBOSS_Experiment_Click, width = 12).place(relx = 0.5, rely = 0.8, anchor= CENTER)

def Glass_Click():
	glass = Toplevel()
	glass.title("Glass Batch Type")
	glass.geometry("500x250")

	glass_label = Label(glass, text = "Select Glass Batch Type Here:", font = 'bold').place(relx=0.3, rely=0.2, anchor=CENTER)
	lbcso_baseline = Button(glass, text = "LBCSO Baseline", command= LBCSO_Baseline_Glass_Click, width = 12).place(relx = 0.35, rely = 0.35, anchor= CENTER)
	lbcso_50_50 = Button(glass, text = "LBCSO 50/50", command= LBCSO_5050_Glass_Click, width = 12).place(relx = 0.35, rely = 0.5, anchor= CENTER)
	JESBOS1 = Button(glass, text = "JESBOS1", command=lambda:LIBOSS_Click('JESBOS1'), width = 12).place(relx = 0.55, rely = 0.35, anchor= CENTER)
	JESBOS2 = Button(glass, text = "JESBOS2", command=lambda:LIBOSS_Click('JESBOS2'), width = 12).place(relx = 0.55, rely = 0.5, anchor= CENTER)
	Exp_LIBOSS = Button(glass, text = "Experimental", command=lambda:LIBOSS_Click('Exp'), width = 12).place(relx = 0.15, rely = 0.35, anchor= CENTER)
	OG_ISU = 	Button(glass, text = " Shipped ISU", command=ISU_Glass_Click, width = 12).place(relx = 0.15, rely = 0.5, anchor= CENTER)
	Our_JES5_16 = Button(glass, text = "JES5.16", command=lambda:LIBOSS_Click('JES5.16'), width = 12).place(relx = 0.75, rely = 0.35, anchor= CENTER)
	Our_JES5_16b = Button(glass, text = "JES5.16b", command=lambda:LIBOSS_Click('JES5.16b'), width = 12).place(relx = 0.75, rely = 0.5, anchor= CENTER)
	Our_JES5 = Button(glass, text = "JES5", command=lambda:LIBOSS_Click('JES5'), width = 12).place(relx = 0.75, rely = 0.2, anchor= CENTER)
	Our_JES5_16c = Button(glass, text = "JES5.16c", command=lambda:LIBOSS_Click('JES5.16c'), width = 12).place(relx = 0.75, rely = 0.65, anchor= CENTER)
	Our_JES5_16d = Button(glass, text = "JES5.16d", command=lambda:LIBOSS_Click('JES5.16d'), width = 12).place(relx = 0.75, rely = 0.8, anchor= CENTER)
	#LIBOSS_add = Button(glass, text = "LIBOSS Additives", command=LIBOSS_Add_Click, width = 16).place(relx = 0.5, rely = 0.7, anchor= CENTER)


def LNTO_Click():
	global lnto_id
	global date_made
	#global final_mass
	global comments
	global initial

	lnto = Toplevel()
	lnto.title("Enter LNTO data here")
	# lnto.iconbitmap(r'JES_logo.ico')
	reg_date=lnto.register(callback_date)
	reg_int=lnto.register(callback_int)
	reg_float=lnto.register(callback_float)
	inv_date = lnto.register(invalid_date)
	inv_int = lnto.register(invalid_int)
	inv_float = lnto.register(invalid_float)

	# User input box
	lnto_id_label = Label(lnto, text = "LNTO ID").grid(row = 0, column =0)
	lnto_id = Entry(lnto, width = 15)
	lnto_id.grid(row = 1, column =0, padx =5)
	lnto_id.insert(0, 'B23')

	date_made_label = Label(lnto, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(lnto, width = 15)
	date_made.grid(row = 1, column =1, padx =5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	# final_mass_label = Label(lnto, text = "Final Mass (g)").grid(row = 0, column =2)
	# final_mass = Entry(lnto, width = 15)
	# final_mass.grid(row = 1, column =2, padx =5)
	# final_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(lnto, text = "Comments").grid(row = 0, column =2)
	comments = Entry(lnto, width = 30)
	comments.grid(row = 1, column =2, padx =5)

	initial_label = Label(lnto, text = "Enter Initials Here").grid(row= 2, column = 1)
	initial = Entry(lnto, width = 15)
	initial.grid(row = 3, column =1, padx =5)

	button_submit = Button(lnto, text = "Upload Data", command=submit_lnto).grid(row = 3, column = 2)	
	
def Substrate_Sputter_Click():
	global substrate_id
	global base_foil
	global coating
	global date_made
	global sputter_duration
	global sputter_pressure
	global sputter_power
	global cleaning_time
	global blue
	global comments
	global initial

	substrate = Toplevel()
	substrate.title("Enter substrate data here")
	# substrate.iconbitmap(r'JES_logo.ico')
	reg_date=substrate.register(callback_date)
	reg_int=substrate.register(callback_int)
	reg_float=substrate.register(callback_float)
	reg_time = substrate.register(callback_time)
	inv_date = substrate.register(invalid_date)
	inv_int = substrate.register(invalid_int)
	inv_float = substrate.register(invalid_float)
	inv_time = substrate.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input box
	substrate_id_label = Label(substrate, text = "substrate ID").grid(row = 0, column =0)
	substrate_id = Entry(substrate, width = 30)
	substrate_id.grid(row = 1, column =0)
	substrate_id.insert(0, 'B23')

	base_foil_label = Label(substrate, text = "Base Foil").grid(row = 0, column =1)
	base_foil = Entry(substrate)
	cursor.execute("Select base_foil from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['base_foil'] is not None:
			base_foil.insert(0, result['base_foil'])
	base_foil.grid(row = 1, column =1)

	coating_label = Label(substrate, text = "Coating").grid(row = 0, column =2)
	coating = Entry(substrate)
	cursor.execute("Select coating from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['coating'] is not None:
			coating.insert(0, result['coating'])
	coating.grid(row = 1, column =2)

	date_made_label = Label(substrate, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =3)
	date_made = Entry(substrate)
	date_made.grid(row = 1, column =3)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	sputter_duration_label = Label(substrate, text = "Sputter Duration (HH:MM:SS)").grid(row = 0, column =4)
	sputter_duration = Entry(substrate)
	sputter_duration.grid(row = 1, column =4)
	cursor.execute("Select sputter_duration from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['sputter_duration'] is not None:
			sputter_duration.insert(0, result['sputter_duration'])
	sputter_duration.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	sputter_pressure_label = Label(substrate, text = "Sputter Pressure").grid(row = 0, column =5)
	sputter_pressure = Entry(substrate)
	sputter_pressure.grid(row = 1, column =5)
	sputter_pressure.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	sputter_power_label = Label(substrate, text = "Sputter Power").grid(row = 0, column =6)
	sputter_power = Entry(substrate)
	sputter_power.grid(row = 1, column =6)
	cursor.execute("Select sputter_power from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['sputter_power'] is not None:
			sputter_power.insert(0, result['sputter_power'])
	sputter_power.config(validate="focusout", validatecommand=(reg_int, '%P'), invalidcommand = (inv_int))

	cleaning_time_label = Label(substrate, text = "Cleaning Time (HH:MM:SS)").grid(row = 0, column =7)
	cleaning_time = Entry(substrate)
	cleaning_time.grid(row = 1, column =7)
	cursor.execute("Select cleaning_time from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['cleaning_time'] is not None:
			cleaning_time.insert(0, result['cleaning_time'])
	cleaning_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	blue = StringVar()
	blue.set(False)
	blue_label = Label(substrate, text = "Blue or White color?").grid(row = 0, column =8)
	blue_cb = Checkbutton(substrate, variable=blue, onvalue=1, offvalue=0)
	blue_cb.grid(row = 1, column =8)

	comments_label = Label(substrate, text = "Comments").grid(row = 0, column =9)
	comments = Entry(substrate)
	comments.grid(row = 1, column =9)

	initial_label = Label(substrate, text = "Enter Initials Here").grid(row= 2, column = 2)
	initial = Entry(substrate)
	initial.grid(row = 3, column =2)

	button_submit = Button(substrate, text = "Upload Data", command=submit_substrate_sputter).grid(row = 3, column = 3)	
		
	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Substrate_Cast_Click():
	global substrate_id
	global base_foil
	global coating
	global date_made
	global coating_mass
	global solvent_type
	global solvent_mass
	global casting_height
	global cure_time
	global cure_temp
	global comments
	global initial

	substrate = Toplevel()
	substrate.title("Enter substrate data here")
	# substrate.iconbitmap(r'JES_logo.ico')
	reg_date=substrate.register(callback_date)
	reg_int=substrate.register(callback_int)
	reg_float=substrate.register(callback_float)
	reg_time = substrate.register(callback_time)
	inv_date = substrate.register(invalid_date)
	inv_int = substrate.register(invalid_int)
	inv_float = substrate.register(invalid_float)
	inv_time = substrate.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input box
	substrate_id_label = Label(substrate, text = "substrate ID").grid(row = 0, column =0)
	substrate_id = Entry(substrate, width = 30)
	substrate_id.grid(row = 1, column =0)
	substrate_id.insert(0, 'B23')

	base_foil_label = Label(substrate, text = "Base Foil").grid(row = 0, column =1)
	base_foil = Entry(substrate)
	cursor.execute("Select base_foil from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['base_foil'] is not None:
			base_foil.insert(0, result['base_foil'])
	base_foil.grid(row = 1, column =1)

	coating_label = Label(substrate, text = "Coating").grid(row = 0, column =2)
	coating = Entry(substrate)
	cursor.execute("Select coating from cells.Cathode_Substrate order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['coating'] is not None:
			coating.insert(0, result['coating'])
	coating.grid(row = 1, column =2)

	date_made_label = Label(substrate, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =3)
	date_made = Entry(substrate)
	date_made.grid(row = 1, column =3)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	coating_mass_label = Label(substrate, text = "Coating Mass (g)").grid(row = 0, column =4)
	coating_mass = Entry(substrate)
	coating_mass.grid(row = 1, column =4)
	coating_mass.insert(0, 12)

	solvent_type_label = Label(substrate, text = "Solvent Type").grid(row = 0, column =5)
	solvent_type = Entry(substrate)
	solvent_type.grid(row = 1, column =5)
	solvent_type.insert(0, 'Ethanol')

	solvent_mass_label = Label(substrate, text = "Solvent Mass (g)").grid(row = 0, column =6)
	solvent_mass = Entry(substrate)
	solvent_mass.grid(row = 1, column =6)
	solvent_mass.insert(0, 3)

	casting_height_label = Label(substrate, text = "Casting Height (mils)").grid(row = 0, column =7)
	casting_height = Entry(substrate)
	casting_height.grid(row = 1, column =7)
	casting_height.insert(0, 0.5)

	cure_temp = Label(substrate, text = "Cure Temp °C").grid(row = 0, column =8)
	cure_temp = Entry(substrate)
	cure_temp.grid(row = 1, column =8)
	cure_temp.insert(0, 250)

	cure_time = Label(substrate, text = "Cure Time (HH:MM:SS)").grid(row = 0, column =9)
	cure_time = Entry(substrate)
	cure_time.grid(row = 1, column =9)
	cure_time.insert(0, '01:00:00')
	cure_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	comments_label = Label(substrate, text = "Comments").grid(row = 0, column =10)
	comments = Entry(substrate)
	comments.grid(row = 1, column =10)

	initial_label = Label(substrate, text = "Enter Initials Here").grid(row= 2, column = 2)
	initial = Entry(substrate)
	initial.grid(row = 3, column =2)

	button_submit = Button(substrate, text = "Upload Data", command=submit_substrate_cast).grid(row = 3, column = 3)	
		
	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Substrate_Click():
	substrate = Toplevel()
	substrate.title("Substrate Batch Type")
	substrate.geometry("300x200")

	substrate_label = Label(substrate, text = "Select Substrate Batch Type Here:", font = 'bold').place(relx=0.5, rely=0.3, anchor=CENTER)
	ag = Button(substrate, text = "Silver Coating on Al", command= Substrate_Cast_Click).place(relx = 0.3, rely = 0.5, anchor= CENTER)
	al = Button(substrate, text = "Al Coating on SS", command=Substrate_Sputter_Click).place(relx = 0.7, rely = 0.5, anchor= CENTER)

def Anode_Click():
	global sample_id
	global start
	global end
	global date_added
	global anode_type
	global active_area_size
	global aas
	global anode_thickness
	global comments
	global initial

	anode = Toplevel()
	anode.title("Enter anode data here")
	# anode.iconbitmap(r'JES_logo.ico')
	reg_date=anode.register(callback_date)
	reg_int=anode.register(callback_int)
	reg_float=anode.register(callback_float)
	inv_date = anode.register(invalid_date)
	inv_int = anode.register(invalid_int)
	inv_float = anode.register(invalid_float)

	# User input box
	sample_id_label = Label(anode, text = "Samples").grid(row = 0, column =0)
	sample_id = Entry(anode, width = 15)
	sample_id.grid(row = 1, column =0, padx = 5)

	start_label = Label(anode, text = "Starting Index").grid(row = 0, column =1)
	start = Entry(anode, width = 15)
	start.grid(row = 1, column =1, padx =5)

	end_label = Label(anode, text = "Last Index").grid(row = 0, column =2)
	end = Entry(anode, width = 15)
	end.grid(row = 1, column =2, padx =5)

	date_added_label = Label(anode, text = "Date added").grid(row = 0, column =3)
	date_added = Entry(anode, width =15)
	date_added.grid(row = 1, column =3, padx =5)
	date_added.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_added.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	anode_type_options = ['Li', 'In', 'Li/In', 'Au', 'Cu', 'Li w Au buffer']

	anode_type_label  = Label(anode, text = "Anode Type").grid(row = 0, column =4)
	anode_type = ttk.Combobox(anode, value = anode_type_options, width = 15)
	anode_type.current(0)
	anode_type.grid(row = 1, column = 4, padx =5)

	active_area_size_options = [2.85, 0.08, 10.3, 0.317, 1.27]

	active_area_size_label  = Label(anode, text = "Active Area Size [cm2]").grid(row = 0, column =5)
	active_area_size = ttk.Combobox(anode, value = active_area_size_options, width = 15)
	active_area_size.current(1)
	active_area_size.grid(row = 1, column = 5, padx =5)

	anode_thickness_label = Label(anode, text = "Anode Thickness (um)").grid(row = 0, column =7)
	anode_thickness = Entry(anode)
	anode_thickness.grid(row = 1, column =7, padx =5)
	anode_thickness.insert(0, 1.5)
	anode_thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(anode, text = "Comments").grid(row = 0, column =8)
	comments = Entry(anode)
	comments.grid(row = 1, column =8, padx =5)

	initial_label = Label(anode, text = "Enter Initials Here").grid(row= 2, column = 2)
	initial = Entry(anode, width = 15)
	initial.grid(row = 3, column =2, padx =5)

	button_submit = Button(anode, text = "Upload Data", command=submit_anode).grid(row = 3, column = 3)	


def CC_Click():
	global sample_id
	global start
	global end
	global date_added
	global anode_cc
	global anode_lead
	global anode_attach
	global cathode_cc
	global cathode_lead
	global cathode_attach
	global comments
	global initial

	cc = Toplevel()
	cc.title("Enter Current Collector data here")
	# cc.iconbitmap(r'JES_logo.ico')
	reg_date=cc.register(callback_date)
	reg_int=cc.register(callback_int)
	reg_float=cc.register(callback_float)
	inv_date = cc.register(invalid_date)
	inv_int = cc.register(invalid_int)
	inv_float = cc.register(invalid_float)

	# User input box
	sample_id_label = Label(cc, text = "Samples").grid(row = 0, column =0)
	sample_id = Entry(cc, width = 15)
	sample_id.grid(row = 1, column =0)

	start_label = Label(cc, text = "Starting Index").grid(row = 0, column =1)
	start = Entry(cc, width = 15)
	start.grid(row = 1, column =1, padx =5)

	end_label = Label(cc, text = "Last Index").grid(row = 0, column =2)
	end = Entry(cc, width = 15)
	end.grid(row = 1, column =2, padx =5)

	date_added_label = Label(cc, text = "Date Added").grid(row = 0, column =3)
	date_added = Entry(cc)
	date_added.grid(row = 1, column =3)
	date_added.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_added.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	anode_cc = StringVar()
	anode_cc.set('Select')
	anode_cc_options = ['Cu', 'None']
	anode_cc_label = Label(cc, text = "Anode Current Collector").grid(row = 0, column =4)
	acc = OptionMenu(cc, anode_cc, *anode_cc_options)
	acc.grid(row = 1, column =4)
	
	anode_lead = StringVar()
	anode_lead.set('Select')
	anode_lead_options = ['Cu']
	anode_lead_label = Label(cc, text = "Anode Lead").grid(row = 0, column =5)
	al = OptionMenu(cc, anode_lead, *anode_lead_options)
	al.grid(row = 1, column =5)

	anode_attach = StringVar()
	anode_attach.set('Select')
	anode_attach_options = ['Cu tape', 'Li', 'Epoxy']
	anode_attach_label = Label(cc, text = "Anode Lead Attachment").grid(row = 0, column =6)
	at = OptionMenu(cc, anode_attach, *anode_attach_options)
	at.grid(row = 1, column =6)

	cathode_cc = StringVar()
	cathode_cc.set('Select')
	cathode_cc_options = ['Al', 'SS', 'Al coated SS']
	cathode_cc_label = Label(cc, text = "Cathode Current Collector").grid(row = 0, column =7)
	ccc = OptionMenu(cc, cathode_cc, *cathode_cc_options)
	ccc.grid(row = 1, column =7)
	
	cathode_lead = StringVar()
	cathode_lead.set('Select')
	cathode_lead_options = ['Ni', 'Al']
	cathode_lead_label = Label(cc, text = "Cathode Lead").grid(row = 0, column =8)
	cl = OptionMenu(cc, cathode_lead, *cathode_lead_options)
	cl.grid(row = 1, column =8)

	cathode_attach = StringVar()
	cathode_attach.set('Select')
	cathode_attach_options = ['Spot weld']
	cathode_attach_label = Label(cc, text = "Cathode Lead Attachment").grid(row = 0, column =9)
	ct = OptionMenu(cc, cathode_attach, *cathode_attach_options)
	ct.grid(row = 1, column =9)

	comments_label = Label(cc, text = "Comments").grid(row = 0, column =10)
	comments = Entry(cc)
	comments.grid(row = 1, column =10)

	initial_label = Label(cc, text = "Enter Initials Here").grid(row= 2, column = 2)
	initial = Entry(cc, width = 15)
	initial.grid(row = 3, column =2)

	button_submit = Button(cc, text = "Upload Data", command=submit_cc).grid(row = 3, column = 3)		

def Houdini_stage_click(code, new_sample_id):
	global sample_id
	global date_made
	global glass_id
	global cathode_coating
	global furnace_temp
	global furnace_time
	global stage_temp
	global o2
	global h2o
	global roller_speed
	global tab
	global tab_material
	global cover
	global cover_material
	global cover_thickness
	global cw
	global cw_material
	global comments
	global initial
	global coating_batch
	global roll_temp
	global cathode_id
	global roll_gap
	global gb5_exp
	global sleeve
	global sleeve_material

	glass = Toplevel()
	glass.title("Enter " + code + " Sample data here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	reg_time = glass.register(callback_time)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	inv_time = glass.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input box
	sample_id_label = Label(glass, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(glass, width = 15)
	sample_id.grid(row = 1, column =0, padx = 5)
	sample_id.insert(0, new_sample_id)

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx = 5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	cathode_id_label = Label(glass, text = "Cathode ID").grid(row = 0, column =2)
	cathode_id = Entry(glass, width = 15)
	cathode_id.grid(row = 1, column =2, padx = 5)
	cathode_id.insert(0, entered_cathode_id.get())

	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =3)
	glass_id = Entry(glass, width = 15)
	cursor.execute("Select glass_id from cells.glass order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['glass_id'] is not None:
			glass_id.insert(0, result['glass_id'])
	glass_id.grid(row = 1, column =3, padx = 5)

	cathode_coating_options = ['None', 'LNTO', 'LNO', 'LLZO sol gel', 'Li Silicate', 'LBCO', 'LBO', 'a-LBCO']
	cathode_coating = ttk.Combobox(glass, value = cathode_coating_options)
	cathode_coating.current(0)
	cathode_coating_label = Label(glass, text = "Cathode Coating").grid(row = 0, column =4)
	cathode_coating.grid(row = 1, column =4, padx =5)

	coating_batch_label = Label(glass, text = "Coating Batch").grid(row = 0, column =5)
	coating_batch = Entry(glass, width = 15)
	coating_batch.grid(row = 1, column =5, padx =5)
	coating_batch.insert(0, 'B23')

	furnace_temp_label = Label(glass, text = "Furnace Temp (°C)").grid(row = 0, column =6)
	furnace_temp = Entry(glass, width = 15)
	furnace_temp.grid(row = 1, column =6, padx = 5)
	furnace_temp.insert(0, 750)
	furnace_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 0, column =7)
	furnace_time = Entry(glass, width = 15)
	furnace_time.grid(row = 1, column =7, padx = 5)
	furnace_time.insert(0, '00:05:00')
	furnace_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	if (code == 'Houdini Stage' or code == 'Hot Roll'):
		stage_temp_label = Label(glass, text = "Stage Temp (°C)").grid(row = 0, column =8)
		stage_temp = Entry(glass, width = 15)
		stage_temp.grid(row = 1, column =8, padx = 5)
		stage_temp.insert(0, 350)
		stage_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		cw = IntVar()
		cw.set(1)
		cw_label = Label(glass, text = "Cathode weight? (Y/N)").grid(row = 2, column =9)
		cw_cb = Checkbutton(glass, variable=cw, onvalue=1, offvalue=0)
		cw_cb.grid(row = 3, column =9, padx = 5)

		cw_material_label = Label(glass, text = "CW Material").grid(row = 2, column =10)
		cw_material = Entry(glass, width = 15)
		cw_material.grid(row = 3, column =10, padx = 5)
		cw_material.insert(0, 'Steel cathode w/ Al foil & insulation')

	roller_speed_label = Label(glass, text = "Roller Speed (Hz)").grid(row = 0, column =9)
	roller_speed = Entry(glass, width = 10)
	roller_speed.grid(row = 1, column =9, padx = 5)

	if (code == 'Houdini Stage' or code == 'Roll Quench'):
		roller_speed.insert(0, 15)

		gb5_exp = Label(glass, text = "GB5 Exposure (HH:MM:SS)").grid(row = 0, column =11)
		gb5_exp = Entry(glass, width = 15)
		gb5_exp.grid(row = 1, column =11, padx = 5)
		gb5_exp.insert(0, '00:20:00')

		o2_label = Label(glass, text = "O2 Level (ppm)").grid(row = 2, column =0)
		o2 = Entry(glass, width = 15)
		o2.grid(row = 3, column =0, padx = 5)
		o2.insert(0, 0.1)

		h2o_label = Label(glass, text = "H2O Level (ppm)").grid(row = 2, column =1)
		h2o = Entry(glass, width = 15)
		h2o.grid(row = 3, column =1, padx = 5)
		h2o.insert(0, 1.5)

		roll_gap_insert = 10

	elif code == 'Hot Roll':
		roller_speed.insert(0, 60)

		roll_temp_label = Label(glass, text = "Roller Temp °C").grid(row = 2, column =0)
		roll_temp = Entry(glass, width = 15)
		roll_temp.grid(row = 3, column =0, padx = 5)
		roll_temp.insert(0, 212)

		roll_gap_insert = 3

	roll_gap_label = Label(glass, text = "Roller Gap (mil)").grid(row = 0, column =10)
	roll_gap = Entry(glass, width = 15)
	roll_gap.grid(row = 1, column =10, padx = 5)
	roll_gap.insert(0, roll_gap_insert)

	tab = IntVar()
	tab.set(1)
	tab_label = Label(glass, text = "Tab? (Y/N)").grid(row = 2, column =2)
	tab_cb = Checkbutton(glass, variable=tab, onvalue=1, offvalue=0)
	tab_cb.grid(row = 3, column =2, padx = 5)

	tab_material_options = ['Select', 'Brass', 'LLZO Brass', 'LLZO Al', 'BN Al', 'BN Brass', 'Copper', 'Steel', 'GC on Al', 'GC on SS']

	tab_material_label  = Label(glass, text = "Tab Material").grid(row = 2, column =3)
	tab_material = ttk.Combobox(glass, value = tab_material_options)
	tab_material.current(3)
	tab_material.grid(row = 3, column =3, padx = 5)

	cover = IntVar()
	cover.set(1)
	cover_label = Label(glass, text = "Cover? (Y/N)").grid(row = 2, column =4)
	cover_cb = Checkbutton(glass, variable=cover, onvalue=1, offvalue=0)
	cover_cb.grid(row = 3, column =4, padx = 5)

	cover_material_label = Label(glass, text = "Cover Material").grid(row = 2, column =5)
	cover_material = Entry(glass, width = 15)
	cover_material.grid(row = 3, column =5)
	cover_material.insert(0, 'Brass')

	cover_thickness_label = Label(glass, text = "Cover thickness (um)?").grid(row = 2, column =6)
	cover_thickness = Entry(glass, width = 15)
	cover_thickness.grid(row = 3, column =6, padx = 5)
	cover_thickness.insert(0, '25')
	cover_thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	sleeve = IntVar()
	sleeve.set(1)
	sleeve_label = Label(glass, text = "Sleeve? (Y/N)").grid(row = 2, column =7)
	sleeve_cb = Checkbutton(glass, variable=sleeve, onvalue=1, offvalue=0)
	sleeve_cb.grid(row = 3, column =7, padx = 5)

	sleeve_material_label  = Label(glass, text = "Sleeve Material").grid(row = 2, column =8)
	sleeve_material = Entry(glass, width = 15)
	sleeve_material.grid(row = 3, column =8, padx =5)
	sleeve_material.insert(0, '2 mil Brass')

	comments_label = Label(glass, text = "Comments").grid(row = 4, column =0)
	comments = Entry(glass, width = 30)
	comments.grid(row = 5, column =0, padx = 5, columnspan =2)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 3)
	initial = Entry(glass)
	initial.grid(row = 5, column =3)

	button_submit = Button(glass, text = "Upload Data", command=lambda: submit_sample(code, new_sample_id)).grid(row = 5, column = 4)

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def No_stage_click(code, new_sample_id):
	global sample_id
	global date_made
	global glass_id
	global cathode_coating
	global furnace_temp
	global furnace_time
	global cathode_id
	# global o2
	# global h2o
	global roller_speed
	global hot_plate_temp
	global tab
	global tab_material
	global cover
	global cover_material
	global cover_thickness
	global comments
	global initial
	global coating_batch

	glass = Toplevel()
	glass.title("Enter Sample data here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	reg_time = glass.register(callback_time)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	inv_time = glass.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input box
	sample_id_label = Label(glass, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(glass, width = 15)
	sample_id.grid(row = 1, column =0, padx = 5)
	sample_id.insert(0, new_sample_id)

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx = 5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	cathode_id_label = Label(glass, text = "Cathode ID").grid(row = 0, column =2)
	cathode_id = Entry(glass, width = 15)
	cathode_id.grid(row = 1, column =2, padx = 5)
	cathode_id.insert(0, entered_cathode_id.get())

	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =3)
	glass_id = Entry(glass, width = 15)
	cursor.execute("Select glass_id from cells.glass order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['glass_id'] is not None:
			glass_id.insert(0, result['glass_id'])
	glass_id.grid(row = 1, column =3, padx = 5)

	cathode_coating_options = ['None', 'LNTO', 'LNO', 'LLZO sol gel', 'Li Silicate', 'LBCO', 'LBO', 'a-LBCO']
	cathode_coating = ttk.Combobox(glass, value = cathode_coating_options)
	cathode_coating.current(0)
	cathode_coating_label = Label(glass, text = "Cathode Coating").grid(row = 0, column =4)
	cathode_coating.grid(row = 1, column =4, padx =5)

	coating_batch_label = Label(glass, text = "Coating Batch").grid(row = 0, column =5)
	coating_batch = Entry(glass, width = 15)
	coating_batch.grid(row = 1, column =5, padx =5)
	coating_batch.insert(0, 'B23')

	furnace_temp_label = Label(glass, text = "Furnace Temp (°C)").grid(row = 0, column =6)
	furnace_temp = Entry(glass, width = 15)
	furnace_temp.grid(row = 1, column =6, padx = 5)
	furnace_temp.insert(0, 850)
	furnace_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 0, column =7)
	furnace_time = Entry(glass, width = 15)
	furnace_time.grid(row = 1, column =7, padx = 5)
	furnace_time.insert(0, '00:02:00')
	furnace_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	# o2_label = Label(glass, text = "O2 Level (ppm)").grid(row = 0, column =8)
	# o2 = Entry(glass, width = 15)
	# o2.grid(row = 1, column =8, padx = 5)
	# o2.insert(0, 0.1)
	# o2.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# h2o_label = Label(glass, text = "H2O Level (ppm)").grid(row = 0, column =9)
	# h2o = Entry(glass, width = 15)
	# h2o.grid(row = 1, column =9, padx = 5)
	# h2o.insert(0, 2.5)
	# h2o.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	if code == 'Roll Quench':
		roller_speed_label = Label(glass, text = "Roller Speed (Hz)").grid(row = 2, column =0)
		roller_speed = Entry(glass, width = 10)
		roller_speed.grid(row = 3, column =0, padx = 5)
		roller_speed.insert(0, 15)
	elif code == 'Rolling Pin':
		hot_plate_temp_label = Label(glass, text = "Hot Plate Temp (°C)").grid(row = 2, column =0)
		hot_plate_temp = Entry(glass, width = 10)
		hot_plate_temp.grid(row = 3, column =0, padx = 5)
		hot_plate_temp.insert(0, 300)

	tab = IntVar()
	tab.set(1)
	tab_label = Label(glass, text = "Tab? (Y/N)").grid(row = 2, column =1)
	tab_cb = Checkbutton(glass, variable=tab, onvalue=1, offvalue=0)
	tab_cb.grid(row = 3, column =1, padx = 5)

	tab_material_options = ['Select', 'Brass', 'GC on Al', 'GC on SS', 'BN Brass', 'Copper', 'Steel']

	tab_material_label  = Label(glass, text = "Tab Material").grid(row = 2, column =2)
	tab_material = ttk.Combobox(glass, value = tab_material_options)
	tab_material.current(1)
	tab_material.grid(row = 3, column =2, padx = 5)

	cover = IntVar()
	cover.set(1)
	cover_label = Label(glass, text = "Cover? (Y/N)").grid(row = 2, column =3)
	cover_cb = Checkbutton(glass, variable=cover, onvalue=1, offvalue=0)
	cover_cb.grid(row = 3, column =3, padx = 5)

	cover_material_label = Label(glass, text = "Cover Material").grid(row = 2, column =4)
	cover_material = Entry(glass, width = 15)
	cover_material.grid(row = 3, column =4)
	cover_material.insert(0, 'Brass')

	cover_thickness_label = Label(glass, text = "Cover thickness (um)?").grid(row = 2, column =5)
	cover_thickness = Entry(glass, width = 15)
	cover_thickness.grid(row = 3, column =5, padx = 5)
	cover_thickness.insert(0, '25')
	cover_thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))


	comments_label = Label(glass, text = "Comments").grid(row = 2, column =6)
	comments = Entry(glass, width = 15)
	comments.grid(row = 3, column =6, padx = 5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 2)
	initial = Entry(glass)
	initial.grid(row = 5, column =2)

	button_submit = Button(glass, text = "Upload Data", command= lambda: submit_sample(code, new_sample_id)).grid(row = 5, column = 3)

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Stamp_Quench_click(new_sample_id):
	global sample_id
	global date_made
	global glass_id
	global cathode_coating
	global coating_batch
	global furnace_temp
	global furnace_time
	global cathode_id
	# global o2
	# global h2o
	# global roller_speed
	# global tab
	# global tab_material
	# global cover
	# global cover_material
	# global cover_thickness
	global hot_plate_temp
	global muffle_furnace
	global muffle_furnace_temp
	global muffle_furnace_time
	global comments
	global initial

	glass = Toplevel()
	glass.title("Enter Sample data here")
	# glass.iconbitmap(r'JES_logo.ico')
	reg_date=glass.register(callback_date)
	reg_int=glass.register(callback_int)
	reg_float=glass.register(callback_float)
	reg_time = glass.register(callback_time)
	inv_date = glass.register(invalid_date)
	inv_int = glass.register(invalid_int)
	inv_float = glass.register(invalid_float)
	inv_time = glass.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input box
	sample_id_label = Label(glass, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(glass, width = 15)
	sample_id.grid(row = 1, column =0, padx = 5)
	sample_id.insert(0, new_sample_id)

	date_made_label = Label(glass, text = "Date Made").grid(row = 0, column =1)
	date_made = Entry(glass, width = 15)
	date_made.grid(row = 1, column =1, padx = 5)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	cathode_id_label = Label(glass, text = "Cathode ID").grid(row = 0, column =2)
	cathode_id = Entry(glass, width = 15)
	cathode_id.grid(row = 1, column =2, padx = 5)
	cathode_id.insert(0, entered_cathode_id.get())

	glass_id_label = Label(glass, text = "Glass ID").grid(row = 0, column =3)
	glass_id = Entry(glass, width = 15)
	cursor.execute("Select glass_id from cells.glass order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['glass_id'] is not None:
			glass_id.insert(0, result['glass_id'])
	glass_id.grid(row = 1, column =3, padx = 5)

	cathode_coating_options = ['None', 'LNTO', 'LNO', 'LLZO sol gel', 'Li Silicate', 'LBCO', 'LBO', 'a-LBCO']
	cathode_coating = ttk.Combobox(glass, value = cathode_coating_options)
	cathode_coating.current(0)
	cathode_coating_label = Label(glass, text = "Cathode Coating").grid(row = 0, column =4)
	cathode_coating.grid(row = 1, column =4, padx =5)

	coating_batch_label = Label(glass, text = "Coating Batch").grid(row = 0, column =5)
	coating_batch = Entry(glass, width = 15)
	coating_batch.grid(row = 1, column =5, padx =5)
	coating_batch.insert(0, 'B23')

	furnace_temp_label = Label(glass, text = "Furnace Temp (°C)").grid(row = 0, column =6)
	furnace_temp = Entry(glass, width = 15)
	furnace_temp.grid(row = 1, column =6, padx = 5)
	furnace_temp.insert(0, 850)
	furnace_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	furnace_time_label = Label(glass, text = "Furnace Time (HH:MM:SS)").grid(row = 0, column =7)
	furnace_time = Entry(glass, width = 15)
	furnace_time.grid(row = 1, column =7, padx = 5)
	furnace_time.insert(0, '00:10:00')
	furnace_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	# o2_label = Label(glass, text = "O2 Level (ppm)").grid(row = 0, column =7)
	# o2 = Entry(glass, width = 15)
	# o2.grid(row = 1, column =7, padx = 5)
	# o2.insert(0, 0.1)
	# o2.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# h2o_label = Label(glass, text = "H2O Level (ppm)").grid(row = 0, column =8)
	# h2o = Entry(glass, width = 15)
	# h2o.grid(row = 1, column =8, padx = 5)
	# h2o.insert(0, 2.5)
	# h2o.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	hot_plate_temp_label = Label(glass, text = "Hot Plate Temp °C").grid(row = 2, column =0)
	hot_plate_temp = Entry(glass, width = 15)
	hot_plate_temp.grid(row = 3, column =0, padx = 5)
	hot_plate_temp.insert(0, 300)

	muffle_furnace = IntVar()
	muffle_furnace.set(1)
	muffle_furnace_label = Label(glass, text = "Muffle Furnace? (Y/N)").grid(row = 2, column =1)
	muffle_furnace_cb = Checkbutton(glass, variable=muffle_furnace, onvalue=1, offvalue=0)
	muffle_furnace_cb.grid(row = 3, column =1, padx = 5)

	muffle_furnace_temp_label = Label(glass, text = "Muffle Furnace Temp °C").grid(row = 2, column =2)
	muffle_furnace_temp = Entry(glass, width = 15)
	muffle_furnace_temp.grid(row = 3, column =2, padx = 5)
	muffle_furnace_temp.insert(0, 400)
	
	muffle_furnace_time_label = Label(glass, text = "Muffle Furnace Time (HH:MM:SS)").grid(row = 2, column =3)
	muffle_furnace_time = Entry(glass, width = 15)
	muffle_furnace_time.grid(row = 3, column =3, padx = 5)
	muffle_furnace_time.insert(0, '00:15:00')
	
	# roller_speed_label = Label(glass, text = "Roller Speed (Hz)").grid(row = 0, column =9)
	# roller_speed = Entry(glass, width = 10)
	# roller_speed.grid(row = 1, column =9, padx = 5)
	# roller_speed.insert(0, 15)
	# roller_speed.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# tab = IntVar()
	# tab.set(1)
	# tab_label = Label(glass, text = "Tab? (Y/N)").grid(row = 0, column =10)
	# tab_cb = Checkbutton(glass, variable=tab, onvalue=1, offvalue=0)
	# tab_cb.grid(row = 1, column =10, padx = 5)

	# tab_material_label = Label(glass, text = "Tab Material").grid(row = 0, column =11)
	# tab_material = Entry(glass, width = 15)
	# tab_material.grid(row = 1, column =11, padx = 5)
	# tab_material.insert(0, 'BN Brass')

	# cover = IntVar()
	# cover.set(1)
	# cover_label = Label(glass, text = "Cover? (Y/N)").grid(row = 0, column =12)
	# cover_cb = Checkbutton(glass, variable=cover, onvalue=1, offvalue=0)
	# cover_cb.grid(row = 1, column =12, padx = 5)

	# cover_material_label = Label(glass, text = "Cover Material").grid(row = 0, column =13)
	# cover_material = Entry(glass, width = 15)
	# cover_material.grid(row = 1, column =13)
	# cover_material.insert(0, 'Brass')

	# cover_thickness_label = Label(glass, text = "Cover thickness (um)?").grid(row = 0, column =14)
	# cover_thickness = Entry(glass, width = 15)
	# cover_thickness.grid(row = 1, column =14, padx = 5)
	# cover_thickness.insert(0, '25')
	# cover_thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(glass, text = "Comments").grid(row = 2, column =4)
	comments = Entry(glass, width = 15)
	comments.grid(row = 3, column =4, padx = 5)

	initial_label = Label(glass, text = "Enter Initials Here").grid(row= 4, column = 2)
	initial = Entry(glass)
	initial.grid(row = 5, column =2)

	button_submit = Button(glass, text = "Upload Data", command= lambda: submit_sample("Stamp Quench", new_sample_id)).grid(row = 5, column = 3)

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Sample_Click2():
	sample = Toplevel()
	sample.title("Quench Method")
	sample.geometry("300x200")

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	cursor.execute("Select sample_id from cells.samples where cathode_id like %s order by sample_id desc limit 1", entered_cathode_id.get())
	result = cursor.fetchone()

	if result is not None:
		if result['sample_id'] is not None:
			# update digits if cathode already in use
			last_sample_id = result['sample_id']

			new_sample_id = int(last_sample_id[-2:]) + 1 

			if new_sample_id < 10:
				new_sample_id = '0' + str(new_sample_id)
			else:
				new_sample_id = str(new_sample_id)

			new_sample_id = last_sample_id[0:3] + new_sample_id
	else:
		# create new sample id based on alphabet if cathode not in use

		# get most recent cathode id
		cursor.execute("Select sample_id, cathode_id from cells.samples where cathode_id like 'B%' order by cathode_id desc, sample_id desc limit 1;")
		result = cursor.fetchone()
		last_cathode_id = result['cathode_id']
		last_sample_id = result['sample_id'][0:2]

		#update based on alphabet
		if last_sample_id[-1] == 'Z':
			first_letter = chr(ord(last_sample_id[0]) + 1).upper()
			second_letter = 'A'
		else:
			first_letter = last_sample_id[0].upper()
			second_letter = chr(ord(last_sample_id[-1]) + 1).upper()

		third_letter = str(entered_cathode_id.get()[-1]).upper()

		new_sample_id = first_letter + second_letter + third_letter + '01'

	sample_label = Label(sample, text = "Select Extrusion Method Here:", font = 'bold').place(relx=0.5, rely=0.2, anchor=CENTER)
	stamp_quench = Button(sample, text = "Stamp Quench", command= lambda: Stamp_Quench_click(new_sample_id), width = 15).place(relx = 0.5, rely = 0.4, anchor= CENTER)
	no_stage = Button(sample, text = "Roll Quench: \n No Stage", command= lambda: Houdini_stage_click('Roll Quench', new_sample_id), width = 15).place(relx = 0.3, rely = 0.6, anchor= CENTER)
	houdini_stage = Button(sample, text = "Roll Quench: \n Houdini Stage", command=lambda: Houdini_stage_click('Houdini Stage', new_sample_id), width = 15).place(relx = 0.7, rely = 0.6, anchor= CENTER)
	rolling_pin = Button(sample, text = "Rolling Pin", command=lambda: No_stage_click('Rolling Pin', new_sample_id), width = 15).place(relx = 0.3, rely = 0.8, anchor= CENTER)
	hot_roll = Button(sample, text = "Hot Roll", command=lambda: Houdini_stage_click('Hot Roll', new_sample_id), width = 15).place(relx = 0.7, rely = 0.8, anchor= CENTER)

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Sample_Click():
	sample = Toplevel()
	sample.title("Quench Method")
	sample.geometry("300x200")

	global entered_cathode_id

	sample_label = Label(sample, text = "Enter Cathode Batch Here:", font = 'bold').place(relx=0.5, rely=0.2, anchor=CENTER)

	entered_cathode_id = Entry(sample, width = 15)
	entered_cathode_id.place(relx = 0.5, rely = 0.4, anchor= CENTER)

	enter = Button(sample, text = "Next", command= Sample_Click2).place(relx = 0.5, rely = 0.6, anchor= CENTER)
	
def Sulfide_Cathode_Click(code):
	global cathode_id
	global description
	global date_made
	global particle_coating
	global casting_coating
	global active_material_vol_percent
	global active_material_type
	global active_material_mass
	global packing_density
	global Glass_id
	global Glass_mass
	global dispersant_type
	global dispersant_mass
	global solvent1_type
	global solvent1_mass
	global balls_small_mass
	global balls_large_mass
	global composite_density
	global milling_time
	global milling_speed
	global substrate_id
	global casting_temp
	global casting_bar_setting
	global casting_bar_type
	global estimate_cathode_thickness
	global num_rolling_layers
	global roller
	global rolling_procedure
	global LNTO_coating
	global LNTO_id
	global cnt_wt_pct
	global cnt_mass
	global comments
	global silica_wt_pct
	global silica_mass
	global initial
	global heat_treatment_temp
	global heat_treatment_time
	global samples
	global mix_speed
	global mix_time
	global mix_rounds

	cathode = Toplevel()
	cathode.title("Enter Sulfide Cathode data here")
	# cathode.iconbitmap(r'JES_logo.ico')
	reg_date=cathode.register(callback_date)
	reg_int=cathode.register(callback_int)
	reg_float=cathode.register(callback_float)
	reg_time = cathode.register(callback_time)
	inv_date = cathode.register(invalid_date)
	inv_int = cathode.register(invalid_int)
	inv_float = cathode.register(invalid_float)
	inv_time = cathode.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input boxes

	cathode_id_label = Label(cathode, text = "Cathode ID").grid(row = 0, column =0)
	cathode_id = Entry(cathode, width = 20)
	cathode_id.grid(row = 1, column =0)
	cathode_id.insert(0, 'B23')

	description_label = Label(cathode, text = "Description").grid(row = 0, column =7)
	description = Entry(cathode, width = 20)
	description.grid(row = 1, column =7)

	date_made_label = Label(cathode, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =1)
	date_made = Entry(cathode, width = 20)
	date_made.grid(row = 1, column =1)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	particle_coating_options = ['None', 'LipSi', 'LNTO', 'NTiO', 'LDP', 'LLZO sol gel', 'LBCSO', 'LBCO', 'LBO']

	particle_coating_label = Label(cathode, text = "Particle Coating").grid(row = 0, column =2)
	particle_coating = ttk.Combobox(cathode, value = particle_coating_options, width = 20)
	particle_coating.current(0)
	particle_coating.grid(row = 1, column =2)

	casting_coating_options = ['None', 'LipSi', 'LNTO', 'NTiO', 'LDP', 'LLZO sol gel', 'LBCSO', 'LBCO', 'LBO']

	casting_coating_label = Label(cathode, text = "Casting Coating").grid(row = 0, column =3)
	casting_coating = ttk.Combobox(cathode, value = casting_coating_options, width = 20)
	casting_coating.current(0)
	casting_coating.grid(row = 1, column =3, padx = 5)

	active_material_vol_percent_label = Label(cathode, text = "Active Material vol%").grid(row = 0, column =4)
	active_material_vol_percent = Entry(cathode, width = 20)
	cursor.execute("Select active_material_vol from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['active_material_vol'] is not None:
			active_material_vol_percent.insert(0, result['active_material_vol'])
	else:
		active_material_vol_percent.insert(0, '')
	active_material_vol_percent.grid(row = 1, column =4)


	active_material_type_options = ['Agl 622 NMC', 'Agl 811 NMC', 'SC 622 NMC', 'SC 631 NMC', 'SC 955 NMC', 'LiNbO coated 811 NMC']

	active_material_type_label = Label(cathode, text = "Active Material Type").grid(row = 0, column =5)
	active_material_type = ttk.Combobox(cathode, value = active_material_type_options, width = 20)
	active_material_type.current(0)
	active_material_type.grid(row = 1, column =5)

	active_material_mass_label = Label(cathode, text = "Active Material Mass (g)").grid(row = 0, column =6)
	active_material_mass = Entry(cathode, width = 20)
	active_material_mass.grid(row = 1, column =6)
	cursor.execute("Select active_material_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['active_material_mass'] is not None:
			active_material_mass.insert(0, result['active_material_mass'])
	active_material_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	Glass_id_label = Label(cathode, text = "Glass ID").grid(row = 4, column =0)
	Glass_id = Entry(cathode, width = 20)
	cursor.execute("Select Glass_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['Glass_id'] is not None:
			Glass_id.insert(0, result['Glass_id'])
	Glass_id.grid(row = 5, column =0)

	Glass_mass_label = Label(cathode, text = "Glass Mass (g)").grid(row = 4, column =1)
	Glass_mass = Entry(cathode, width = 20)
	Glass_mass.grid(row = 5, column =1)
	cursor.execute("Select Glass_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['Glass_mass'] is not None:
			Glass_mass.insert(0, result['Glass_mass'])
	Glass_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	dispersant_type_label = Label(cathode, text = "Dispersant Type").grid(row = 4, column =2)
	dispersant_type = Entry(cathode, width = 20)
	# cursor.execute("Select dispersant_type from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['dispersant_type'] is not None:
	# 		dispersant_type.insert(0, result['dispersant_type'])
	dispersant_type.insert(0, 'PMHSO')
	dispersant_type.grid(row = 5, column =2)

	dispersant_mass_label = Label(cathode, text = "Dispersant Mass (g)").grid(row = 4, column =3)
	dispersant_mass = Entry(cathode, width = 20)
	dispersant_mass.grid(row = 5, column =3)
	cursor.execute("Select dispersant_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['dispersant_mass'] is not None:
			dispersant_mass.insert(0, result['dispersant_mass'])
	dispersant_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	heat_treatment_time_label = Label(cathode, text = "Heat Treatment Time (HH:MM:SS)").grid(row = 4, column =4)
	heat_treatment_time = Entry(cathode, width = 20)
	heat_treatment_time.grid(row = 5, column = 4)
	heat_treatment_time.insert(0, '01:00:00')
	heat_treatment_time.config(validate = 'focusout', validatecommand = (reg_time, '%P'), invalidcommand = (inv_time))

	heat_treatment_temp_label = Label(cathode, text = "Heat Treatment Temp °C").grid(row = 4, column =5)
	heat_treatment_temp = Entry(cathode, width = 20)
	heat_treatment_temp.grid(row = 5, column = 5)
	heat_treatment_temp.insert(0, 200)
	heat_treatment_temp.config(validate = 'focusout', validatecommand = (reg_int, '%P'), invalidcommand = (inv_int))

	composite_density_label = Label(cathode, text = "Composite Density").grid(row = 4, column =6)
	composite_density = Entry(cathode, width = 20)
	composite_density.grid(row = 5, column =6)
	# cursor.execute("Select composite_density from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['composite_density'] is not None:
	# 		composite_density.insert(0, result['composite_density'])
	composite_density.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	# viscosity_label = Label(cathode, text = "Viscosity").grid(row = 7, column =0)
	# viscosity = Entry(cathode, width = 20)
	# viscosity.grid(row = 8, column =0, padx =5)
	# # cursor.execute("Select viscosity from cells.cathode order by date_made desc limit 1")
	# # result = cursor.fetchone()
	# # if result is not None:
	# # 	if result['viscosity'] is not None:
	# # 		viscosity.insert(0, result['viscosity'])
	# viscosity.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	solvent1_type_label = Label(cathode, text = "Solvent 1 Type").grid(row = 7, column =1)
	solvent1_type = Entry(cathode, width = 20)
	solvent1_type.insert(0, 'ACN, anhydrous')
	solvent1_type.grid(row = 8, column =1)

	solvent1_mass_label = Label(cathode, text = "Solvent 1 Mass (g)").grid(row = 7, column =2)
	solvent1_mass = Entry(cathode, width = 20)
	solvent1_mass.grid(row = 8, column =2)
	cursor.execute("Select solvent1_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['solvent1_mass'] is not None:
			solvent1_mass.insert(0, result['solvent1_mass'])
	solvent1_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	if code == 'mill':
		milling_time_label = Label(cathode, text = "Milling Time (HH:MM:SS)").grid(row = 7, column =3)
		milling_time = Entry(cathode, width = 20)
		milling_time.grid(row = 8, column =3)
		milling_time.insert(0, '01:00:00')

		milling_speed_label = Label(cathode, text = "Milling Speed (rpm)").grid(row = 7, column =4)
		milling_speed = Entry(cathode, width = 20)
		milling_speed.grid(row = 8, column =4)
		milling_speed.insert(0, 400)

		balls_small_mass_label = Label(cathode, text = "Small Balls Mass (g)").grid(row = 7, column =5)
		balls_small_mass = Entry(cathode, width = 20)
		balls_small_mass.grid(row = 8, column =5)
		balls_small_mass.insert(0, 16)
		balls_small_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

		balls_large_mass_label = Label(cathode, text = "Large Balls Mass (g)").grid(row = 7, column =6)
		balls_large_mass = Entry(cathode, width = 20)
		balls_large_mass.grid(row = 8, column =6)
		balls_large_mass.insert(0, 14)
		balls_large_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	elif code == 'mix':
		mix_time_label = Label(cathode, text = "Speed Mix Time (HH:MM:SS)").grid(row = 7, column =3)
		mix_time = Entry(cathode, width = 20)
		mix_time.grid(row = 8, column =3)
		mix_time.insert(0, '00:05:00')

		mix_speed_label = Label(cathode, text = "Speed Mix (rpm)").grid(row = 7, column =4)
		mix_speed = Entry(cathode, width = 20)
		mix_speed.grid(row = 8, column =4)
		mix_speed.insert(0, 1200)

		mix_rounds_label = Label(cathode, text = "Speed Mix Rounds").grid(row = 7, column =5)
		mix_rounds = Entry(cathode, width = 20)
		mix_rounds.grid(row = 8, column =5)
		mix_rounds.insert(0, 3)

	substrate_id_label = Label(cathode, text = "Substrate ID").grid(row = 7, column =0)
	substrate_id = Entry(cathode, width = 20)
	cursor.execute("Select substrate_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['substrate_id'] is not None:
			substrate_id.insert(0, result['substrate_id'])
	substrate_id.grid(row = 8, column =0)

	casting_bar_setting_label = Label(cathode, text = "Casting Bar Setting").grid(row = 10, column =1)
	casting_bar_setting = Entry(cathode, width = 20)
	casting_bar_setting.grid(row = 11, column =1)
	casting_bar_setting.insert(0, 50)

	casting_bar_type_label = Label(cathode, text = "Casting Bar Type").grid(row = 10, column =2)
	casting_bar_type = Entry(cathode, width = 20)
	casting_bar_type.grid(row = 11, column =2)
	casting_bar_type.insert(0, '4-sided')

	casting_temp_label = Label(cathode, text = "Casting Temp (°C)").grid(row = 10, column =0)
	casting_temp = Entry(cathode, width = 20)
	casting_temp.grid(row = 11, column =0)
	cursor.execute("Select casting_temp from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['casting_temp'] is not None:
			casting_temp.insert(0, result['casting_temp'])
	casting_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	estimate_cathode_thickness_label = Label(cathode, text = "Estimated Thickness (um)").grid(row = 4, column =7)
	estimate_cathode_thickness = Entry(cathode, width = 20)
	estimate_cathode_thickness.grid(row = 5, column =7)

	num_rolling_layers_label = Label(cathode, text = "Number of Rolling Layers").grid(row = 10, column =4)
	num_rolling_layers = Entry(cathode, width = 20)
	num_rolling_layers.grid(row = 11, column =4)
	cursor.execute("Select num_rolling_layers from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['num_rolling_layers'] is not None:
			num_rolling_layers.insert(0, result['num_rolling_layers'])

	roller_label = Label(cathode, text = "Roller").grid(row = 10, column =5)
	roller = Entry(cathode, width = 20)
	roller.grid(row = 11, column =5, padx =5)
	cursor.execute("Select roller from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['roller'] is not None:
			roller.insert(0, result['roller'])

	rolling_procedure_label = Label(cathode, text = "Rolling Procedure").grid(row = 10, column =3)
	rolling_procedure = Entry(cathode, width = 20)
	rolling_procedure.grid(row = 11, column =3, padx =5)
	cursor.execute("Select rolling_procedure from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['rolling_procedure'] is not None:
			rolling_procedure.insert(0, result['rolling_procedure'])

	LNTO_coating = IntVar()
	LNTO_coating.set(0)
	LNTO_coating_label = Label(cathode, text = "LNTO Coating? (Y/N)").grid(row = 16, column =3)
	LNTO_coating_cb = Checkbutton(cathode, variable=LNTO_coating, onvalue=1, offvalue=0)
	LNTO_coating_cb.grid(row = 17, column =3, padx =5)

	LNTO_id_label = Label(cathode, text = "LNTO ID").grid(row = 16, column =4)
	LNTO_id = Entry(cathode, width = 20)
	LNTO_id.grid(row = 17, column =4, padx =5)
	cursor.execute("Select LNTO_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['LNTO_id'] is not None:
			LNTO_id.insert(0, result['LNTO_id'])
	else:
		LNTO_id.insert(0, 'B23')
	# LNTO_id.config(validate="focusout", validatecommand=(reg_id, '%P'), invalidcommand = (inv_id))

	silica_label = Label(cathode, text = "Silica wt_pct").grid(row = 16, column =5)
	silica_wt_pct = Entry(cathode, width = 20)
	silica_wt_pct.grid(row = 17, column =5)

	silica_mass_label = Label(cathode, text = "Silica Mass (g)").grid(row = 16, column =6)
	silica_mass = Entry(cathode, width = 20)
	silica_mass.grid(row = 17, column =6)

	cnt_wt_pct_label = Label(cathode, text = "Carbon Nano Tube wt_pct").grid(row = 16, column =0)
	cnt_wt_pct = Entry(cathode, width = 20)
	cnt_wt_pct.grid(row = 17, column =0)
	cnt_wt_pct.insert(0, 0.06)

	cnt_mass_label = Label(cathode, text = "Carbon Nano Tube (g)").grid(row = 16, column =1)
	cnt_mass = Entry(cathode, width = 20)
	cnt_mass.grid(row = 17, column =1)
	cursor.execute("Select cnt_mass from cells.cathode where cathode_type like 'Sulfide' order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['cnt_mass'] is not None:
			cnt_mass.insert(0, result['cnt_mass'])
	else:
		cnt_mass.insert(0, 0)

	packing_density_label = Label(cathode, text = "Packing Density").grid(row = 16, column =2)
	packing_density = Entry(cathode, width = 20)
	packing_density.grid(row = 17, column =2)
	packing_density.insert(0, 0.85)

	samples_label = Label(cathode, text = "Samples per Batch").grid(row = 10, column =6)
	samples = Entry(cathode, width = 20)
	samples.grid(row = 11, column =6, padx = 5)

	batch_label = Label(cathode, text = "Batch Size").grid(row = 18, column =0)
	batch = Entry(cathode, width = 20)
	batch.grid(row = 19, column =0, padx = 5)

	comments_label = Label(cathode, text = "Comments").grid(row = 18, column =4)
	comments = Entry(cathode, width = 60)
	comments.grid(row = 19, column =3, columnspan = 3)

	initial_label = Label(cathode, text = "Enter Initials Here").grid(row= 20, column = 2)
	initial = Entry(cathode, width = 20)
	initial.grid(row = 21, column =2)

	button_submit = Button(cathode, text = "Upload Data", command=lambda: submit_sulfide_cathode(code)).grid(row = 21, column = 3, pady = 5)

def Baseline_Cathode_Click(code):
	global cathode_id
	global description
	global date_made
	global particle_coating
	global casting_coating
	global active_material_vol_percent
	global active_material_type
	global active_material_mass
	global packing_density
	global LLZO_id
	global LLZO_mass
	global Glass_id
	global Glass_mass
	global dispersant_type
	global dispersant_mass
	global polymer_type
	global polymer_mass
	global plasticizer_type
	global plasticizer_mass
	global solvent1_type
	global solvent1_mass
	global solvent2_type
	global solvent2_mass
	global balls_small_mass
	global balls_large_mass
	global composite_density
	global milling_time
	global milling_speed
	global substrate_id
	global casting_temp
	global casting_bar_setting
	global casting_bar_type
	global estimate_cathode_thickness
	global num_rolling_layers
	global roller
	global rolling_procedure
	global bisque_heating_temp
	global bisque_heating_time
	global sinter1_date
	global sinter1_heating_temp
	global sinter1_heating_time
	global sinter2_date
	global sinter2_heating_temp
	global sinter2_heating_time
	global samples
	global mix_speed
	global mix_time
	global mix_rounds
	global comments
	global initial

	cathode = Toplevel()
	cathode.title("Enter Baseline data here")
	# cathode.iconbitmap(r'JES_logo.ico')
	reg_date=cathode.register(callback_date)
	reg_int=cathode.register(callback_int)
	reg_float=cathode.register(callback_float)
	reg_time = cathode.register(callback_time)
	inv_date = cathode.register(invalid_date)
	inv_int = cathode.register(invalid_int)
	inv_float = cathode.register(invalid_float)
	inv_time = cathode.register(invalid_time)

	# Connect to DB to pull most recent entry values
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	# User input boxes

	cathode_id_label = Label(cathode, text = "Cathode ID").grid(row = 0, column =0)
	cathode_id = Entry(cathode, width = 20)
	cathode_id.grid(row = 1, column =0)
	cathode_id.insert(0, 'B23')

	description_label = Label(cathode, text = "Description").grid(row = 0, column =8)
	description = Entry(cathode, width = 20)
	description.grid(row = 1, column =8)

	date_made_label = Label(cathode, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =1)
	date_made = Entry(cathode, width = 20)
	date_made.grid(row = 1, column =1)
	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	particle_coating_options = ['None', 'LipSi', 'LNTO', 'NTiO', 'LDP', 'LLZO sol gel', 'LBCSO', 'LBCO', 'LBO']

	particle_coating_label = Label(cathode, text = "Particle Coating").grid(row = 0, column =2)
	particle_coating = ttk.Combobox(cathode, value = particle_coating_options, width = 20)
	particle_coating.current(0)
	particle_coating.grid(row = 1, column =2)

	casting_coating_options = ['None', 'LipSi', 'LNTO', 'NTiO', 'LDP', 'LLZO sol gel', 'LBCSO', 'LBCO', 'LBO']

	casting_coating_label = Label(cathode, text = "Casting Coating").grid(row = 0, column =3)
	casting_coating = ttk.Combobox(cathode, value = casting_coating_options, width = 20)
	casting_coating.current(0)
	casting_coating.grid(row = 1, column =3)

	active_material_vol_percent_label = Label(cathode, text = "Active Material vol%").grid(row = 0, column =4)
	active_material_vol_percent = Entry(cathode, width = 20)
	cursor.execute("Select active_material_vol from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['active_material_vol'] is not None:
			active_material_vol_percent.insert(0, result['active_material_vol'])
	else:
		active_material_vol_percent.insert(0, '')
	active_material_vol_percent.grid(row = 1, column =4)

	active_material_type_options = ['Agl 622 NMC', 'Agl 811 NMC', 'SC 622 NMC', 'SC 631 NMC', 'SC 955 NMC', 'LiNbO coated 811 NMC (store bought)']

	active_material_type_label = Label(cathode, text = "Active Material Type").grid(row = 0, column =5)
	active_material_type = ttk.Combobox(cathode, value = active_material_type_options, width = 20)
	active_material_type.current(0)
	active_material_type.grid(row = 1, column =5)

	active_material_mass_label = Label(cathode, text = "Active Material Mass (g)").grid(row = 0, column =6)
	active_material_mass = Entry(cathode, width = 20)
	active_material_mass.grid(row = 1, column =6)
	cursor.execute("Select active_material_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['active_material_mass'] is not None:
			active_material_mass.insert(0, result['active_material_mass'])
	active_material_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	packing_density_label = Label(cathode, text = "Packing Density").grid(row = 0, column =7)
	packing_density = Entry(cathode, width = 20)
	packing_density.grid(row = 1, column =7, padx = 5)
	packing_density.insert(0, 0.85)

	Glass_id_label = Label(cathode, text = "Glass ID").grid(row = 4, column =0)
	Glass_id = Entry(cathode, width = 20)
	cursor.execute("Select Glass_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['Glass_id'] is not None:
			Glass_id.insert(0, result['Glass_id'])
	Glass_id.grid(row = 5, column =0)

	Glass_mass_label = Label(cathode, text = "Glass Mass (g)").grid(row = 4, column =1)
	Glass_mass = Entry(cathode, width = 20)
	Glass_mass.grid(row = 5, column =1)
	cursor.execute("Select Glass_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['Glass_mass'] is not None:
			Glass_mass.insert(0, result['Glass_mass'])
	Glass_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	dispersant_type_label = Label(cathode, text = "Dispersant Type").grid(row = 4, column =2)
	dispersant_type = Entry(cathode, width = 20)
	dispersant_type.insert(0, 'Fish Oil')
	dispersant_type.grid(row = 5, column =2)

	dispersant_mass_label = Label(cathode, text = "Dispersant Mass (g)").grid(row = 4, column =3)
	dispersant_mass = Entry(cathode, width = 20)
	dispersant_mass.grid(row = 5, column =3)
	cursor.execute("Select dispersant_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['dispersant_mass'] is not None:
			dispersant_mass.insert(0, result['dispersant_mass'])
	dispersant_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	polymer_type_label = Label(cathode, text = "Polymer Type").grid(row = 4, column =4)
	polymer_type = Entry(cathode, width = 20)
	polymer_type.insert(0, 'PVB')
	polymer_type.grid(row = 5, column =4)

	polymer_mass_label = Label(cathode, text = "Polymer Mass (g)").grid(row = 4, column =5)
	polymer_mass = Entry(cathode, width = 20)
	polymer_mass.grid(row = 5, column =5)
	cursor.execute("Select polymer_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['polymer_mass'] is not None:
			polymer_mass.insert(0, result['polymer_mass'])
	polymer_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	plasticizer_type_label = Label(cathode, text = "Plasticizer Type").grid(row = 4, column =6)
	plasticizer_type = Entry(cathode, width = 20)
	plasticizer_type.insert(0, 'BBT')
	plasticizer_type.grid(row = 5, column =6)

	plasticizer_mass_label = Label(cathode, text = "Plasticizer Mass (g)").grid(row = 4, column =7)
	plasticizer_mass = Entry(cathode, width = 20)
	plasticizer_mass.grid(row = 5, column =7, padx =5)
	cursor.execute("Select plasticizer_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['plasticizer_mass'] is not None:
			plasticizer_mass.insert(0, result['plasticizer_mass'])
	plasticizer_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	LLZO_mass_label = Label(cathode, text = "LLZO Mass (g)").grid(row = 4, column =8)
	LLZO_mass = Entry(cathode, width = 20)
	LLZO_mass.grid(row = 5, column =8)
	cursor.execute("Select LLZO_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['LLZO_mass'] is not None:
			LLZO_mass.insert(0, result['LLZO_mass'])

	LLZO_id_label = Label(cathode, text = "LLZO ID").grid(row = 4, column =9)
	LLZO_id = Entry(cathode, width = 20)
	cursor.execute("Select LLZO_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['LLZO_id'] is not None:
			LLZO_id.insert(0, result['LLZO_id'])
	else:
		LLZO_id.insert(0, 'B23')
	LLZO_id.grid(row = 5, column =9)

	solvent1_type_label = Label(cathode, text = "Solvent 1 Type").grid(row = 7, column =1)
	solvent1_type = Entry(cathode, width = 20)
	solvent1_type.insert(0, 'Ethanol')
	solvent1_type.grid(row = 8, column =1)

	solvent1_mass_label = Label(cathode, text = "Solvent 1 Mass (g)").grid(row = 7, column =2)
	solvent1_mass = Entry(cathode, width = 20)
	solvent1_mass.grid(row = 8, column =2)
	cursor.execute("Select solvent1_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['solvent1_mass'] is not None:
			solvent1_mass.insert(0, result['solvent1_mass'])
	solvent1_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	solvent2_type_label = Label(cathode, text = "Solvent 2 Type").grid(row = 7, column =3)
	solvent2_type = Entry(cathode, width = 20)
	solvent2_type.insert(0, 'Xylene')
	solvent2_type.grid(row = 8, column =3)

	solvent2_mass_label = Label(cathode, text = "Solvent 2 Mass (g)").grid(row = 7, column =4)
	solvent2_mass = Entry(cathode, width = 20)
	solvent2_mass.grid(row = 8, column =4)
	cursor.execute("Select solvent2_mass from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['solvent2_mass'] is not None:
			solvent2_mass.insert(0, result['solvent2_mass'])
	solvent2_mass.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	composite_density_label = Label(cathode, text = "Composite Density").grid(row = 7, column =5)
	composite_density = Entry(cathode, width = 20)
	composite_density.grid(row = 8, column =5)
	cursor.execute("Select composite_density from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['composite_density'] is not None:
			composite_density.insert(0, result['composite_density'])
	composite_density.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	substrate_id_label = Label(cathode, text = "Substrate ID").grid(row = 7, column =6)
	substrate_id = Entry(cathode, width = 20)
	cursor.execute("Select substrate_id from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['substrate_id'] is not None:
			substrate_id.insert(0, result['substrate_id'])
	substrate_id.grid(row = 8, column =6)

	if code == 'mill':
		milling_time_label = Label(cathode, text = "Milling Time (HH:MM:SS)").grid(row = 10, column =0)
		milling_time = Entry(cathode, width = 20)
		milling_time.grid(row = 11, column =0)
		milling_time.insert(0, '01:00:00')

		milling_speed_label = Label(cathode, text = "Milling Speed (rpm)").grid(row = 10, column =1)
		milling_speed = Entry(cathode, width = 20)
		milling_speed.grid(row = 11, column =1)
		milling_speed.insert(0, 400)

		balls_small_mass_label = Label(cathode, text = "Small Balls Mass (g)").grid(row = 10, column =2)
		balls_small_mass = Entry(cathode, width = 20)
		balls_small_mass.grid(row = 11, column =2)
		balls_small_mass.insert(0, 16)

		balls_large_mass_label = Label(cathode, text = "Large Balls Mass (g)").grid(row = 10, column =3)
		balls_large_mass = Entry(cathode, width = 20)
		balls_large_mass.grid(row = 11, column =3)
		balls_large_mass.insert(0, 14)

	elif code == 'mix':
		mix_time_label = Label(cathode, text = "Speed Mix Time (HH:MM:SS)").grid(row = 10, column =0)
		mix_time = Entry(cathode, width = 20)
		mix_time.grid(row = 11, column =0)
		mix_time.insert(0, '00:05:00')

		mix_speed_label = Label(cathode, text = "Speed Mix (rpm)").grid(row = 10, column =1)
		mix_speed = Entry(cathode, width = 20)
		mix_speed.grid(row = 11, column =1)
		mix_speed.insert(0, 1200)

		mix_rounds_label = Label(cathode, text = "Speed Mix Rounds").grid(row = 10, column =2)
		mix_rounds = Entry(cathode, width = 20)
		mix_rounds.grid(row = 11, column =2)
		mix_rounds.insert(0, 3)

	# viscosity_label = Label(cathode, text = "Viscosity").grid(row = 10, column =3)
	# viscosity = Entry(cathode, width = 20)
	# viscosity.grid(row = 11, column =3, padx =5)
	# cursor.execute("Select viscosity from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['viscosity'] is not None:
	# 		viscosity.insert(0, result['viscosity'])
	# viscosity.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	casting_temp_label = Label(cathode, text = "Casting Temp (°C)").grid(row = 10, column =5)
	casting_temp = Entry(cathode, width = 20)
	casting_temp.grid(row = 11, column =5)
	# cursor.execute("Select casting_temp from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['casting_temp'] is not None:
	# 		casting_temp.insert(0, result['casting_temp'])
	casting_temp.insert(0, 25)
	casting_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	casting_bar_setting_label = Label(cathode, text = "Casting Bar Setting (um)").grid(row = 10, column =6)
	casting_bar_setting = Entry(cathode, width = 20)
	casting_bar_setting.grid(row = 11, column =6)
	# cursor.execute("Select casting_bar_setting from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['casting_bar_setting'] is not None:
	# 		casting_bar_setting.insert(0, result['casting_bar_setting'])
	casting_bar_setting.insert(0, 50)

	casting_bar_type_label = Label(cathode, text = "Casting Bar Type").grid(row = 10, column =4)
	casting_bar_type = Entry(cathode, width = 20)
	casting_bar_type.grid(row = 11, column =4)
	# cursor.execute("Select casting_bar_type from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['casting_bar_type'] is not None:
	# 		casting_bar_type.insert(0, result['casting_bar_type'])
	casting_bar_type.insert(0, '4-sided')

	estimate_cathode_thickness_label = Label(cathode, text = "Estimated Thickness (um)").grid(row = 10, column =7)
	estimate_cathode_thickness = Entry(cathode, width = 20)
	estimate_cathode_thickness.grid(row = 11, column =7)

	num_rolling_layers_label = Label(cathode, text = "Number of Rolling Layers").grid(row = 13, column =1)
	num_rolling_layers = Entry(cathode, width = 20)
	num_rolling_layers.grid(row = 14, column =1)
	cursor.execute("Select num_rolling_layers from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['num_rolling_layers'] is not None:
			num_rolling_layers.insert(0, result['num_rolling_layers'])

	roller_label = Label(cathode, text = "Roller").grid(row = 13, column =2)
	roller = Entry(cathode, width = 20)
	roller.grid(row = 14, column =2, padx =5)
	cursor.execute("Select roller from cells.cathode order by date_made desc limit 1")
	result = cursor.fetchone()
	if result is not None:
		if result['roller'] is not None:
			roller.insert(0, result['roller'])

	rolling_procedure_label = Label(cathode, text = "Rolling Procedure").grid(row = 13, column =0)
	rolling_procedure = Entry(cathode, width = 20)
	rolling_procedure.grid(row = 14, column =0, padx =5)
	# cursor.execute("Select rolling_procedure from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['rolling_procedure'] is not None:
	# 		rolling_procedure.insert(0, result['rolling_procedure'])
	rolling_procedure.insert(0, '3x5, 3x3, 3x0')

	bisque_heating_temp_label = Label(cathode, text = "Bisque Heating Temp (°C)").grid(row = 13, column =4)
	bisque_heating_temp = Entry(cathode, width = 20)
	bisque_heating_temp.grid(row = 14, column =4, padx =5)
	# cursor.execute("Select bisque_heating_temp from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['bisque_heating_temp'] is not None:
	# 		bisque_heating_temp.insert(0, result['bisque_heating_temp'])
	bisque_heating_temp.insert(0, 400)
	bisque_heating_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	bisque_heating_time_label = Label(cathode, text = "Bisque Heating Time (HH:MM:SS)").grid(row = 13, column =3)
	bisque_heating_time = Entry(cathode, width = 20)
	bisque_heating_time.grid(row = 14, column =3, padx =5)
	# cursor.execute("Select bisque_heating_time from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['bisque_heating_time'] is not None:
	# 		bisque_heating_time.insert(0, result['bisque_heating_time'])
	bisque_heating_time.insert(0, '06:00:00')
	bisque_heating_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	sinter1_date_label = Label(cathode, text = "Sinter 1 Date (YYY-MM-DD)").grid(row = 13, column =5)
	sinter1_date = Entry(cathode, width = 20)
	sinter1_date.grid(row = 14, column =5, padx =5)
	sinter1_date.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))

	sinter1_heating_temp_label = Label(cathode, text = "Sinter 1 Heating Temp (°C)").grid(row = 13, column =6)
	sinter1_heating_temp = Entry(cathode, width = 20)
	sinter1_heating_temp.grid(row = 14, column =6, padx =5)
	# cursor.execute("Select sinter_heating_temp from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['sinter_heating_temp'] is not None:
	# 		sinter_heating_temp.insert(0, result['sinter_heating_temp'])
	sinter1_heating_temp.insert(0, 550)
	sinter1_heating_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	sinter1_heating_time_label = Label(cathode, text = "Sinter 1 Heating Time (HH:MM:SS)").grid(row = 13, column =7)
	sinter1_heating_time = Entry(cathode, width = 20)
	sinter1_heating_time.grid(row = 14, column =7, padx =5)
	# cursor.execute("Select sinter_heating_time from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['sinter_heating_time'] is not None:
	# 		sinter_heating_time.insert(0, result['sinter_heating_time'])
	sinter1_heating_time.insert(0, '00:05:00')
	sinter1_heating_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	sinter2_date_label = Label(cathode, text = "Sinter 2 Date (YYY-MM-DD)").grid(row = 16, column =0)
	sinter2_date = Entry(cathode, width = 20)
	sinter2_date.grid(row = 17, column =0, padx =5)

	sinter2_heating_temp_label = Label(cathode, text = "Sinter 2 Heating Temp (°C)").grid(row = 16, column =1)
	sinter2_heating_temp = Entry(cathode, width = 20)
	sinter2_heating_temp.grid(row = 17, column =1, padx =5)
	# cursor.execute("Select sinter_heating_temp from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['sinter_heating_temp'] is not None:
	# 		sinter_heating_temp.insert(0, result['sinter_heating_temp'])
	sinter2_heating_temp.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	sinter2_heating_time_label = Label(cathode, text = "Sinter 2 Heating Time (HH:MM:SS)").grid(row = 16, column =2)
	sinter2_heating_time = Entry(cathode, width = 20)
	sinter2_heating_time.grid(row = 17, column = 2, padx =5)
	# cursor.execute("Select sinter_heating_time from cells.cathode order by date_made desc limit 1")
	# result = cursor.fetchone()
	# if result is not None:
	# 	if result['sinter_heating_time'] is not None:
	# 		sinter_heating_time.insert(0, result['sinter_heating_time'])
	sinter2_heating_time.config(validate="focusout", validatecommand=(reg_time, '%P'), invalidcommand = (inv_time))

	samples_label = Label(cathode, text = "Samples per Batch").grid(row = 16, column =3)
	samples = Entry(cathode, width = 20)
	samples.grid(row = 17, column =3, padx = 5)

	comments_label = Label(cathode, text = "Comments").grid(row = 16, column =4)
	comments = Entry(cathode, width = 40)
	comments.grid(row = 17, column =4, columnspan = 2)

	initial_label = Label(cathode, text = "Enter Initials Here").grid(row= 18, column = 2)
	initial = Entry(cathode, width = 20)
	initial.grid(row = 19, column =2)

	button_submit = Button(cathode, text = "Upload Data", command=lambda: submit_baseline_cathode(code)).grid(row = 19, column = 3, pady = 5)
		
	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Mix_Click(code):
	mix = Toplevel()
	mix.title("Cathode Batch Type")
	mix.geometry("300x200")

	cathode_label = Label(mix, text = "Select Cathode Batch Type Here:", font = 'bold').place(relx=0.5, rely=0.3, anchor=CENTER)
	
	if code == 'baseline':
		mixb = Button(mix, text = "Speed Mix", command= lambda: Baseline_Cathode_Click('mix')).place(relx = 0.3, rely = 0.5, anchor= CENTER)
		mill = Button(mix, text = "Reverse Mill ", command= lambda: Baseline_Cathode_Click('mill')).place(relx = 0.7, rely = 0.5, anchor= CENTER)
	elif code == 'sulfide':
		mixb = Button(mix, text = "Speed Mix", command= lambda: Sulfide_Cathode_Click('mix')).place(relx = 0.3, rely = 0.5, anchor= CENTER)
		mill = Button(mix, text = "Reverse Mill ", command= lambda: Sulfide_Cathode_Click('mill')).place(relx = 0.7, rely = 0.5, anchor= CENTER)

def Cathode_Click():
	cathode = Toplevel()
	cathode.title("Cathode Batch Type")
	cathode.geometry("300x200")

	cathode_label = Label(cathode, text = "Select Cathode Batch Type Here:", font = 'bold').place(relx=0.5, rely=0.3, anchor=CENTER)
	baseline = Button(cathode, text = "Baseline Cathode", command= lambda: Mix_Click('baseline')).place(relx = 0.3, rely = 0.5, anchor= CENTER)
	sulfide = Button(cathode, text = "Sulfide Cathode", command= lambda: Mix_Click('sulfide')).place(relx = 0.7, rely = 0.5, anchor= CENTER)

def EIS_Click():
	global sample_id
	global date_tested
	global location
	global impedance
	global thickness
	global area
	global conductivity
	global initial
	global comments
	global contact

	eis = Toplevel()
	eis.title("Enter EIS Testing data here")
	# eis.iconbitmap(r'JES_logo.ico')
	reg_date=eis.register(callback_date)
	reg_int=eis.register(callback_int)
	reg_float=eis.register(callback_float)
	reg_time = eis.register(callback_time)
	inv_date = eis.register(invalid_date)
	inv_int = eis.register(invalid_int)
	inv_float = eis.register(invalid_float)
	inv_time = eis.register(invalid_time)

	# User input box
	sample_id_label = Label(eis, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(eis, width = 15)
	sample_id.grid(row = 1, column =0, padx =5)

	date_tested_label = Label(eis, text = "Date Tested").grid(row = 0, column =1)
	date_tested = Entry(eis, width = 15)
	date_tested.grid(row = 1, column =1, padx = 5)
	date_tested.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_tested.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	here_label = Label(eis, text = "Enter: ").grid(row = 1, column =2)

	impedance_label = Label(eis, text = "Impedance Z (ohms)").grid(row = 0, column =3)
	impedance = Entry(eis, width = 15)
	impedance.grid(row = 1, column =3, padx =5)
	impedance.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	thickness_label = Label(eis, text = "Layer Thickness d (um)").grid(row = 0, column =4)
	thickness = Entry(eis, width =15)
	thickness.grid(row = 1, column =4, padx =5)
	thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	area_label = Label(eis, text = "Au bar X-sect area (cm2)").grid(row = 0, column =5)
	area = Entry(eis, width = 15)
	area.grid(row = 1, column =5, padx =5)
	area.insert(0, 0.08)
	area.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	or_label = Label(eis, text = "Or enter:").grid(row = 1, column =6, padx =5)

	conductivity_label = Label(eis, text = "Conductivity (S/cm)").grid(row = 0, column =7)
	conductivity = Entry(eis, width = 15)
	conductivity.grid(row = 1, column =7, padx =5)
	conductivity.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	contact_options = ['Select', 'Au', 'Li']

	contact_label = Label(eis, text = "Contact Material").grid(row = 0, column =8)
	contact = ttk.Combobox(eis, value = contact_options)
	contact.current(0)
	contact.grid(row = 1, column =8, padx = 5)

	comments_label = Label(eis, text = "Comments").grid(row = 0, column =9)
	comments = Entry(eis, width = 15)
	comments.grid(row = 1, column =9, padx=5)

	initial_label = Label(eis, text = "Enter Initials Here").grid(row= 2, column = 4)
	initial = Entry(eis, width = 15)
	initial.grid(row = 3, column =4, padx =5)

	button_submit = Button(eis, text = "Upload Data", command=submit_eis).grid(row = 3, column = 5)

def E_Cond_Click():
	global sample_id
	global date_tested
	global voltage
	global current
	global thickness
	global area
	global conductivity
	global comments
	global initial

	e_cond = Toplevel()
	e_cond.title("Enter E Conductivity data here")
	# eis.iconbitmap(r'JES_logo.ico')
	reg_date=e_cond.register(callback_date)
	reg_int=e_cond.register(callback_int)
	reg_float=e_cond.register(callback_float)
	reg_time = e_cond.register(callback_time)
	inv_date = e_cond.register(invalid_date)
	inv_int = e_cond.register(invalid_int)
	inv_float = e_cond.register(invalid_float)
	inv_time = e_cond.register(invalid_time)

	# User input box
	sample_id_label = Label(e_cond, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(e_cond, width = 15)
	sample_id.grid(row = 1, column =0, padx =5)

	date_tested_label = Label(e_cond, text = "Date Tested").grid(row = 0, column =1)
	date_tested = Entry(e_cond, width = 15)
	date_tested.grid(row = 1, column =1, padx = 5)
	date_tested.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_tested.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	here_label = Label(e_cond, text = "Enter: ").grid(row = 1, column =2)

	voltage_label = Label(e_cond, text = "Voltage (V)").grid(row = 0, column =3)
	voltage = Entry(e_cond, width = 15)
	voltage.grid(row = 1, column =3, padx =5)
	voltage.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	current_label = Label(e_cond, text = "Current (amps)").grid(row = 0, column =4)
	current = Entry(e_cond, width = 15)
	current.grid(row = 1, column =4, padx =5)
	current.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	thickness_label = Label(e_cond, text = "Layer Thickness d (um)").grid(row = 0, column =5)
	thickness = Entry(e_cond, width =15)
	thickness.grid(row = 1, column =5, padx =5)
	thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	area_label = Label(e_cond, text = "Au bar X-sect area (cm2)").grid(row = 0, column =6)
	area = Entry(e_cond, width = 15)
	area.grid(row = 1, column =6, padx =5)
	area.insert(0, 0.08)
	area.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	or_label = Label(e_cond, text = "Or enter:").grid(row = 1, column =7, padx =5)

	conductivity_label = Label(e_cond, text = "Conductivity (S/cm)").grid(row = 0, column =8)
	conductivity = Entry(e_cond, width = 15)
	conductivity.grid(row = 1, column =8, padx =5)
	conductivity.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(e_cond, text = "Comments").grid(row = 0, column =9)
	comments = Entry(e_cond, width = 15)
	comments.grid(row = 1, column =9, padx=5)

	initial_label = Label(e_cond, text = "Enter Initials Here").grid(row= 2, column = 4)
	initial = Entry(e_cond, width = 15)
	initial.grid(row = 3, column =4, padx =5)

	button_submit = Button(e_cond, text = "Upload Data", command=submit_Econd).grid(row = 3, column = 5)

def Galvo_Click():
	global sample_id
	global date_tested
	global current
	global area
	global num_cycles
	global comments
	global initial

	galvo = Toplevel()
	galvo.title("Enter Galvanostatic Testing data here")
	# galvo.iconbitmap(r'JES_logo.ico')
	reg_date=galvo.register(callback_date)
	reg_int=galvo.register(callback_int)
	reg_float=galvo.register(callback_float)
	reg_time = galvo.register(callback_time)
	inv_date = galvo.register(invalid_date)
	inv_int = galvo.register(invalid_int)
	inv_float = galvo.register(invalid_float)
	inv_time = galvo.register(invalid_time)

	# User input box
	sample_id_label = Label(galvo, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(galvo, width = 15)
	sample_id.grid(row = 1, column =0, padx =5)

	date_tested_label = Label(galvo, text = "Date Tested").grid(row = 0, column =1)
	date_tested = Entry(galvo, width = 15)
	date_tested.grid(row = 1, column =1, padx = 5)
	date_tested.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date_tested.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	current_label = Label(galvo, text = "Current (amps)").grid(row = 0, column =4)
	current = Entry(galvo, width = 15)
	current.grid(row = 1, column =4, padx =5)
	current.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	area_label = Label(galvo, text = "Area (cm2)").grid(row = 0, column =6)
	area = Entry(galvo, width = 15)
	area.grid(row = 1, column =6, padx =5)
	area.insert(0, 0.08)
	area.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	num_cycles_label = Label(galvo, text = "# Cycles").grid(row = 0, column =8)
	num_cycles = Entry(galvo, width = 15)
	num_cycles.grid(row = 1, column =8, padx =5)
	num_cycles.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

	comments_label = Label(galvo, text = "Comments").grid(row = 0, column =9)
	comments = Entry(galvo, width = 15)
	comments.grid(row = 1, column =9, padx=5)

	initial_label = Label(galvo, text = "Enter Initials Here").grid(row= 2, column = 4)
	initial = Entry(galvo, width = 15)
	initial.grid(row = 3, column =4, padx =5)

	button_submit = Button(galvo, text = "Upload Data", command=submit_galvo).grid(row = 3, column = 5)

def Cond_Click():
	cond = Toplevel()
	cond.title("E-Chem Test Type")
	cond.geometry("300x200")

	cond_label = Label(cond, text = "Select E-Chem Test Type Here:", font = 'bold').place(relx=0.5, rely=0.2, anchor=CENTER)
	e = Button(cond, text = "Electronic Conductivity", command= E_Cond_Click).place(relx = 0.5, rely = 0.4, anchor= CENTER)
	i = Button(cond, text = "Ionic Conductivity (EIS)", command=EIS_Click).place(relx = 0.5, rely = 0.6, anchor= CENTER)
	h = Button(cond, text = "Galvanostatic Cycling", command=Galvo_Click).place(relx = 0.5, rely = 0.8, anchor= CENTER)

def AC_Click():
	global sample_id
	global start
	global end
	global material
	global anode_coating_batch
	global coated_anode
	global comments
	global initial

	ac = Toplevel()
	ac.title("Enter anode data here")
	# anode.iconbitmap(r'JES_logo.ico')

	# User input box
	sample_id_label = Label(ac, text = "Samples").grid(row = 0, column =0)
	sample_id = Entry(ac, width = 15)
	sample_id.grid(row = 1, column =0, padx = 5)

	start_label = Label(ac, text = "Starting Index").grid(row = 0, column =1)
	start = Entry(ac, width = 15)
	start.grid(row = 1, column =1, padx =5)

	end_label = Label(ac, text = "Last Index").grid(row = 0, column =2)
	end = Entry(ac, width = 15)
	end.grid(row = 1, column =2, padx =5)

	material_options = ['LLZO', 'LNTO', 'LiF', 'LiTSFI', 'MFSA', 'H3PO4', 'LBCSO']

	material_label  = Label(ac, text = "Material").grid(row = 0, column =3)
	material = ttk.Combobox(ac, value = material_options, width = 15)
	material.current(0)
	material.grid(row = 1, column = 3, padx =5)

	anode_coating_batch_label  = Label(ac, text = "Batch").grid(row = 0, column =5)
	anode_coating_batch = Entry(ac, width = 15)
	anode_coating_batch.grid(row = 1, column = 5, padx =5)

	coated_anode = IntVar()
	coated_anode.set(0)
	coated_anode_label = Label(ac, text = "Coated Anode (Li)? (Y/N)").grid(row =0, column =6)
	coated_anode_cb = Checkbutton(ac, variable=coated_anode, onvalue=1, offvalue=0)
	coated_anode_cb.grid(row = 1, column =6, padx = 5)

	comments_label = Label(ac, text = "Comments").grid(row = 0, column =8)
	comments = Entry(ac)
	comments.grid(row = 1, column =8, padx =5)

	initial_label = Label(ac, text = "Enter Initials Here").grid(row= 2, column = 2)
	initial = Entry(ac, width = 15)
	initial.grid(row = 3, column =2, padx =5)

	button_submit = Button(ac, text = "Upload Data", command=submit_ac).grid(row = 3, column = 3)	

# def B2S3_Click():
# 	global sample_id
# 	global date_made
# 	global B_type
# 	global preparation
# 	global temp_profile
# 	global time_profile 
# 	global comments
# 	global initial

# 	b2s3 = Toplevel()
# 	b2s3.title("Enter B2S3 data here")
# 	# b2s3.iconbitmap(r'JES_logo.ico')
# 	reg_date=b2s3.register(callback_date)
# 	reg_int=b2s3.register(callback_int)
# 	reg_float=b2s3.register(callback_float)
# 	inv_date = b2s3.register(invalid_date)
# 	inv_int = b2s3.register(invalid_int)
# 	inv_float = b2s3.register(invalid_float)

# 	# User input box
# 	sample_id_label = Label(b2s3, text = "Sample ID").grid(row = 0, column =0)
# 	sample_id = Entry(b2s3, width = 15)
# 	sample_id.grid(row = 1, column =0, padx = 5)

# 	date_made_label = Label(b2s3, text = "Date Made (YYYY-MM-DD)").grid(row = 0, column =3)
# 	date_made = Entry(b2s3, width =15)
# 	date_made.grid(row = 1, column =3, padx =5)
# 	date_made.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
# 	date_made.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

# 	B_type_options = ['Crystalline', 'Amorphous']
# 	B_type = ttk.Combobox(b2s3, value = B_type_options)
# 	B_type.current(0)
# 	B_type_label = Label(b2s3, text = 'Select the Boron Type').grid(row = 0, column =4)
# 	B_type.grid(row = 1, column = 4, padx =5)

# 	preparation_options = ['GC Crucible', 'Ampule Only']
# 	preparation = ttk.Combobox(b2s3, value = preparation_options)
# 	preparation.current(0)
# 	preparation_label = Label(b2s3, text = "Prep Method").grid(row = 0, column =5)
# 	preparation.grid(row = 1, column =5, padx =5)

# 	temp_profile_label = Label(b2s3, text = "Temp Profile (°C)").grid(row = 0, column =6)
# 	temp_profile = Entry(b2s3)
# 	temp_profile.grid(row = 1, column =6, padx =5)
# 	temp_profile.insert(0, '')

# 	time_profile_label = Label(b2s3, text = "Time Profile").grid(row = 0, column =7)
# 	time_profile = Entry(b2s3)
# 	time_profile.grid(row = 1, column =7, padx =5)
# 	time_profile.insert(0, '')

# 	comments_label = Label(b2s3, text = "Comments").grid(row = 0, column =8)
# 	comments = Entry(b2s3)
# 	comments.grid(row = 1, column =8, padx =5)

# 	initial_label = Label(b2s3, text = "Enter Initials Here").grid(row= 2, column = 3)
# 	initial = Entry(b2s3, width = 15)
# 	initial.grid(row = 3, column =3, padx =5)

# 	button_submit = Button(b2s3, text = "Upload Data", command=submit_b2s3).grid(row = 3, column = 4)	

# def Parylene_Click():
# 	global sample_id
# 	global date_added
# 	global thickness
# 	global base_pressure
# 	global comments
# 	global initial

# 	pary = Toplevel()
# 	pary.title("Enter Parylene Encapsulation Parameters here")
# 	# pary.iconbitmap(r'JES_logo.ico')
# 	reg_date=pary.register(callback_date)
# 	reg_int=pary.register(callback_int)
# 	reg_float=pary.register(callback_float)
# 	reg_time = pary.register(callback_time)
# 	inv_date = pary.register(invalid_date)
# 	inv_int = pary.register(invalid_int)
# 	inv_float = pary.register(invalid_float)
# 	inv_time = pary.register(invalid_time)

# 	# User input box
# 	sample_id_label = Label(pary, text = "Sample ID").grid(row = 0, column =0)
# 	sample_id = Entry(pary, width = 30)
# 	sample_id.grid(row = 1, column =0)

# 	date_added_label = Label(pary, text = "Date Encapsulated").grid(row = 0, column =1)
# 	date_added = Entry(pary)
# 	date_added.grid(row = 1, column =1)
# 	date_added.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
# 	date_added.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

# 	thickness_label = Label(pary, text = "Parylene Thickness (um)").grid(row = 0, column =2)
# 	thickness = Entry(pary)
# 	thickness.grid(row = 1, column =2)
# 	thickness.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	base_pressure_label = Label(pary, text = "Base Pressure").grid(row = 0, column =3)
# 	base_pressure = Entry(pary)
# 	base_pressure.grid(row = 1, column =3)
# 	base_pressure.config(validate="focusout", validatecommand=(reg_float, '%P'), invalidcommand = (inv_float))

# 	comments_label = Label(pary, text = "Comments").grid(row = 0, column =4)
# 	comments = Entry(pary)
# 	comments.grid(row = 1, column =4)

# 	initial_label = Label(pary, text = "Enter Initials Here").grid(row= 2, column = 2)
# 	initial = Entry(pary)
# 	initial.grid(row = 3, column =2)

# 	button_submit = Button(pary, text = "Upload Data", command=submit_pary).grid(row = 3, column = 3)

def PostA_Click():
	global sample_id
	global cracked
	# global laterite
	# global flaking_peeling
	# global active_area_craters
	global appearance
	global sep_thickness
	global cathode_thickness
	global infiltration_depth
	global reason
	global bubbles
	global seal_ok
	global rxn_ring
	global Li_corrosion
	global Li_plating
	global comments
	global initial

	postA = Toplevel()
	postA.title("Enter Post Post-Analysis data here")
	# postA.iconbitmap(r'JES_logo.ico')

	# User input box
	sample_id_label = Label(postA, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(postA, width = 15)
	sample_id.grid(row = 1, column =0)

	reason_options = ['Select', 'Failure to Reach Voltage', 'Short After Successful Cycling', 'High Impedance', 'Efficiency Loss', 'Initial Leaking', 'Capacity Drop', 'Test Completed Successfully']
	reason = ttk.Combobox(postA, value = reason_options, width = 30)
	reason.current(0)
	reason_label = Label(postA, text = "Reason Cell Failed").grid(row = 0, column =1)
	reason.grid(row = 1, column =1, padx =5)

	sep_thickness_label = Label(postA, text = "Separator Thickness (um)").grid(row = 0, column =2)
	sep_thickness = Entry(postA, width = 15)
	sep_thickness.grid(row = 1, column =2)

	# cathode_broke = IntVar()
	# cathode_broke.set(0)
	# cathode_broke_label = Label(postA, text = "Cathode Broken?").grid(row = 1, column =3)
	# cathode_broke_cb = Checkbutton(postA, variable=cathode_broke, onvalue=1, offvalue=0)
	# cathode_broke_cb.grid(row = 2, column =3)

	cathode_thickness_label = Label(postA, text = "Cathode Thickness (um)").grid(row = 0, column =3)
	cathode_thickness = Entry(postA, width = 15)
	cathode_thickness.grid(row = 1, column =3)

	infiltration_depth_label = Label(postA, text = "Infiltration Depth (um)").grid(row = 0, column =4)
	infiltration_depth = Entry(postA, width = 15)
	infiltration_depth.grid(row = 1, column =4)

	appearance_options = ['Select', 'Fully Amorphous', 'Mostly Amporhous', '50:50', 'Mostly Crystalline', 'Fully Crystalline']
	appearance = ttk.Combobox(postA, value = appearance_options, width = 30)
	appearance.current(0)
	appearance_label = Label(postA, text = "Appearance of Separator").grid(row = 0, column =5)
	appearance.grid(row = 1, column =5, padx =5)

	cracked = IntVar()
	cracked.set(0)
	cracked_label = Label(postA, text = "Cracks?").grid(row = 3, column =0)
	cracked_cb = Checkbutton(postA, variable=cracked, onvalue=1, offvalue=0)
	cracked_cb.grid(row = 4, column =0)

	# active_area_craters = StringVar()
	# active_area_craters.set(False)
	# active_area_craters_label = Label(postA, text = "Active Area Craters?").grid(row = 0, column =5)
	# active_area_craters_cb = Checkbutton(postA, variable=active_area_craters, onvalue=1, offvalue=0)
	# active_area_craters_cb.grid(row = 1, column =5)

	# laterite = StringVar()
	# laterite.set(False)
	# laterite_label = Label(postA, text = "Laterite?").grid(row = 3, column =0)
	# laterite_cb = Checkbutton(postA, variable=laterite, onvalue=1, offvalue=0)
	# laterite_cb.grid(row = 4, column =0)

	# flaking_peeling = StringVar()
	# flaking_peeling.set(False)
	# flaking_peeling_label = Label(postA, text = "Flaking or Peeling?").grid(row = 3, column =1)
	# flaking_peeling_cb = Checkbutton(postA, variable=flaking_peeling, onvalue=1, offvalue=0)
	# flaking_peeling_cb.grid(row = 4, column =1)

	bubbles = IntVar()
	bubbles.set(0)
	bubbles_label = Label(postA, text = "Bubbles under Li?").grid(row = 3, column =1)
	bubbles_cb = Checkbutton(postA, variable=bubbles, onvalue=1, offvalue=0)
	bubbles_cb.grid(row = 4, column =1)

	rxn_ring = IntVar()
	rxn_ring.set(0)
	rxn_ring_label = Label(postA, text = "Reaction Ring?").grid(row = 3, column =2)
	rxn_ring_cb = Checkbutton(postA, variable=rxn_ring, onvalue=1, offvalue=0)
	rxn_ring_cb.grid(row = 4, column =2)

	Li_corrosion = IntVar()
	Li_corrosion.set(0)
	Li_corrosion_label = Label(postA, text = "Li Corrosion?").grid(row = 3, column =3)
	Li_corrosion_cb = Checkbutton(postA, variable=Li_corrosion, onvalue=1, offvalue=0)
	Li_corrosion_cb.grid(row = 4, column =3)

	Li_plating = IntVar()
	Li_plating.set(0)
	Li_plating_label = Label(postA, text = "Li Plating \n around anode?").grid(row = 3, column =4)
	Li_plating_cb = Checkbutton(postA, variable=Li_plating, onvalue=1, offvalue=0)
	Li_plating_cb.grid(row = 4, column =4)

	comments_label = Label(postA, text = "Comments").grid(row = 3, column =5)
	comments = Entry(postA, width =30)
	comments.grid(row = 4, column =5)

	initial_label = Label(postA, text = "Enter Initials Here").grid(row= 5, column = 2)
	initial = Entry(postA)
	initial.grid(row = 6, column =2)

	button_submit = Button(postA, text = "Upload Data", command=submit_postA).grid(row = 6, column = 3)


# Sample Summary Page
def Sample_Summary():
	global label
	# Load sample summary window
		# Get full screen width, height
	summary = Toplevel()
	summary.update_idletasks()
	summary.attributes('-fullscreen', True)
	summary.state('iconic')
	height = summary.winfo_screenheight()
	width = summary.winfo_screenwidth()
	summary.destroy()

		# set to full screen
	summary = Toplevel()
	summary.title("Sample Summary")
	summary.geometry('%dx%d' % (width, height))

	# Connect to DB
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	sample_label = Label(summary, text = "Enter Sample ID here:").grid(row= 0, column = 0)
	sample = Entry(summary)
	sample.grid(row = 0, column =1)

	sample = 'XYA11'

	# Sample Info
		# Info from samples table
	cursor.execute("Select cathode_id, cathode_coating, sample_type, separator_id, anode_type, active_area_size, ifnull(stage_temp, 0) +  ifnull(muffle_furnace_temp, 0) + ifnull(hot_plate_temp, 0) AS cathode_temp, anode_coating_type, coated_anode_directly, comments from cells.samples where sample_id like (%s);", sample)
	result = cursor.fetchone()
	cathode_id = result['cathode_id']
	cathode_coating = result['cathode_coating']
	sample_type = result['sample_type']
	separator_id = result['separator_id']
	anode_type = result['anode_type']
	active_area_size = result['active_area_size']
	cathode_temp = result['cathode_temp']
	comment = result['comments']
	anode_coating = result['anode_coating_type']
	coated_anode = result['coated_anode_directly']

	# Info from cathode table
	cursor.execute("Select casting_coating, particle_coating, active_material_type from cells.cathode where cathode_id like (%s);", cathode_id)
	result = cursor.fetchone()
	cathode_type = result['active_material_type']
	casting_coating = result['casting_coating']
	particle_coating = result['particle_coating']

	# Info from glass table
	cursor.execute("Select glass_type, num_melts from cells.glass where glass_id like (%s);", separator_id)
	result = cursor.fetchone()
	glass_type = result['glass_type']
	num_melts = result['num_melts']

	# Info from testing table

	# Add info to sample summary
	samp_type_label = Label(summary, text = "Sample Type:", anchor="e", width = 20, justify = 'left').grid(row = 2, column = 0)
	samp_type = Label(summary, text = sample_type).grid(row = 2, column =1)

	cathode_label = Label(summary, text = "Cathode Type:", anchor="e", width = 20, justify = 'right').grid(row = 3, column = 0)
	cathode = Label(summary, text = cathode_type).grid(row = 3, column =1)
	cathode_id_label = Label(summary, text = "(" + cathode_id + ")").grid(row =3, column =2)

	particle_coating_label = Label(summary, text = "Cathode Particle Coating:", anchor="e", width = 20, justify = 'right').grid(row = 4, column = 0)
	particle_coating_label = Label(summary, text = cathode_type).grid(row = 4, column =1)

	casting_coating_label = Label(summary, text = "Casting Cathode Coating:", anchor="e", width = 20, justify = 'right').grid(row = 5, column = 0)
	casting_coating_label = Label(summary, text = cathode_type).grid(row = 5, column =1)

	sinter_coating_label = Label(summary, text = "Sintered Cathode Coating:", anchor="e", width = 20, justify = 'right').grid(row = 6, column = 0)
	sinter_coating_label = Label(summary, text = cathode_coating).grid(row = 6, column =1)

	sep_type_label = Label(summary, text = "Glass Type:", anchor="e", width = 20, justify = 'right').grid(row = 7, column = 0)
	sep_type = Label(summary, text = glass_type + ' x' + str(num_melts)).grid(row = 7, column =1)
	sep_id = Label(summary, text = "(" + separator_id + ")").grid(row = 7, column =2)

	anode_type_label = Label(summary, text = "Anode Type:", anchor="e", width = 20, justify = 'right').grid(row = 8, column = 0)
	anode_type_label = Label(summary, text = anode_type).grid(row = 8, column =1)

	active_area_size_label = Label(summary, text = "Active Area Size:", anchor="e", width = 20, justify = 'right').grid(row = 9, column = 0)
	active_area_size_label = Label(summary, text = active_area_size).grid(row = 9, column =1)

	anode_coating_label = Label(summary, text = "Anode Coating:", anchor="e", width = 20, justify = 'right').grid(row= 10, column = 0)
	anode_coating_label = Label(summary, text = anode_coating).grid(row = 10, column =1)
	if coated_anode:
		anode_coating_label = Label(summary, text = '(Coated on anode directly)').grid(row = 10, column =1)
	elif coated_anode is not None:
		anode_coating_label = Label(summary, text = '(Coated on separator)').grid(row = 10, column =1)

	comments_label = Label(summary, text = "Comments:", anchor="e", width = 20, justify = 'right').grid(row= 11, column = 0)
	comments_label = Label(summary, text = comment).grid(row = 11, column =1, columnspan = 3)
	

	# Load all images w matching sample name in path
	path = r'\\nx3100\\Mdrive\\JES\\SharedFiles\\JES Glass Improvement Study\\Glass Characterization\\SEM'
	os.chdir(path)
	names = []
	for file in glob.iglob('**\\' + sample +'*', recursive = True):
		names.append(file)

	images = []

	for name in names:
		# Check if file is .TIF or .JPEG
		try:
			file_type = re.search(r"(\.[A-Z]{3,4})", name).group()
			if file_type in ['.TIF', '.JPEG', '.JPG']:
				images.append(ImageTk.PhotoImage(Image.open(name)))
		except:
			pass

	if len(images) == 0:
		label = Label(summary, text = 'No SEM images').grid(row=1, column=5, rowspan = 20)
	else:
		# Back and Forward buttons
		label = Label(summary, image=images[0])
		label.grid(row=1, column=5, rowspan = 20)

		def forward(img_no, max_img_no):
			global label
			global button_forward
			global button_back

			label.grid_forget() # clear previous image

			label = Label(summary, image=images[img_no-1])
			label.grid(row=1, column=5, rowspan = 20)

			if img_no == max_img_no:
				button_forward = Button(summary, text="Forward", state=DISABLED)
			else:
				button_forward = Button(summary, text="Forward", command=lambda: forward(img_no+1, len(images)))

			button_back = Button(summary, text="Back", command=lambda: back(img_no-1))

			# Placing the button in new grid
			button_back.grid(row=24, column=5)
			button_forward.grid(row=24, column=6)
		 
		 
		def back(img_no):
			global label
			global button_forward
			global button_back

			label.grid_forget()

			label = Label(summary, image=images[img_no - 1])
			label.grid(row=1, column=5, rowspan = 20)

			button_forward = Button(summary, text="Forward", command=lambda: forward(img_no + 1, len(images)))

			if img_no == 1:
				button_back = Button(summary, Text="Back", state=DISABLED)
			else:
				button_back = Button(summary, text="Back", command=lambda: back(img_no - 1))

			label.grid(row=1, column=5, rowspan = 20)
			button_back.grid(row=24, column=5)
			button_forward.grid(row=24, column=6)

		button_back = Button(summary, text="Back", command=back, state=DISABLED)
		button_forward = Button(summary, text="Forward", command=lambda: forward(2,len(images)))

		button_back.grid(row=24, column=5)
		button_forward.grid(row=24, column=6)


	# Load all images w matching sample name in path
	path = r'\\Mims-server2\indexed\ASCIIfiles\\'
	os.chdir(path)
	names = []

	for file in glob.iglob('**\\' + sample +'*', recursive = True):
		names.append(file)

	print(names)

	if len(names) == 0:
		sinter_coating_label = Label(summary, text = "Not Tested", anchor="e", width = 20, justify = 'right').grid(row = 22, column = 0)
	else:
		# Plotting
		fig, ax = plt.subplots()
		ax.plot(testing_data_df['Cyc'], testing_data_df['Cyc'])
		ax.plot(testing_data_df['Cyc'], testing_data_df['Cyc'])

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

	summary.mainloop()

def Pull_Data_Export():
	# Connect to DB
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	if table.get() == 'LLZO':
		tab = 'llzo'
	elif table.get() == 'Li3BO3':
		tab = 'Li3BO3'
	elif table.get() == 'Glass':
		tab = 'glass'
	elif table.get() == 'LNTO':
		tab = 'lnto'
	elif table.get() == 'Substrate':
		tab = 'cathode_substrate'
	elif table.get() == 'Cathode':
		tab = 'cathode'
	elif table.get() == 'Glass Extrusion':
		tab = 'samples'
	elif table.get() == 'Anode':
		tab = 'anode'
	elif table.get() == 'Current Collector':
		tab = 'current_collector'
	elif table.get() == 'Parylene':
		tab = 'parylene'
	elif table.get() == 'EIS Testing':
		tab = 'eis_testing'
	elif table.get() == 'Post Analysis':
		tab = 'post_analysis'
	elif table.get() == 'Post Testing':
		tab = 'post_testing'
	elif table.get() == 'Pre Testing':
		tab = 'pre_testing'
	elif table.get() == 'Logged Test Failures':
		tab = 'log_test_end'
	elif table.get() == 'Maccor Raw Data':
		tab = 'raw_testing_info'
	elif table.get() == 'LIBOSS Glass Properties':
		query =  "SELECT glass_id, glass_type, Li_mol_pct, B_mol_pct, Si_mol_pct, O_mol_pct, C_mol_pct, Cl_mol_pct, F_mol_pct, S_mol_pct, I_mol_pct, N_mol_pct, P_mol_pct, Br_mol_pct, furnace_temp, total_mass, g.comments, c.contact, c.i_conductivity, c.e_conductivity, c.voltage, current_density galvo_current_density, num_cycles galvo_num_cycles FROM cells.glass g left outer join (Select c.sample_id, contact, i_conductivity, e_conductivity, c.voltage, current_density, num_cycles from (SELECT i.sample_id, i.contact, i_conductivity, e_conductivity, voltage FROM eis_testing i left outer join e_conductivity e on i.sample_id = e.sample_id) c left outer join galvo_test gt on c.sample_id = gt.sample_id) c on g.glass_id = c.sample_id where g.glass_type like '%LIBOSS%' order by glass_id desc;"
		cursor.execute(query)
		testing_data_df = pd.DataFrame(cursor.fetchall())

		d = str(datetime.now(tz=None).strftime("%y%m%d"))

		# Create a Pandas Excel writer using XlsxWriter as the engine.
		name = str(d + '_Pulled_' + str(table.get()) + '_Data.xlsx').replace(" ", "_")
		writer = pd.ExcelWriter(name, engine='xlsxwriter')

		testing_data_df.insert(loc = 14, column = 'Li:O', value = list(testing_data_df['Li_mol_pct'] / testing_data_df['O_mol_pct']))
		testing_data_df.insert(loc = 15, column = 'S:O', value = list(testing_data_df['S_mol_pct'] / testing_data_df['O_mol_pct']))

		# Write the dataframe data to XlsxWriter. Turn off the default header and
		# index and skip one row to allow us to insert a user defined header.
		testing_data_df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)

		# Get the xlsxwriter workbook and worksheet objects.
		workbook = writer.book
		worksheet = writer.sheets['Sheet1']

		# Get the dimensions of the dataframe.
		(max_row, max_col) = testing_data_df.shape

		# Create a list of column headers, to use in add_table().
		column_settings = [{'header': column} for column in testing_data_df.columns]

		# Add the Excel table structure. Pandas will add the data.
		worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

		# Make the columns wider for clarity.
		worksheet.set_column(0, max_col - 1, 12)

		# Close the Pandas Excel writer and output the Excel file.
		writer.save()

		# Open the file
		command = "start EXCEL.EXE " + name
		os.system(command)

		return

	elif table.get() == 'LIBOSS Sample Properties':
		query =  "Select s.sample_id, s.glass_type, s.preparation, s.Li_mol_pct, s.B_mol_pct, s.Si_mol_pct, s.O_mol_pct, s.C_mol_pct, s.Cl_mol_pct, s.F_mol_pct, s.S_mol_pct, s.I_mol_pct, s.N_mol_pct, s.P_mol_pct, s.Br_mol_pct, s.contact, s.i_conductivity i_cond_glass, s.e_conductivity e_cond_glass, p.sep_thickness, p.cathode_thickness, p.infiltration_depth_max, p.inflitration_percent_max, current_density galvo_current_density_glass, num_cycles galvo_num_cycles_glass from (select s.sample_id, s.separator_id, s.cathode_id, glass_type, preparation, Li_mol_pct, B_mol_pct, Si_mol_pct, O_mol_pct, C_mol_pct, Cl_mol_pct, F_mol_pct, S_mol_pct, I_mol_pct, N_mol_pct, P_mol_pct, Br_mol_pct, contact, i_conductivity, e_conductivity, current_density, num_cycles from samples s left outer join (Select glass_id, glass_type, preparation, Li_mol_pct, B_mol_pct, Si_mol_pct, O_mol_pct, C_mol_pct, Cl_mol_pct, F_mol_pct, S_mol_pct, I_mol_pct, N_mol_pct, P_mol_pct, Br_mol_pct, contact, i_conductivity, e_conductivity, current_density, num_cycles from glass g left outer join (Select c.sample_id, contact, i_conductivity, e_conductivity, current_density, num_cycles from (SELECT i.sample_id, i.contact, i_conductivity, e_conductivity FROM eis_testing i left outer join e_conductivity e on i.sample_id = e.sample_id) c left outer join galvo_test gt on c.sample_id = gt.sample_id) c on c.sample_id = g.glass_id) gg on s.separator_id = gg.glass_id) s left outer join post_analysis p on s.sample_id = p.sample_id where s.glass_type like '%LIBOSS%';"
		cursor.execute(query)
		testing_data_df = pd.DataFrame(cursor.fetchall())

		d = str(datetime.now(tz=None).strftime("%y%m%d"))
		name = str(d + '_Pulled_' + str(table.get()) + '_Data.xlsx').replace(" ", "_")
		testing_data_df.to_excel(name, index = False)

		# Open the file
		os.system("start EXCEL.EXE {}".format(name))

		return

	elif table.get() == 'Glass Properties':
		query =  "SELECT glass_id, glass_type, preparation, sio2_mass, sio2_wt_pct, li2s_wt_pct, li2s_mass, lii_mass, lii_wt_pct, b2s3_mass, b2s3_wt_pct, Li2B4O7_mass, Li2B4O7_wt_pct, B_wt_pct, B_mass, S_wt_pct, S_mass, sis2_wt_pct, sis2_mass, furnace_temp, furnace_time, liboss_base, sio2_type, total_mass, g.comments, c.contact, c.i_conductivity, c.e_conductivity, c.voltage, current_density galvo_current_density, num_cycles galvo_num_cycles FROM cells.glass g left outer join (Select c.sample_id, contact, i_conductivity, e_conductivity, c.voltage, current_density, num_cycles from (SELECT i.sample_id, i.contact, i_conductivity, e_conductivity, voltage FROM eis_testing i left outer join e_conductivity e on i.sample_id = e.sample_id) c left outer join galvo_test gt on c.sample_id = gt.sample_id) c on g.glass_id = c.sample_id;"
		cursor.execute(query)
		testing_data_df = pd.DataFrame(cursor.fetchall())

		d = str(datetime.now(tz=None).strftime("%y%m%d"))
		name = str(d + '_Pulled_' + str(table.get()) + '_Data.xlsx').replace(" ", "_")
		testing_data_df.to_excel(name, index = False)

		# Open the file
		os.system("start EXCEL.EXE {}".format(name))

		return

	elif table.get() == 'Sample Properties':
		query =  "SELECT s.sample_id, s.glass_type, s.preparation, s.contact, s.i_conductivity i_cond_glass, s.e_conductivity e_cond_glass, p.sep_thickness, p.cathode_thickness, p.inflitration_percent, current_density galvo_current_density_glass, num_cycles galvo_num_cycles_glass from (select s.sample_id, s.separator_id, s.cathode_id, glass_type, preparation, contact, i_conductivity, e_conductivity, current_density, num_cycles from samples s left outer join (Select glass_id, glass_type, preparation, contact, i_conductivity, e_conductivity, current_density, num_cycles from glass g left outer join (Select c.sample_id, contact, i_conductivity, e_conductivity, current_density, num_cycles from (SELECT i.sample_id, i.contact, i_conductivity, e_conductivity FROM eis_testing i left outer join e_conductivity e on i.sample_id = e.sample_id) c left outer join galvo_test gt on c.sample_id = gt.sample_id) c on c.sample_id = g.glass_id) gg on s.separator_id = gg.glass_id) s left outer join post_analysis p on s.sample_id = p.sample_id;"
		cursor.execute(query)
		testing_data_df = pd.DataFrame(cursor.fetchall())

		d = str(datetime.now(tz=None).strftime("%y%m%d"))
		name = str(d + '_Pulled_' + str(table.get()) + '_Data.xlsx').replace(" ", "_")
		testing_data_df.to_excel(name, index = False)

		# Open the file
		os.system("start EXCEL.EXE {}".format(name))

		return

	elif table.get() == 'All':
		tab01 = 'LLZO'
		tab02 = 'Li3BO3'
		tab03 = 'glass'
		tab04 = 'lnto'
		tab05 = 'cathode_substrate'
		tab06 = 'cathode'
		tab07 = 'samples'
		tab08 = 'anode'
		tab09 = 'current_collector'
		tab10 = 'parylene'
		tab11 = 'eis_testing'
		tab12 = 'post_analysis'
		tab13 = 'post_testing'
		tab14 = 'pre_testing'

		tab_list = [tab01, tab02, tab03, tab04, tab05, tab06, tab07, tab08, tab09, tab10, tab11, tab12, tab13, tab14]
		df_list = []

		for tab in tab_list:
			query = "Select * from {};".format(tab)
			cursor.execute(query)
			df = pd.DataFrame(cursor.fetchall())
			df_list.append(df)

		d = str(datetime.now(tz=None).strftime("%y%m%d"))
		name = str(d + '_Pulled_All_Data.xlsx').replace(" ", "_")
		writer = pd.ExcelWriter(name)
		for i, df in enumerate(df_list):
			df.to_excel(writer,sheet_name="{}".format(tab_list[i]))
		writer.save()

		# Open the file
		os.system("start EXCEL.EXE {}".format(name))

		return

	query = "Select * from {};".format(tab)
	cursor.execute(query)
	testing_data_df = pd.DataFrame(cursor.fetchall())

	d = str(datetime.now(tz=None).strftime("%y%m%d"))
	name = str(d + '_Pulled_' + str(table.get()) + '_Data.xlsx').replace(" ", "_")
	testing_data_df.to_excel(name, index = False)

	# Open the file
	os.system("start EXCEL.EXE {}".format(name))

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Pull_Data():
	global table
	# # Connect to DB
	# conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	# cursor = conn.cursor()

	# cursor.execute("Select sample_id from cells.samples;")
	# sample_list = [item['sample_id'] for item in cursor.fetchall()]
	
	pull = Toplevel()
	pull.title("Select a Table to Export to Excel")
	pull.geometry('200x300')

	# samples = StringVar()
	# samples.set('Select a Sample')
	# samples_label = Label(pull, text = "Samle ID").grid(row = 0, column =0)
	# samp = OptionMenu(pull, samples, *sample_list)
	# samp.grid(row = 1, column =0)

	table = StringVar()
	table.set('Select a Table')
	table_options = ['LLZO', 'Li3BO3', 'Glass', 'LNTO', 'Substrate', 'Cathode', 'Glass Extrusion', 'Anode', 'Current Collector', 'Parylene', 'EIS Testing', 'Post Analysis', 'Post Testing', 'Pre Testing', 'Logged Test Failures', 'Maccor Raw Data', 'LIBOSS Glass Properties', 'LIBOSS Sample Properties', 'Glass Properties', 'Sample Properties', 'All']
	table_label = Label(pull, text = "Select a Table:").grid(row = 0, column =0)
	table_cc = OptionMenu(pull, table, *table_options)
	table_cc.grid(row = 1, column =0)

	button_to_excel = Button(pull, text = 'Write to .xlsx', command = Pull_Data_Export).grid(row = 2, column =0, columnspan =2)

	# sample_range_label = Label(pull, text = "Sample Range (XXX##:XXX##)").grid(row = 0, column =1)
	# sample_range = Entry(pull, width = 30)
	# sample_range.grid(row = 1, column =1)

	# cursor.execute("Select * from cells.raw_testing_info where sample_id like (%s);", (samp.get()))
	# testing_data_df = pd.DataFrame(cursor.fetchall())

	# testing_data_df.to_csv('Pulled_Maccor_Data.csv', index = False)

	# # Close connection
	# conn.commit()
	# conn.close()
	# cursor.close()

# Fail Log

# submit button
def submit_fail():
	# Connect to DB
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	cursor.execute("Insert into fail_log values (%s, %s, %s, %s, %s, %s);",
		(date.get(),
		name.get(),
		task.get(),
		made.get(),
		sent.get(),
		comments.get()))

	# Clear text boxes
	made.delete(0, END)
	sent.delete(0, END)
	comments.delete(0, END)

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

def Log_Fail():
	global date
	global name
	global task
	global made
	global sent
	global comments

	fail = Toplevel()
	fail.title("Success/Fail Log")

	reg_date=fail.register(callback_date)
	reg_int=fail.register(callback_int)
	reg_float=fail.register(callback_float)
	inv_date = fail.register(invalid_date)
	inv_int = fail.register(invalid_int)
	inv_float = fail.register(invalid_float)

	# User input box
	date_label = Label(fail, text = "Date").grid(row = 0, column =0)
	date = Entry(fail, width = 15)
	date.grid(row = 1, column =0, padx = 5)
	date.insert(0, str(datetime.now(tz=None).strftime("%Y-%m-%d")))
	date.config(validate="focusout", validatecommand=(reg_date, '%P'), invalidcommand = (inv_date))

	name = StringVar()
	name.set('Select your name')
	name_options = ['Aaron', 'Ben', 'Eleston', 'Jaimison', 'Kenya']
	name_label = Label(fail, text = "Name").grid(row = 0, column =1)
	name_cc = OptionMenu(fail, name, *name_options)
	name_cc.grid(row = 1, column =1, padx = 5)

	task = StringVar()
	task.set('Select a task')
	task_options = ['Cathode', 'Glass Extrusion', 'Anode', 'Current Collector', 'Testing']
	task_label = Label(fail, text = "Task").grid(row = 0, column =2)
	task_cc = OptionMenu(fail, task, *task_options)
	task_cc.grid(row = 1, column =2, padx = 5)

	made_label = Label(fail, text = "# Made").grid(row = 0, column =3)
	made = Entry(fail, width = 15)
	made.grid(row = 1, column =3, padx = 5)
	made.config(validate="focusout", validatecommand=(reg_int, '%P'), invalidcommand = (inv_int))

	sent_label = Label(fail, text = "# Sent").grid(row = 0, column =4)
	sent = Entry(fail, width = 15)
	sent.grid(row = 1, column =4, padx = 5)
	sent.config(validate="focusout", validatecommand=(reg_int, '%P'), invalidcommand = (inv_int))

	comments_label = Label(fail, text = "Comments").grid(row = 0, column =5)
	comments = Entry(fail, width = 15)
	comments.grid(row = 1, column =5, padx = 5)

	button_submit = Button(fail, text = "Upload Data", command=submit_fail).grid(row = 2, column = 2, pady =5)

# load sucecess and fail stats
def Fail_show():
	# Connect to DB
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	cathode_total = cursor.execute("Select * from cells.cathode")
	cathode_fail = cursor.execute("Select * from cells.cathode") - cursor.execute("Select * from cells.samples")
	cathode_success = cathode_total - cathode_fail
	cathode_success_rate = cathode_success/cathode_total

	separator_total = cursor.execute("Select * from cells.samples")
	separator_fail = cursor.execute("Select * from cells.samples") - cursor.execute("Select * from cells.anode")
	separator_success  = separator_total - separator_fail
	separator_success_rate = separator_success/separator_total

	anode_total = cursor.execute("Select * from cells.anode")
	anode_fail = cursor.execute("Select * from cells.anode") - cursor.execute("Select * from cells.current_collector")
	anode_success  = anode_total - anode_fail
	anode_success_rate = anode_success/anode_total

	cc_total = cursor.execute("Select * from cells.current_collector")
	cc_fail = cursor.execute("Select * from cells.current_collector") - cursor.execute("Select * from cells.pre_testing")
	cc_success  = cc_total - cc_fail
	cc_success_rate = cc_success/cc_total

	overall_total = cursor.execute("Select * from cells.samples") # define as number of samples made by Ben
	overall_fail = cursor.execute("Select * from cells.samples") - cursor.execute("Select * from cells.pre_testing")
	overall_success = overall_total - overall_fail
	overall_success_rate = overall_success/overall_total

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

	# Display stats table
	fail = Toplevel()
	fail.title("Success/Fail Log")
	fail.geometry('800x800')
	F = Frame(fail, width=400, height=400, bg='#db1e36').place(relx=0.5, rely=0.5, anchor=CENTER)
	table = TreeView(fail)
	table['columns'] = ('Cathode Casting', 'Separator Extrusion', 'Anode', 'Current Collector', 'Cell Survived')

	table.column("Parameters", anchor=CENTER, width=80)
	table.column("Cathode Casting",anchor=CENTER, width=80)
	table.column("Separator Extrusion",anchor=CENTER,width=80)
	table.column("Anode",anchor=CENTER,width=80)
	table.column("Current Collector",anchor=CENTER,width=80)
	table.column("Cell Survived",anchor=CENTER,width=80)

	table.heading("Parameters",text="",anchor=CENTER)
	table.heading("Cathode Casting",text="Cathode Casting",anchor=CENTER)
	table.heading("Separator Extrusion",text="Separator Extrusio",anchor=CENTER)
	table.heading("Anode",text="Anode",anchor=CENTER)
	table.heading("Current Collector",text="Current Collector",anchor=CENTER)
	table.heading("Cell Survived",text="Overall Success Rate",anchor=CENTER)

	table.insert(parent='',index='end',iid=0,text='', values=('Successes: ', cathode_success, separator_success, anode_success, cc_success, overall_success))
	table.insert(parent='',index='end',iid=1,text='', values=('Failures: ', cathode_fail, separator_fail, anode_fail, cc_fail, overall_fail))
	table.insert(parent='',index='end',iid=2,text='', values=('Success Rate (%): ', cathode_success_rate,  separator_success_rate, anode_success_rate, cc_success_rate, overall_success_rate))

# Maccor test-start file generation button

# Add entry to df
def add_samples(df):
	new = [channel.get(), sample_id.get(), procedure.get(), 0, '', location.get()]
	df.loc[len(df)] = new

	# Clear/reset entry boxes
	sample_id.delete(0, END)
	channel.delete(0, END)
	return df

# Submit command for generating tsv file for Maccor test-start file
def write_csv(df):
	# delete first (empty) row from df
	df['sample_id'].replace('', np.nan, inplace=True)
	df = df.dropna(subset = 'sample_id')

	# Connect to DB
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor() 

	c_rate = []
	comments = []
	date_start = []
	current_revision = []
	group = []

	# Get 'c-rate' for each sample
	samples = [(sample) for sample in df['sample_id']]

	for sample in samples:
		# Auto update revision id
		query = "SELECT sample_id from cells.testing_summary where sample_id like '{}%'".format(sample)
		cursor.execute(query)
		result = cursor.fetchall()
		try:
			revision_list = sorted([r['sample_id'] for r in result])
			revision = revision_list[-1][-1].lower()
			current_revision.append(chr(ord(revision) +1))
		except:
			current_revision.append('a')

		# Info from samples table
		cursor.execute("Select Expected_capacity, cathode_id, cathode_coating, sample_type, separator_id, anode_type, active_area_size, ifnull(stage_temp, 0) +  ifnull(muffle_furnace_temp, 0) + ifnull(hot_plate_temp, 0) AS cathode_temp, anode_coating_type, coated_anode_directly, comments from cells.samples where sample_id like (%s);", sample)
		result = cursor.fetchone()
		c_rate.append(result['Expected_capacity'])
		cathode_id = result['cathode_id']
		cathode_coating = result['cathode_coating']
		sample_type = result['sample_type']
		separator_id = result['separator_id']
		anode_type = result['anode_type']
		active_area_size = result['active_area_size']
		cathode_temp = result['cathode_temp']
		comment = result['comments']
		anode_coating = result['anode_coating_type']
		coated_anode = ['coated_anode_directly']

		if sample_type == 'Rolling Pin':
			group.append('RF')
		elif sample_type == 'Houdini Stage':
			group.append('HF')
		elif sample_type == 'Stamp Quench':
			group.append('SF')
		elif sample_type == 'Roll Quench':
			group.append('QF')
		elif sample_type == 'Hot Roll':
			group.append('GF')
		elif sample_type == 'Liquid Electrolyte':
			group.append('LE')

		# Info from cathode table
		cursor.execute("Select casting_coating, particle_coating, active_material_type from cells.cathode where cathode_id like (%s);", cathode_id)
		result = cursor.fetchone()
		cathode_type = result['active_material_type']
		casting_coating = result['casting_coating']
		particle_coating = result['particle_coating']

		# Info from glass table
		cursor.execute("Select glass_type, num_melts from cells.glass where glass_id like (%s);", separator_id)
		result = cursor.fetchone()
		glass_type = result['glass_type']
		num_melts = result['num_melts']

		maccor_comment = '-{} {}x melts-{}-cathode @ {}C-{} {}cm2'.format(glass_type, num_melts, sample_type, int(cathode_temp), anode_type, active_area_size)

		# Compile into commments
			# Anode coating comments
		if anode_coating:
			if coated_anode == 1:
				anode_comment = '-anode coated w {}-{}'.format(anode_coating, comment)
			elif coated_anode == 0:
				anode_comment = '-separator coated w {}-{}'.format(anode_coating, comment)
			else:
				anode_comment = '-{} anode interface-{}'.format(anode_coating, comment)
		else:
			anode_comment = '-{}'.format(comment)

		# Cathode particle coating comments
		if particle_coating:
			particle_comment = '{} particle coated {}'.format(particle_coating, cathode_type)
		else:
			particle_comment = '{}'.format(cathode_type)

		# Cathode casting coating comments
		if casting_coating:
			cathode_comment = ' casted with {}'.format(casting_coating)
		else:
			cathode_comment = ''

		# Post-sinter coating comments
		if cathode_coating:
			coating_comments = '-coated w {} after sintering'.format(cathode_coating)
		else:
			coating_comments = ''

		# Combine
		maccor_comment = particle_comment+cathode_comment+coating_comments+maccor_comment+anode_comment

		comments.append(maccor_comment)

		# Date start
		date_start.append(str(datetime.now(tz=None).strftime("%y%m%d")))

	df.loc[:,'c_rate'] = c_rate
	df.loc[:,'comments'] = comments
	df.loc[:,'date_start'] = date_start
	df.loc[:, 'current_revision'] = current_revision
	df.loc[:, 'group'] = group
	df.loc[:, 'file_name'] = df.loc[:, 'date_start'] + df.loc[:, 'location'] + df.loc[:, 'group'] + df.loc[:, 'sample_id'] + df.loc[:, 'current_revision']

	# Reorder df columns to match maccor input
	df = df[['channel', 'file_name', 'procedure', 'c_rate', 'weight', 'comments']]

	# Export to csv
	df.to_csv('cells_to_test.txt', sep = '	', index = False, header= False)

	# add sample to testing_summary
	for i, sample in enumerate(samples):
		cursor.execute("insert into testing_summary (sample_id, date_test_start) values (%s, %s);", (sample+current_revision[i], date_start[i]))

	# Close connection
	conn.commit()
	conn.close()
	cursor.close()

# Create an empty df
global df
df = pd.DataFrame(columns = ['channel', 'sample_id', 'procedure', 'weight', 'file_name', 'location'])

# Click command for generating Maccor test-start files
def Maccor_Click(df):
	global sample_id
	global location
	global channel
	global num
	global procedure

	maccor = Toplevel()
	maccor.title("Generate Maccor test-start files here")
	#maccor.iconbitmap(r'JES_logo.ico')

	procedure_options = ['Select',
	"~~AFOIL-RT-CV-C-C5-C2.000",
    "~~AFOIL-C10 CH_C20 Dis.000",
    "~~AFOIL-HT-CV-CCChargeC20.000",
    "~~AFOIL-RT-CV-CCChargeC20.000",
    "~~AFOIL-RT-CV-CCChargeC50.000",
    "~~FOIL-C10CH_C20DC 3800mV.000",
    "~~FOIL-C10CH_C20DC 4300mV.000",
    "~~FOIL-CV-CC 4300mv C40.000"]

	# User input boxes
	sample_id_label = Label(maccor, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(maccor, width = 15)
	sample_id.grid(row = 1, column =0, padx=5)

	channel_label = Label(maccor, text = "Channel #").grid(row = 0, column =1)
	channel = Entry(maccor, width = 15)
	channel.grid(row = 1, column =1, padx=5)

	procedure_label = Label(maccor, text = "Procedure").grid(row = 0, column =2)
	procedure = ttk.Combobox(maccor, value = procedure_options, width = 30)
	procedure.current(1)
	procedure.grid(row = 1, column =2)

	location_options = ['Select', 'LB', 'PB', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7']
	location_label = Label(maccor, text = "Select a Location:").grid(row = 0, column =3)
	location = ttk.Combobox(maccor, value = location_options)
	location.current(2)
	location.grid(row = 1, column =3, padx = 5)

	# group_options = ['Select', 'FT', 'FF', 'TT', 'TF', 'ST', 'SF']
	# group_label = Label(maccor, text = "Select a Group:").grid(row = 0, column =5)
	# group = ttk.Combobox(maccor, value = group_options)
	# group.current(0)
	# group.grid(row = 1, column =5, padx = 5)

	button_add = Button(maccor, text = "Add Data", command=lambda: add_samples(df)).grid(row = 3, column = 0, columnspan =2)

	df = add_samples(df)

	button_to_csv = Button(maccor, text = 'Write to .csv', command = lambda: write_csv(df)).grid(row = 4, column =0, columnspan =2)
	df = pd.DataFrame(columns = ['channel', 'sample_id', 'procedure', 'weight', 'file_name', 'location'])

def submit_error():
	df = pd.DataFrame.from_dict({'Date': [str(datetime.now(tz=None).strftime("%Y-%m-%d"))], 'Error' : [er.get()]})
	df.to_csv('Error_Log.csv', mode = 'a', index = False)

	er.delete(0, END)

def Error_Log():
	global er

	error = Toplevel()
	error.title('Report Data Entry Errors Here')
	#maccor.iconbitmap(r'JES_logo.ico')

	# User input boxes
	er_label = Label(error, text = "Report Error Here").grid(row = 0, column =0)
	er = Entry(error, width = 100)
	er.grid(row = 1, column =0, padx = 10)

	button_submit = Button(error, text = "Submit Error", command=submit_error).grid(row = 2, column = 0, columnspan =2)

def Delete_Entry():
	delt = Toplevel()
	delt.title("Delete Entries Here")
	#maccor.iconbitmap(r'JES_logo.ico')

def submit_update():

	if initial.get()is not None:
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			if table.get() == 'LLZO':
				query = 'update {} set {} = "{}" where llzo_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			elif table.get() == 'Li3BO3':
				query = 'update {} set {} = "{}" where li3bo3_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			elif table.get() == 'LNTO':
				query = 'update {} set {} = "{}" where lnto_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			elif table.get() == 'Cathode':
				query = 'update {} set {} = "{}" where cathode_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			elif table.get() == 'Cathode Substrate':
				query = 'update {} set {} = "{}" where substrate_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			elif table.get() == 'Glass':
				query = 'update {} set {} = "{}" where glass_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			else:
				query = 'update {} set {} = "{}" where sample_id like "{}"'.format(table.get(), field.get(), new_value.get(), sample_id.get())
			
			cursor.execute(query)

			# Clear text boxes
			sample_id.delete(0, END)
			initial.delete(0, END)

		except:
			error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
			if re.match("Duplicate entry", error) is not None:
				messagebox.showerror('Duplicate Entry Error', error)
			else:
				messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		cursor.close()
		conn.commit()
		conn.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')


def Update_Click():
	global table
	global field
	global sample_id
	global new_value
	global initial

	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	def pick_fields(event):

		if table.get() == 'Substrate':
			tab = 'Cathode_Substrate'
		elif table.get() == 'Glass Extrusion':
			tab = 'samples'
		elif table.get()  == 'Anode':
			tab = 'samples'
		elif table.get()  == 'Current Collector':
			tab = 'current_collector'
		elif table.get()  == 'EIS Testing':
			tab = 'eis_testing'
		elif table.get() == 'E Conductivity':
			tab = 'e_conductivity'
		elif table.get() == 'Post Analysis':
			tab = 'post_analysis'
		else:
			tab = table.get()

		query = "describe {};".format(tab)
		cursor.execute(query)
		field_options = cursor.fetchall()
		field_options = [d['Field'] for d in field_options]

		field.config(value = field_options)
		field.current(0)

	up = Toplevel()
	up.title("Update Entries Here")
	#maccor.iconbitmap(r'JES_logo.ico')
	up.geometry('600x400')

	table_options = ['Select', 'LLZO', 'Li3BO3', 'Glass', 'LNTO', 'Substrate', 'Cathode', 'Glass Extrusion', 'Anode', 'Current Collector', 'Parylene', 'EIS Testing', 'E Conductivity', 'Post Analysis', 'B2S3']
	table_label = Label(up, text = "Select a Table:").grid(row = 0, column =5)
	table = ttk.Combobox(up, value = table_options)
	table.current(0)
	table.grid(row = 1, column =5, padx = 5)

	table.bind("<<ComboboxSelected>>", pick_fields)

	field_label = Label(up, text = "Select a Field:").grid(row = 0, column =6)
	field = ttk.Combobox(up, value = ['Select'])
	field.grid(row = 1, column =6, padx = 5)

	sample_id_label = Label(up, text = "Sample ID").grid(row = 0, column =7)
	sample_id = Entry(up, width = 15)
	sample_id.grid(row = 1, column =7, padx = 5)

	new_value_label = Label(up, text = "New Value").grid(row = 0, column =8)
	new_value = Entry(up, width = 15)
	new_value.grid(row = 1, column =8, padx = 5)

	initial_label = Label(up, text = "Enter Your Initials Here:").grid(row = 2, column =6)
	initial = Entry(up, width = 15)
	initial.grid(row = 3, column =6, padx = 5)

	button_submit = Button(up, text = "Upload Data", command=submit_update).grid(row = 3, column = 7)

# Click command for logging why cells are taken off maccor testing
def submit_test_end():
	if initial.get():
		# Connect to DB
		conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
		cursor = conn.cursor() 

		try:
			cursor.execute("Insert into log_test_end (sample_id, reason_test_end, comments, initials) values (%s, %s, %s, %s);",
				(sample_id.get(),
				r.get(),
				comments.get(),
				initial.get()))

			# Clear text boxes
			sample_id.delete(0, END)
			#date_made.delete(0, END)
			#date_rm.delete(0, END)
			comments.delete(0, END)
			initial.delete(0, END)

		except:
				error = re.search(r'pymysql.*"(.*)"', str(traceback.format_exc())).group(1)
				if re.match("Duplicate entry", error) is not None:
					messagebox.showerror('Duplicate Entry Error', error)
				else:
					messagebox.showerror('Data Entry Error', str(traceback.format_exc()))

		# Close connection
		cursor.close()
		conn.commit()
		conn.close()
	else:
		messagebox.showerror('Initial Error', 'Make sure you are entering your initials!')

def End_Test_Click():
	global sample_id
	global date_test_end
	global r
	global comments
	global initial

	et = Toplevel()
	et.title("Log Why Cells are Taken Off Maccor Testing")
	#maccor.iconbitmap(r'JES_logo.ico')
	reg_date=et.register(callback_date)
	# reg_int=maccor.register(callback_int)
	# reg_float=maccor.register(callback_float)
	inv_date = et.register(invalid_date)
	# inv_int = maccor.register(invalid_int)
	# inv_float = maccor.register(invalid_float)

	# User input boxes
	sample_id_label = Label(et, text = "Sample ID").grid(row = 0, column =0)
	sample_id = Entry(et, width = 15)
	sample_id.grid(row = 1, column =0)

	r = StringVar()
	r.set('Pick a Reason')

	r_options = ['High Impedance', 'Efficiency Loss', 'Initial Leaking', 'Capacity < 70% of 2nd cycle', 'Test Completed']

	r_label = Label(et, text = "Reason").grid(row = 0, column =1) 
	reason = OptionMenu(et, r, *r_options)
	reason.grid(row = 1, column =1)

	comments_label = Label(et, text = "Comments").grid(row = 0, column =2)
	comments = Entry(et, width = 60)
	comments.grid(row = 1, column =2)

	initial_label = Label(et, text = "Enter Initials Here").grid(row= 2, column = 1)
	initial = Entry(et, width = 15)
	initial.grid(row = 3, column =1)

	
	button_submit = Button(et, text = "Submit Data", command=submit_test_end).grid(row = 3, column = 2)

def Group_glass():
	conn = pymysql.connect(host = '192.168.0.39', user = 'JESRemote', password = '@!2022J3$**', db = 'cells', charset = 'utf8mb4' , cursorclass = pymysql.cursors.DictCursor)
	cursor = conn.cursor()

	query = "SELECT * from glass;"
	cursor.execute(query)
	testing_data_df = pd.DataFrame(cursor.fetchall())

	testing_data_df.set_index('Glass_id', inplace = True)

	d = str(datetime.now(tz=None).strftime("%y%m%d"))

	materials_list = ['Li2B4O7', 'SiO2', 'B2O3', 'Li2O', 'Li2CO3', 'LiBO2', 'Li3BO3', 'Li2O2', 'LiOH', 'K2CO3', 'MoO3', 'V2O5', 'NbO', 'LiCl', 'Na2SO4', 'Li2SO4', 'LiI', 'Li3N', 'Al2O3', 'C', 'LiF', 'Li2SiO3', 'Li4SiO4', 'B2S3', 'SiS2', 'Li2S', 'LiPO3', 'SiI4', 'SiCl4', 'P2O3.5N', 'GeS2', 'LiTSFI', 'LiBr', 'S', 'B', 'LiBF4']
	cols = []

	for m in materials_list:
		cols.append(m + '_wt_pct')

	grouped = testing_data_df.groupby(by = cols, axis = 0)

	groups = [val for val in grouped.groups.values()]

	groups.pop(0)

	dict_groups = {}

	i = 1

	for g in groups:
		if len(g) > 1:
			dict_groups['Group ' + str(i)] = g.tolist()
			i+=1

	dict_groups = dict([ (k,pd.Series(v)) for k,v in dict_groups.items() ])

	df = pd.DataFrame.from_dict(dict_groups)

	name = "Glass_Groups" + d + ".xlsx"

	df.to_excel(name, index = False)

	os.system("start EXCEL.EXE {}".format(name))


# Buttons and Frames

	# Entry table frame (top, middle)
F0 = Frame(root, width=400, height=190, bg='#db1e36').place(relx=0.5, rely=0.157, anchor=CENTER)
F1 = Frame(F0, width=380, height=170, bg='#f6f6f6').place(relx=0.5, rely=0.157, anchor=CENTER)

	# Buttons to navigate to user data entry tables
LLZO_Button = Button(F1, text="LLZO", command = LLZO_Click, width = 15, bg = '#c5c5c5').place(relx=0.35, rely=0.08, anchor=CENTER)
Li3BO3_Button = Button(F1, text="Li3BO3", command = Li3BO3_Click,  width = 15, bg = '#c5c5c5').place(relx=0.35, rely=0.13, anchor=CENTER)
LNTO_Button = Button(F1, text="LNTO", command = LNTO_Click,  width = 15, bg = '#c5c5c5').place(relx=0.35, rely=0.18, anchor=CENTER)
separator_Button = Button(F1, text="Glass", command = Glass_Click,  width = 15, bg = '#c5c5c5').place(relx=0.35, rely=0.23, anchor=CENTER)
Substrate_Button = Button(F1, text="Substrate", command = Substrate_Click,  width = 15, bg = '#c5c5c5').place(relx=0.5, rely=0.08, anchor=CENTER)
Cathode_Button = Button(F1, text="Cathode", command = Cathode_Click,  width = 15, bg = '#c5c5c5').place(relx=0.5, rely=0.13, anchor=CENTER)
Glass_Button = Button(F1, text="Glass Extrusion", command = Sample_Click,  width = 15, bg = '#c5c5c5').place(relx=0.5, rely=0.18, anchor=CENTER)
Anode_Button = Button(F1, text="Anode", command = Anode_Click,  width = 15, bg = '#c5c5c5').place(relx=0.5, rely=0.23, anchor=CENTER)
CC_Button = Button(F1, text="Current Collector", command = CC_Click,  width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.08, anchor=CENTER)
#Pary_Button = Button(F1, text="Parylene", command = Parylene_Click,  width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.13, anchor=CENTER)
Conductivity = Button(F1, text="E-Chem Tests", command = Cond_Click,  width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.13, anchor=CENTER)
# B2S3 = Button(F1, text="B2S3", command = B2S3_Click, width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.18, anchor=CENTER)
AC_Button = Button(F1, text="Anode Coating", command = AC_Click, width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.18, anchor=CENTER)
PostA_Button  = Button(F1, text="Post Analysis", command = PostA_Click,  width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.23, anchor=CENTER)

# Maccor Test-start file frame (middle, middle)
F2 = Frame(root, width=400, height=60, bg='#db1e36').place(relx=0.5, rely=0.35, anchor=CENTER)
F3 = Frame(F2, width=380, height=40, bg= '#f6f6f6').place(relx=0.5, rely=0.35, anchor=CENTER)

	# Button to generate Fail Log, Enter Fail Stats
Fail_Button = Button(root, text= 'Log Successes and Failures', command = Log_Fail, bg = '#c5c5c5').place(relx=0.39, rely=0.35, anchor=CENTER)
Fail_Stats_Button = Button(root, text= 'Show Success and Fail Stats', command = Fail_show, bg = '#b46767').place(relx=0.61, rely=0.35, anchor=CENTER)

	# Maccor Test-start file frame (middle, middle)
F4 = Frame(root, width=400, height=60, bg='#db1e36').place(relx=0.5, rely=0.5, anchor=CENTER)
F5 = Frame(F4, width=380, height=40, bg='#f6f6f6').place(relx=0.5, rely=0.5, anchor=CENTER)

	# Button to generate Maccor test Start file
Maccor_CSV_Button = Button(root, text= 'Generate CSV File', command = lambda: Maccor_Click(df), width = 15, bg = '#c5c5c5').place(relx=0.41, rely=0.5, anchor=CENTER)
Maccor_End_Test_Button = Button(root, text= 'Log Test End', command = End_Test_Click, width = 15, bg = '#c5c5c5').place(relx=0.58, rely=0.5, anchor=CENTER)

	# Pulling and Plotting data frame (bottom, middle)
F6 = Frame(root, width=400, height=60, bg='#db1e36').place(relx=0.5, rely=0.65, anchor=CENTER)
F7 = Frame(F6, width=380, height=40, bg='#f6f6f6').place(relx=0.5, rely=0.65, anchor=CENTER)

Sample_Summary_Button = Button(root, text= 'Sample Summary', command = Sample_Summary, width = 15, bg = '#b46767').place(relx=0.35, rely=0.65, anchor=CENTER)
Pull_Data_Button = Button(root, text= 'Pull Data', command = Pull_Data, width = 15, bg = '#c5c5c5').place(relx=0.5, rely=0.65, anchor=CENTER) 
Group_glass_Button = Button(root, text= 'Group Glasses', command = Group_glass, width = 15, bg = '#c5c5c5').place(relx=0.65, rely=0.65, anchor=CENTER)

	# Error Logs, Delete with Special Permission
F8 = Frame(root, width=400, height=60, bg='#db1e36').place(relx=0.5, rely=0.8, anchor=CENTER)
F9 = Frame(F8, width=380, height=40, bg='#f6f6f6').place(relx=0.5, rely=0.8, anchor=CENTER)

Error_Log_Button = Button(root, text= 'Submit Error Note', command = Error_Log, width = 15, bg = '#c5c5c5').place(relx=0.41, rely=0.8, anchor=CENTER)
Update_Entry_Button = Button(root, text= 'Update Error', command = Update_Click, width = 15, bg = '#c5c5c5').place(relx=0.58, rely=0.8, anchor=CENTER)
# Delete_Entry_Button = Button(root, text= 'Delete Entry', command = Delete_Entry, width = 15, bg = '#b46767').place(relx=0.65, rely=0.8, anchor=CENTER)

# #Button to plot
# Plot_Button = Button(root, text= 'Generate CSV File', command = lambda: Maccor_Click(df)).place(relx=0.5, rely=0.35, anchor=CENTER)

root.mainloop()