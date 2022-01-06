from string import punctuation
from Google import Create_Service
import base64
import os
import datetime
from check_if_resume import copy_resumes


def search_email(service, query_string, label_ids =[]): 
    try : 
        message_list_response = service.users().messages().list(
            userId = 'me',
            labelIds = label_ids,
            q = query_string
        ).execute()

        
        message_items = message_list_response.get('messages')
        nextPageToken = message_list_response.get('nextPageToken')

        while nextPageToken : 
            message_list_response = service.users().messages().list(
                userId = 'me',
                labelIds = label_ids,
                q = query_string,
                pageToken = nextPageToken
            ).execute()

            message_items.extend(message_list_response.get('messages'))
            nextPageToken = message_list_response.get('nextPageToken')
        return message_items
            

    except Exception as e : 
        print("Exception in search_email : \n",e)
        return None

def get_message_detail(service, message_id, format = 'metadata', metadata_headers = []) : 

    try : 
        message_detail = service.users().messages().get(
            userId = 'me',
            id = message_id,
            format = format,
            metadataHeaders = metadata_headers
        ).execute()

        return message_detail
    
    except Exception as e :
        print(e)
        return None

def download_resumes() : 
    CLIENT_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION  = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)


    #Create all the folders required
    download_path = os.path.join(os.getcwd(),'downloads')

    if not os.path.exists(download_path) : 
        os.mkdir(download_path)

    query_string = 'has:attachment filename:pdf' 
    
    if os.path.exists('timestamp.txt') :
        last_line = ''
        with open('timestamp.txt','r') as fp : 
            for last_line in fp :
                pass

        if last_line : 
            format_data = "%Y-%m-%d %H:%M:%S.%f" 
            dt = datetime.datetime.strptime(last_line,format_data)

            year = dt.strftime('%Y')
            month = dt.strftime('%m')
            day = dt.strftime('%d')
            query_string +=f" after:{year}/{month}/{day}"

    email_messages = search_email(service, query_string, ['INBOX'])

    if not email_messages : 
        print("No new emails to download")
        return None

    print("Type of email_messages : ",type(email_messages[0]))
    print("Content of email_messages : ")
    print(email_messages)

    for email_message in email_messages : 
        messageId = email_message['threadId']
        messageSubject = '(No Subject) ({0})'.format(messageId)
        messageDetail = get_message_detail(
            service,
            email_message['id'],
            format='full',
            metadata_headers=['parts']
        )
        messageDetailPayload = messageDetail.get('payload')

        # Get the subject if it exists
        for item in messageDetailPayload['headers'] : 
            if item['name'] == 'Subject' : 
                if item['value'] : 
                    messageSubject = '({0}) ({1})'.format(item['value'],messageId)
            
        # Check the messageDetailPayload for the attachments
        if 'parts' in messageDetailPayload : 
            for msgPayload in messageDetailPayload['parts']: 
                
                mime_type = msgPayload['mimeType']
                file_name = msgPayload['filename']
                head,ext= os.path.splitext(file_name)

                head = ''.join(e for e in head if e.isalnum())

                body = msgPayload['body']

                if 'attachmentId' in body : 
                    attachment_id = body['attachmentId']

                    response = service.users().messages().attachments().get(
                        userId = 'me',
                        messageId = email_message['id'],
                        id=attachment_id
                    ).execute()

                    file_data = base64.urlsafe_b64decode(
                        response.get('data').encode('UTF-8')
                    )
                    
                    made_up_file_name = f'({head}) ({messageId}){ext}'
                    file_path = os.path.join(download_path,made_up_file_name)

                    try : 
                        print(f"Writing file : {file_name}")
                        with open(file_path,'wb') as fh :
                            fh.write(file_data)

                    except Exception as e : 
                        print(f"Error in writing file : {file_name}")
                        print(e)
                        print()


    # Write the current time to a file, so that next time the program is run, this file can be consulted to see the last time the program was run.
    # This can be usefull when only the latest unseen email attachments need to be downloaded
    with open('timestamp.txt','a') as fp : 
        string_to_write = '\n'+str(datetime.datetime.now())
        dt = fp.write(string_to_write)

    resumes = copy_resumes(download_path)
    return resumes

if __name__ == '__main__' : 
    download_resumes()