def check_imports():
    result = True
    try:
        import sys
        import shapely

        if (sys.platform.startswith('linux') and 
                not check_if_lower_version(shapely.__version__)):
            return False
         
        from qgis import processing
        
    except:
        result = False
        

    return result


def check_if_lower_version(version : str):
    vers = version.split('.')

    #useless now but maybe they will create a 2.X version one day
    if int(vers[0]) > 1: 
        return False
    
    if int(vers[1][0]) > 5: 
        return False

    return True