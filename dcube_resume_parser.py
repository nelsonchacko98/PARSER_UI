import spacy
from spacy.matcher import Matcher
import utils
import json
import os
from tqdm import tqdm
import glob

class ResumeParser(object):

    def __init__(
        self,
        resume,
        skills_file=None,
        custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'name': None,
            'email': None,
            'mobile_number': None,
            'skills': None,
            'no_of_pages': None,
            'file_name' : None
        }
        self.__resume = resume
        ext = self.__resume.split('.')[-1]
        try : 
            self.__text_raw = utils.extract_text(self.__resume, '.' + ext)
        except Exception as e :
            print(f"{self.__resume} has a problem {e}")
        self.__text = ' '.join(self.__text_raw.split())
        self.__lines = utils.get_lines_from_text(self.__text_raw)
        self.__nlp = nlp(self.__text)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__blocks = utils.extract_entity_sections_grad(self.__text_raw)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details

    def __get_basic_details(self):
        # name = utils.extract_name(self.__nlp, matcher=self.__matcher)
        name , otherHits = utils.extract_name_regex(self.__lines)
        email = utils.extract_email(self.__text)
        mobile = utils.extract_mobile_number(self.__text, self.__custom_regex)
        skills = utils.extract_skills_new(
                    self.__text_raw
                )
        # edu = utils.extract_education(
        #               [sent.string.strip() for sent in self.__nlp.sents]
        #       )
        entities = utils.extract_entity_sections_grad(self.__text_raw)
        
        self.__details['name'] = name
        self.__details['mobile_number'] = mobile
        self.__details['email'] = email
        self.__details['skills'] = skills
        self.__details['no_of_pages'] = utils.get_number_of_pages(
                                            self.__resume
                                        )
        self.__details['file_name'] = self.__resume
        self.__details['other name hits '] = otherHits        
        return
    
    

def parser() : 
    print('Starting Programme')
    resume_folder = os.path.join(os.getcwd(),'downloads','confirm_resume_folder')
    pdf_files = glob.glob(f'{resume_folder}/*.pdf')

    if not os.path.isdir('json_out') : 
        os.makedirs('json_out')

    files = list(set(pdf_files))
    files.sort()
    print (f"{len(files)} files identified")

    for f in tqdm(files):
        print(f"Reading File {f}")
        obj = ResumeParser(f)
        details = obj.get_extracted_data()
        
        # fileName = f.split('\\')[-1]
        fileName = os.path.split(f)[1].split('.')[0]
                
        fOut = open(f'json_out/{fileName}.json','w') 
        fOut.write(json.dumps(details,indent=4))
        fOut.close()

    return
        
        
if __name__ == '__main__' : 
    parser()
