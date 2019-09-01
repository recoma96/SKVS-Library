package skvsclient.modules.packet.dataelement;

import skvsclient.modules.packet.dataelement.DataElement.DataType;
import skvsclient.modules.packet.dataelement.DataElement.StructType;
import skvsclient.modules.packet.exception.*;

public class TypePrinter {
	

	

	public static String aboutDataType(DataElement.DataType _dataType) {
			
		switch(_dataType) {
		case DT_String: return "string";
		case DT_Number: return "number";
		case DT_Float: return "float";
		default: return null;
		}
	}
	public static String aboutStructType(DataElement.StructType _structType) {
		switch(_structType) {
		case ST_Element: return "element";
		case ST_Basic: return "basic";
		case ST_OneSet: return "oneset";
		case ST_MultiSet: return "multiset";
		case ST_DynamicList: return "dynamiclist";
		case ST_StaticList: return "staticlist";
		case ST_DynamicHashMap: return "dynamichashmap";
		case ST_StaticHashMap: return "statichashmap";
		default: return null;
		}
	}
}
