from .DataElement import *
from .DataElementTypeConverter import *

strData = DataElement("string", DataType.DT_String, StructType.ST_Element)
copiedData = DataElement("string", DataType.DT_String, StructType.ST_Basic)

if strData == copiedData:
    print("ok")

print(DataTypeConverter.toType(1))