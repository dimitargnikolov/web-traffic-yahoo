package workers;

import java.util.ArrayList;
import java.util.List;

public class Common {
	public static String[] split(String s, String delimiter) {
		if (s.equals("")) {
			return new String[]{""};
		}
		String[] parts = s.trim().split(delimiter);
		List<String> partsNew = new ArrayList<String>();
		for (String p : parts) {
			if (p != null && !p.trim().equals("")) {
				partsNew.add(p.trim());
			}
		}
		return partsNew.toArray(new String[]{});
	}
	
	public static String joinStrings(String[] strings, String delimiter) {
		String s = "";
		for (int i=0; i<strings.length; i++) {
			s += strings[i];
			if (i < strings.length - 1) {
				s += delimiter;
			}
		}
		return s;
	}
	
	public static boolean isIPAddress(String url) {
		String[] parts = split(url, "\\.");
		if (parts.length == 4) {
			for(String part : parts) {
				try {
					int n = Integer.parseInt(part);
					if (n < 0 || n > 255) {
						return false;
					}
				} catch (NumberFormatException e) {
					return false;
				}
			}
			return true;
		}
		return false;
	}
}
