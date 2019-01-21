# -*- coding: utf-8 -*-

import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

xml_files_dir_path =  'XML_FILES/'
CSV_files_dir_path = 'CSV/'


def fix_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        return date_string


def update_dict_types(values_dict, attributes_types_list):
    """
    casting fields to different types, input as list with tuples(field,type)
    example: [("Id", int), ("UserId", int)]
    """
    for field, _type in attributes_types_list:
        try:
            values_dict[field]=_type(values_dict[field])
        except:
            continue


def create_row_list(xml_file_path, typesToCastList=None):
    """
    generate list of xmlfile based on rows
    #TODO: transfer to generator
    """
    document = ET.parse(xml_file_path).getroot()
    row_list = []
    for doc in document.iter('row'):
        doc_elements = doc.attrib
        if typesToCastList:
            update_dict_types(doc_elements, typesToCastList)
        row_list.append(doc_elements)
    return row_list


def pandasframe_to_CSV(csv_dir, file_name, pandas_frame, separator="|"):
    """
    export to CSV
    """
    file_name = file_name.split(".xml")[0] + ".csv"   
    output =  csv_dir + file_name
    pandas_frame.to_csv(output, index = False, sep=separator', encoding='utf-8')        
   
     
def create_pandas_dataframe(xml_file_name, typesToCastList=None, create_CSV=True):  
    """
    returns pandas dataframe, if create_CSV=True 
    """
    xml_file_path = xml_files_dir_path + xml_file_name
    rows = create_row_list(xml_file_path, typesToCastList)
    pandas_doc = pd.DataFrame(rows)

    if create_CSV:
        pandasframe_to_CSV(csv_dir=CSV_files_dir_path, file_name=xml_file_name, pandas_frame=pandas_doc)
    
    return pandas_doc


##### XML -> Pandas   
#Badges
types_Badges = [("Id", int), ("UserId", int), ("Class", int), ("Date", fix_date)]
Badges_pandas = create_pandas_dataframe("Badges.xml", types_Badges)

#Commemnts
types_Comments = [("Id", int), ("PostId", int), ("UserId", int),  ("Score", int), ("CreationDate", fix_date)]
Comments_pandas = create_pandas_dataframe("Comments.xml", types_Comments)

#PostHistory
types_PostHistory = [("Id", int), ("PostHistoryTypeId", int), ("PostId", int), ("CreationDate", fix_date), ("UserId", int)]
PostHistory_pandas = create_pandas_dataframe("PostHistory.xml", types_PostHistory)

#PostLinks
types_PostLinks = [("Id", int), ("RelatedPostId", int), ("PostId", int), ("CreationDate", fix_date)]
PostLinks_pandas = create_pandas_dataframe("PostLinks.xml", types_PostLinks)

#Post
types_Posts = [("Id", int), ("PostTypeId", int), ("AcceptedAnswerId", int),  ("CreationDate", fix_date), ("Score", int),
               ("ViewCount", int), ("OwnerUserId",int), ("LastEditorUserId",int),
               ("LastEditDate", fix_date), ("LastActivityDate", fix_date), ("AnswerCount", int),
               ("CommentCount", int), ("ClosedDate", fix_date), ("FavoriteCount", int), ("AnswerCount",int)]
Post_pandas = create_pandas_dataframe("Posts.xml", types_Posts)              

#Tags
types_Tags = [("Id", int), ("Count", int), ("ExcerptPostId", int), ("WikiPostId", int)]
Tags_pandas = create_pandas_dataframe("Tags.xml", types_Tags)

#Users
types_Users = [("Id", int), ("Reputation", int), ("AccountId", int), ("DownVotes", int),
                ("UpVotes", int), ("Views", int), ("CreationDate", fix_date),
                ("LastAccessDate", fix_date)]
Users_pandas = create_pandas_dataframe("Users.xml", types_Users)

#Votes
types_Votes = [("Id", int), ("PostId", int), ("VoteTypeId", int), ("UserId", int),
               ("CreationDate", fix_date),("BountyAmount", int)]
Votes_pandas = create_pandas_dataframe("Votes.xml", types_Votes)


##### print infos about pandas frames
for pandasFrame in [Votes_pandas, Users_pandas, Tags_pandas, Badges_pandas, Comments_pandas,
          PostHistory_pandas, PostLinks_pandas, Post_pandas]:
    print("INFO:")
    print(pandasFrame.info())
    print()
    print("HEAD[1]")
    print(pandasFrame.head(1))
    
    

    

