import re


def validate_tag(tag: str) -> str:
    """
    TODO: Implement A Regex for this validation
    Name components may contain lowercase letters, digits and separators.
    A separator is defined as a period, one or two underscores, or one or more dashes.
    A name component may not start or end with a separator.v
    https://docs.docker.com/engine/reference/commandline/tag/#extended-description
    """
    tag = tag.lower()

    print(tag)
    return re.sub('[!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ \t\n\r\x0b\x0c]', '', tag)
