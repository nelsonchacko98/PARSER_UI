import os
import glob
from pdfminer.high_level import extract_text
import nltk
from tqdm import tqdm

"""
  The function takes in the path for the pdf files to check if the files are resume or not. The function uses resume_keys list to match keywords. 
  If the number of keywords is higher than a certain threshold ( 6 in this case ), then the file is deemed as a resume and moved to another folder
  
"""

resume_keys = ['Education','skills','College', 'email', 'language', 'experience','experiences', 'career','careers' 'objective','objectives' 'profile', 'profiles','institution','institutions', 'course','courses','technical', 'project','projects', 'intern', 'intersnship', 'cerificates', 'work', 'certificate','interests', 'summary','PROFESSIONAL','ACADEMIC','QUALIFICATIONS','QUALIFICATION','training', 'achievement', 'achievements', 'software', 'engineer', 'volunteer', 'reference', 'declaration', 'contact','technology','technologies' ]


def copy_resumes(download_folder) : 
  resumes = []
  file_paths = glob.glob(f"{download_folder}/*.pdf")


  confirm_resume_path = os.path.join(download_folder,"confirm_resume_folder")

  if not os.path.isdir(confirm_resume_path):
      os.makedirs(confirm_resume_path, exist_ok=True)

  print("Confirmed resumes : ")
  for file in file_paths : 
      
      file_name = file.split("\\")[-1]
      
      try : 
        text = extract_text(file)

      except Exception as e : 
        print(f"Unable to extract data from {file_name}")
      
      common_words =[]
      
      nltk_tokens = nltk.word_tokenize(text)

      for i in nltk_tokens:
          for j in resume_keys:
              if i.lower()==j.lower():
                  common_words.append(i)
          
      unique = set(common_words)
      

      if(len(unique) > 6):
          print(file_name)
      
          dest_path = os.path.join(confirm_resume_path,file_name)

          try : 
            os.rename(file,dest_path)
            resumes.append(file_name)

          except Exception as e :
            print(f"An error occured for {file_name}, File might already Exist there")

  return resumes
          
if __name__ == '__main__' :
  download_folder = os.path.join(os.getcwd(),'downloads')
  resumes = copy_resumes(download_folder)
  print(resumes)
  