import xml.etree.cElementTree as et


def is_svg(file):
    """
    Check if provided file is svg
    """
    file.seek(0)
    tag = None
    try:
        for event, el in et.iterparse(file, ('start',)):
            tag = el.tag
            break
    except et.ParseError:
        pass
    return tag == '{http://www.w3.org/2000/svg}svg'

def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("File not svg")