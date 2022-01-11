import spacy
import utils
import os
import glob
import json

import constants as cs

from spacy.matcher import Matcher
from spacy import util
from tqdm import tqdm

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
        self.__resume_path = resume
        self.__resume_name = os.path.split(resume)[1]
        ext = self.__resume_path.split('.')[-1]
        try : 
            self.__text_raw = utils.extract_text(self.__resume_path, '.' + ext)
        except Exception as e :
            print(f"{self.__resume_path} has a problem {e}")
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
                                            self.__resume_path
                                        )
        self.__details['file_name'] = self.__resume_path
        self.__details['resume_name'] = self.__resume_name
        self.__details['other name hits '] = otherHits        
        return
    

def get_existing_resume_names() : 
    names = []
    with open(cs.DATABASE) as fin : 
        for line in fin : 
            data = json.loads(line)
            names.append(data.get('resume_name'))

    return names

def parser() : 
    print('Starting Programme')
    resume_folder = os.path.join(os.getcwd(),'downloads','confirm_resume_folder')
    pdf_files = glob.glob(f'{resume_folder}/*.pdf')

    if not os.path.isdir('json_out') : 
        os.makedirs('json_out')

    names = get_existing_resume_names()
    files = list(set(pdf_files))
    files.sort()
    print (f"{len(files)} files identified")

    for f in tqdm(files):
        print(f"Reading File {f}")
        obj = ResumeParser(f)
        details = obj.get_extracted_data()

        utils.write_to_json(details,names)

    return
        
        
if __name__ == '__main__' : 
    parser()
