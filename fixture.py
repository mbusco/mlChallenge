def getOwnerDisplayName(item): # Devuelve el nombre del owner de un archivo
    return ((item.get('owners',[]))[0]).get('displayName',[])

def getOwnerEmailAddress(item): # Devuelve el correo electrónico del owner de un archivo
    return ((item.get('owners',[]))[0]).get('emailAddress',[])

def getItemId(item): # Devuelve el ID del archivo
    return item.get('id',[])

def getName(item): # Devuelve el nombre del archivo
    return item.get('name',[])

def getLastChangeDate(item): # Devuelve la última fecha en la que se modifico el archivo
    return item.get('modifiedTime',[])

def getFileExtension(item): # Devuelve la extensión del archivo si es externo
    return item.get('fileExtension','DriveInternalFile')

def getFileAccess(item): # Devuelve los permisos al archivo
    permissionsList = (item.get('permissions',[]))
    listOfGrants = []
    for permissions in permissionsList:
        listOfGrants.append(permissions.get('type'))
    return ('anyone' in listOfGrants) or ('anyoneWithLink' in listOfGrants)


