package skvsclient;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.ListIterator;

public class SkvsReadStream {
	
	private ArrayList<HashMap<String, String>> resultData;
	private ListIterator<HashMap<String, String>> cursor;
	
	
	protected SkvsReadStream(ArrayList<HashMap<String, String>> _resultData) {
		resultData = _resultData;
		cursor = resultData.listIterator();
	}
	
	
	public boolean front() {
		if(resultData.isEmpty())
			return false;

		while(cursor.hasPrevious())
			cursor.previous();
		return true;
	}
	
	public boolean end() {
		if(resultData.isEmpty())
			return false;
		while(cursor.hasNext())
			cursor.next();
		return true;
	}
	
	public HashMap<String, String> read() {
		if(resultData.isEmpty())
			return null;
		if(!cursor.hasNext()) return null;
		return cursor.next();
	}
	public HashMap<String, String> readBack() {
		if(resultData.isEmpty()) return null;
		if(!cursor.hasPrevious()) return null;
		return cursor.previous();
	}

	
	
}
