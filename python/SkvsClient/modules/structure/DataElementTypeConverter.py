from . import DataElement as de

#서버로부터 받은 정수값을 enum타입으로 바꾸기
class DataTypeConverter:
    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        #값 입력 시작
        if _integer is 0: return de.DataType.DT_String
        elif _integer is 1: return de.DataType.DT_Number
        elif _integer is 2: return de.DataType.DT_Float
        else: raise ValueError("This integer is out of range")
    
    def toInteger(_type):
        if type(_type) != de.DataType:
            raise TypeError("This Value is not DataType")
        if _type is de.DataType.DT_String: return 0
        elif _type is de.DataType.DT_Number: return 1
        elif _type is de.DataType.DT_Float: return 2
        else: raise ValueError("This Type is out of range")

class StructTypeConverter:

    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        if _integer is 0: return de.StructType.ST_Element
        elif _integer is 1: return de.StructType.ST_Basic
        elif _integer is 2: return de.StructType.ST_OneSet
        elif _integer is 3: return de.StructType.ST_MultiSet
        elif _integer is 4: return de.StructType.ST_DynamicList
        elif _integer is 5: return de.StructType.ST_StaticList
        elif _integer is 6: return de.StructType.ST_DynamicHashMap
        elif _integer is 7: return de.StructType.ST_StaticHashMap
        else: raise ValueError("This integer is out of range")

    def toInteger(_type):
        if type(_type) != de.StructType:
            raise TypeError("This Value is not StructType")
        if _type is de.StructType.ST_Element: return 0
        elif _type is de.StructType.ST_Basic: return 1
        elif _type is de.StructType.ST_OneSet: return 2
        elif _type is de.StructType.ST_MultiSet: return 3
        elif _type is de.StructType.ST_DynamicList: return 4
        elif _type is de.StructType.ST_StaticList: return 5
        elif _type is de.StructType.ST_DynamicHashMap: return 6
        elif _type is de.StructType.ST_StaticHashMap: return 7
        else: raise ValueError("This Type is out of range")
        
        

