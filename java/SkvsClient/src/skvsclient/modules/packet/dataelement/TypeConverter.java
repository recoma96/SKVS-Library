package skvsclient.modules.packet.dataelement;

import skvsclient.modules.packet.dataelement.DataElement.DataType;
import skvsclient.modules.packet.dataelement.DataElement.StructType;
import skvsclient.modules.packet.exception.*;

public class TypeConverter {
	
	//1.datatype
	public static class DataTypeConverter {
		
		public static int toInteger(DataElement.DataType _dataType) {

			if(_dataType == DataElement.DataType.DT_String) return 0;
			else if(_dataType == DataElement.DataType.DT_Number) return 1;
			else return 2;
		}
		

		public static DataType toType(int _num) throws ConvertException {
			switch(_num) {
			case 0:
				return DataElement.DataType.DT_String;
			case 1:
				return DataElement.DataType.DT_Number;
			case 2:
				return DataElement.DataType.DT_Float;
			default:
				throw new ConvertException("This number is out of range to convert datatype");

			}
		}
	}
	
	//2.Struct type
	public static class StructTypeConverter {
		

		public static int toInteger(DataElement.StructType _structType) {
			
			switch(_structType) {
			case ST_Element: return 0;
			case ST_Basic: return 1;
			case ST_OneSet: return 2;
			case ST_MultiSet: return 3;
			case ST_DynamicList: return 4;
			case ST_StaticList: return 5;
			case ST_DynamicHashMap: return 6;
			case ST_StaticHashMap: return 7;
			default: return -1;
			}
		}
		

		public static StructType toType(int _num) throws ConvertException {
			switch(_num) {
			case 0: return DataElement.StructType.ST_Element;
			case 1: return DataElement.StructType.ST_Basic;
			case 2: return DataElement.StructType.ST_OneSet;
			case 3: return DataElement.StructType.ST_MultiSet;
			case 4: return DataElement.StructType.ST_DynamicList;
			case 5: return DataElement.StructType.ST_StaticList;
			case 6: return DataElement.StructType.ST_DynamicHashMap;
			case 7: return DataElement.StructType.ST_StaticHashMap;
			default: throw new ConvertException("This number is out of range to convert structtype");
			}
		}
	
	}
}
