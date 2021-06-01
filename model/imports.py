
def check_imports():
    result = True
    try:
        import shapely
        # etc
    except:
        result = False

    return result