import enum

#DataType
class DataType(enum.Enum):
    DT_String = 0
    DT_Number = 1
    DT_Float = 2

class StructType(enum.Enum):
    ST_Element = 0
    ST_Basic = 1
    ST_OneSet = 2
    ST_MultiSet = 3
    ST_DynamicList = 4
    ST_StaticList = 5
    ST_DynamicHashMap = 6
    ST_StaticHashMap = 7

class DataElement:
    def __init__(self, _data, _dataType, _structType):

        #데이터타입 스트럭트 타입 매칭 판정
        if type(_dataType) != DataType:
             raise TypeError("dataType's type is not Datatype")
        if type(_structType) != StructType:
            raise TypeError("structType's type is not StructType")

        #data와 _dataType 매칭 판정
        if _dataType == DataType.DT_Number:
            if type(_data) != int:
                raise TypeError("DataType is number. but, Data is not integer")
        elif _dataType == DataType.DT_Float:
            if type(_data) != float:
                raise TypeError("DataType is float. but, Data is not float")
        elif _dataType == DataType.DT_String:
            if type(_data) != str:
                raise TypeError("DataType is string. but, Data is not string")
        else:
            raise TypeError("Datatype over range.")
        #판정 끝
        self.data = _data; self.dataType = _dataType; self.structType = _structType
    
    #연산자 오버로딩 ==
    def __eq__(self, other):
        if type(other) != DataElement:
            return False
        if self.data == other.data and self.dataType == other.dataType:
            return True
        else:
            return False

           
