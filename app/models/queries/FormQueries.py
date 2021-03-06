from app.models import Forms
from app.models import Files
from app.models import Galleries
from app.config.loadConfig import get_cfg 
from app.logic.validation import*


def exists(fid, include_deleted=False):
    if include_deleted:
        return Forms.select().where(Forms.fid == fid).exists()
    else:
        return Forms.select().where(Forms.fid == fid).where(Forms.status != "Deleted").exists()


def get_all_from_gallery(gid, include_deleted = False):
    """ Retrieves all form object for a single gallery

    Args:
        gid (int): The gid of the gallery model to retrieve forms from

    Returns:
        Forms (list): A list of the form objects for a gallery
        None: If the gallery object does not exist
    """

    if type(gid) is int:
        if Galleries.select().where(Galleries.gid == gid).exists():
            if include_deleted:
                forms = Forms.select().join(Galleries).where(Galleries.gid == gid)
            else:
                forms = Forms.select().join(Galleries).where(Galleries.gid == gid).where(Forms.status != "Deleted")
            print("Got all forms")
            return list(forms)
    return None



def get(fid):
    """ Retrieves a single Form object

    Args:
        fid (int): The fid of the Form model to retrieve 

    Returns:
        Form: The Form object if it exists
        None: If the Form object does not exist
    """

    if type(fid) is int:
        if Forms.select().where(Forms.fid == fid).exists():
            return Forms.get(Forms.fid == fid)
    return None

def select_all(self, include_deleted=False):
    '''This method is to select all the forms stored in the database'''
    try:
        if include_deleted:
            forms = Forms.select()
        else:
            forms = Forms.select().where(Forms.status != "Deleted")
        return forms
    except Exception as e:
        print (e)
        return False


def select_single(fid):
    '''This function is to select a single form from the database using the unique identifier (FID) associated with that form'''
    try:
        form = Forms.get(Form.fid == fid)
        return form
    except Exception as e:
        print (e)
        return False

def insert(first_name, last_name, street_address, second_address,city, state, zip_code, email, phone_number, website, gallery,cv, personal_statement, submit_date, status, folder_path):
    '''This function is to store the inputs received from the application form into the database'''
    try:
        form, created = Forms.get_or_create(   email=email,
                        defaults={
                            "first_name":first_name,
                            "last_name":last_name,
                            "street_address":street_address,
                            "second_address":second_address,
                            "city":city,
                            "state":state,
                            "zip_code":zip_code,
                            "phone_number":phone_number,
                            "website":website,
                            "gallery":gallery,
                            "submit_date":submit_date,
                            "cv":cv,
                            "personal_statement":personal_statement,
                            "folder_path":folder_path,
                            "status":status,
                        }
                    )
        form.save()
        if not created:
            folder_path = form.folder_path
            cv = form.cv
            personal_statement = form.personal_statement
            if form.status == "Deleted":
                folder_path = None
                cv = None
                personal_statement = None

            update = Forms.update({
                            "first_name":first_name,
                            "last_name":last_name,
                            "street_address":street_address,
                            "second_address":second_address,
                            "city":city,
                            "state":state,
                            "zip_code":zip_code,
                            "phone_number":phone_number,
                            "website":website,
                            "gallery":gallery,
                            "cv":cv,
                            "personal_statement":personal_statement,
                            "folder_path":folder_path,
                            "submit_date":submit_date,
                            "status":status,
                            }
                        ).where(Forms.email == email)
            update.execute()
        return form
    except Exception as e:
        return e
    return False

def insert_attachment_file(doc_type, fid, filename, filepath, filetype):
    '''This method is to store attachment files such as CVs and personal statements into the database'''
    form = Forms.get(Forms.fid == fid)
    file = Files(filepath = filepath, filename=filename, filetype = filetype)
    file.save()
    if doc_type == "cv":
        try:
            form.cv = file
        except Exception as e:
            print (e)
            return False
    if doc_type =="statement":
        try:
            form.personal_statement = file
        except Exception as e:
            print (e)
            return False
    form.save()
    return form
    

def get_cv(fid):
    form = get(fid)
    if form is not None:
        if form.cv is not None:
            return form.cv
    return None

def get_statement(fid):
    form = get(fid)
    if form is not None:
        if form.personal_statement is not None:
            return form.personal_statement
    return None

def update_status_all(gid,status="Deleted"):
    if Forms.select().where(Forms.gallery == gid).exists():
        forms = Forms.update({Forms.status: status}).where(Forms.gallery == gid)
        print(forms.execute())
        return forms


