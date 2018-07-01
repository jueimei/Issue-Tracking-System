#!/usr/bin/python
import sys,string,datetime
import csv
import sqlite3
import argparse

def read_csv(csv_path,failure_symptom,bundle,diags,os):
  """ generates record info
  :param csv_path: .csv with sn and config 
  :return: a list of record
  """
  temp = []
  time = datetime.datetime.now().strftime("%Y-%m-%d_%I:%M:%S")
  result = "FAIL"
  with open(csv_path,'rU') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
      row.append(failure_symptom)
      row.append(time)
      row.append(bundle)
      row.append(diags)
      row.append(os)
      row.append(result)
      temp.append(row)
  return temp

def insert_db(db_path,unit_list):
  """ database connection to the SQLite database
        specified by db_path
  :param db_path: general db 
  :unit_list: record to be added
  """
  connection = sqlite3.connect(db_path)
  cursor = connection.cursor()
  for item in unit_list:
    col_sn=0
    col_cfg=1
    col_fs=2
    col_time=3
    col_bundle=4
    col_diags=5
    col_os=6
    col_result=7
    temp_0 = [item[col_sn],item[col_cfg],item[col_fs],item[col_time]]
    cursor.execute('insert into BurnIn (SN,Type,FailureSymptom,Time) values (?,?,?,?)', temp_0)
    temp_1 = [item[col_sn],item[col_cfg],item[col_time],item[col_bundle],item[col_diags],item[col_os]]
    cursor.execute('insert into BurnInUnitsList (SN,Type,Time,Bundle,Diags,Root) values (?,?,?,?,?,?)', temp_1)
    temp_2 = [item[col_sn],item[col_result],item[col_cfg],item[col_time]]
    cursor.execute('insert into InputUnitsList (SN,Result,Type,Time) values (?,?,?,?)', temp_2)

  connection.commit()
  print "Records created successfully!"
  connection.close()


parser = argparse.ArgumentParser(description='Insert test argument')
parser.add_argument("-c", "--csv_path", help="input csv path") 
parser.add_argument("-db", "--db_path", help="input db path") 
parser.add_argument("-f", "--failure_symptom", help="input failure symptom") 
parser.add_argument("-b", "--bundle", help="input bundle version") 
parser.add_argument("-d", "--diags", help="input diags version") 
parser.add_argument("-o", "--os", help="input os version") 

args = parser.parse_args()

csv_path = args.csv_path if args.csv_path else None
db_path = args.db_path if args.db_path else None
failure_symptom = args.failure_symptom if args.failure_symptom else ''
bundle = args.bundle if args.bundle else ''
diags = args.diags if args.diags else ''
os = args.os if args.os else ''

unit_list = read_csv(csv_path,failure_symptom,bundle,diags,os)
insert_db(db_path,unit_list)



