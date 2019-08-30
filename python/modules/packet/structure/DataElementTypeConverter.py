from .DataElement import *



#서버로부터 받은 정수값을 enum타입으로 바꾸기
class DataTypeConverter:
    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        #값 입력 시작
        if _integer is 0: return DataType.DT_String
        elif _integer is 1: return DataType.DT_Number
        elif _integer is 2: return DataType.DT_Float
        else: raise ValueError("This integer is out of range")
    
    def toInteger(_type):
        if type(_type) != DataType:
            raise TypeError("This Value is not DataType")
        if _type is DataType.DT_String: return 0
        elif _type is DataType.DT_Number: return 1
        elif _type is DataType.DT_Float: return 2
        else: raise ValueError("This Type is out of range")

class StructTypeConverter:

    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        if _integer is 0: return StructType.ST_Element
        elif _integer is 1: return StructType.ST_Basic
        elif _integer is 2: return StructType.ST_OneSet
        elif _integer is 3: return StructType.ST_MultiSet
        elif _integer is 4: return StructType.ST_DynamicList
        elif _integer is 5: return StructType.ST_StaticList
        elif _integer is 6: return StructType.ST_DynamicHashMap
        elif _integer is 7: return StructType.ST_StaticHashMap
        else: raise ValueError("This integer is out of range")

    def toInteger(_type):
        if type(_type) != StructType:
            raise TypeError("This Value is not StructType")
        if _type is StructType.ST_Element: return 0
        elif _type is StructType.ST_Basic: return 1
        elif _type is StructType.ST_OneSet: return 2
        elif _type is StructType.ST_MultiSet: return 3
        elif _type is StructType.ST_DynamicList: return 4
        elif _type is StructType.ST_StaticList: return 5
        elif _type is StructType.ST_DynamicHashMap: return 6
        elif _type is StructType.ST_StaticHashMap: return 7
        else: raise ValueError("This Type is out of range")
        
        

