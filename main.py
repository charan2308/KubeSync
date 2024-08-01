import os.path # for checking if token.json exists
from google.auth.transport.requests import Request #for making requests
from google.oauth2.credentials import Credentials #for fetching credentials from credentials.json
from google_auth_oauthlib.flow import InstalledAppFlow # used to handle the OAuth 2.0 authorization flow for applications
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError # for handling http errors
from googleapiclient.http import MediaFileUpload # for multipart upload
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"] # specifies the level of access allowed to the app



def main():
  """Shows basic usage of the Drive v3 API.
     Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  
  
  
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=1, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", []) #get files on drive
    if not items:
      print("No files found.")
      return
    print("Files that are on my drive:")
    for item in items:
      print(f"{item['name']} ({item['id']})")
  except HttpError as error:
    # - Handle errors from drive API.
    print(f"An error occurred: {error}")
    
    
def credsfunc():
  """ builds and returns the connection object(service) using creds"""
  creds=None
  if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
          """The file token.json stores the user's access and refresh tokens, and is created automatically 
     when the authorization flow completes for the first time."""
          flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
          creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())
  service = build("drive", "v3", credentials=creds)
  return service
      
      

def upload_file(FILENAME,service):
  """Prints the names of the first 10 files the user has access to."""
  creds=None
  mymedia=MediaFileUpload(FILENAME)
  # Metadata about the file. 
  upload= service.files().create(body={"name":FILENAME},media_body=mymedia).execute()
  print("File upload function executed : ")
  print(upload.get("name"))
  

 
def create_folder(service): 
  try:
    """creating a folder on drive with the name as backup_+current_timestamp and returning the file id"""
    current_timestamp = datetime.now().strftime("%Y/%m/%d_%H:%M:%S")
    folder_metadata = {
          "name": "backup_"+current_timestamp,
          "mimeType": "application/vnd.google-apps.folder",
          }
    folder = service.files().create(body=folder_metadata, fields="id,name").execute()
    print('\033[32mBackup Folder created on GoogleDrive with name :\033[32m \033[0m',folder.get("name"))
    return folder.get('id')
  except HttpError as error:
      print(f"An error occurred : {error}")
      return None 


 
def upload_to_folder(service,folder_id,filename):
  """upload a file to the created folder using its id """
  try:
      file_metadata = {"name": filename, "parents": [folder_id]}
      media = MediaFileUpload(filename, resumable=True)
      file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
      print(f'Uploaded file: "{file.get("name")}".')
      return file.get("id")
  except HttpError as error:
      print(f"An error occurred while uploading file {filename}: {error}")
      return None




def upload_all_files_n_folders(service,folder_id,folder_path):
  """os.walk recursively traverses through the directory and 
  gets the current directory, all the files and folder in that
  directory"""
  try:
    current_folder_id = folder_id
    for root, dirs, files in os.walk(folder_path):
      folder_name = os.path.basename(root)
      totfiles=len(files)
      # Create folder in Google Drive 
      folder_metadata = {"name": folder_name, "parents": [current_folder_id], "mimeType": "application/vnd.google-apps.folder"}
      folder = service.files().create(body=folder_metadata, fields="id").execute()
      current_folder_id = folder.get("id")
      print(f"\033[32m\nCreated folder\033[0m {folder_name} \033[32mon GoogleDrive\033[0m")
      print("Folders in",os.path.basename(root),":",dirs)
      print("Total files in the current folder:",totfiles)
      # Upload files in the current folder
      filecount=0
      for file in files:
        filecount+=1
        file_metadata = {"name": file, "parents": [current_folder_id]}
        media = MediaFileUpload(os.path.join(root, file), resumable=True)
        uploadfile = service.files().create(body=file_metadata, media_body=media).execute()
        print("\033[33mUploading file:\033[0m", uploadfile.get('name'))
      print("\033[32mSucessfully uploaded the folder\033[0m")
      break
    # Recursively traverse into subdirectories
    for subdir in dirs:
      print("\nNow going to upload folder: \"",subdir,"\"")
      upload_all_files_n_folders(service, current_folder_id, root+"/"+subdir)

  except HttpError as error:
    print("Error uploading")
    return False          
  return True
              
  
  
  
if __name__ == "__main__":
  def main():
    path="/app/files"
    # path = 'D:\\SEM6\\CC\\project\\bcd'

    # for root, dirs,files in os.walk(path):
    #   break
    # newpath = root +"/"+dirs[0] 
    newpath=path


    if not os.path.exists(newpath):
        print("\033[31mThe given path does not exist. Please check the path and try again.\033[0m")
        return None
      
    service = credsfunc()

    folder_id = create_folder(service)
    if(upload_all_files_n_folders(service, folder_id, newpath)):
      print("\033[34m\nUploaded all files and folders successfully!\033[0m\n")
      

  main()
