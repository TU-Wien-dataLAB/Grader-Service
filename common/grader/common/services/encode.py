import base64

#for strings
def encodeStrings(content: str) -> str:
    asciicontent = content.encode('ascii')
    encodedContent = base64.b64encode(asciicontent)
    #make it human readable
    encodedContent = encodedContent.decode('ascii')
    return encodedContent

#for binaries
def encodeBinary(binary) -> str:
    encodedContent = base64.b64encode(binary)
    #make it human readable
    encodedContent = encodedContent.decode('utf-8')
    return encodedContent

def decodeStrings(encoded: str) -> str:
    base64bytes = encoded.encode('ascii')
    decoded = base64.b64decode(base64bytes)
    content = decoded.decode('ascii')
    return content

def decodeBinary(encoded: str):
    filebytes = encoded.encode('utf-8')
    binary = base64.decodebytes(filebytes)
    return binary
