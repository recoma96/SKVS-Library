package skvsclient.modules.packet.dataelement;
import skvsclient.modules.packet.exception.*;

public class DataElement {
	
	public enum DataType {
		DT_String, DT_Number, DT_Float
	}
	
	//structType
	public enum StructType {
		ST_Element, ST_Basic, ST_OneSet, ST_MultiSet, ST_DynamicList, ST_StaticList,
		ST_DynamicHashMap, ST_StaticHashMap
	}

	
	private String data;
	private DataType dataType;
	private StructType structType;
	
	public DataElement(String _data, DataType _dataType, StructType _structType) throws TypeException {
		

		switch(_dataType) {
		case DT_String:
		break;
		case DT_Number:
			try {
				Integer.parseInt(_data);
				
			} catch(Exception e) {
				throw new TypeException("DataType is number but, data is not number");
			}
		break;
		case DT_Float:
			try {
				Double.parseDouble(_data);
			} catch(Exception e) {
				throw new TypeException("DataType is float, but,  data is not float");
			}
		break;
		}
		

		this.data = _data; this.dataType = _dataType; this.structType = _structType;
	}
	

	public String getData() { return data; }
	public DataType getDataType() { return dataType; }
	public StructType getStructType() { return structType; }
	
	
}
