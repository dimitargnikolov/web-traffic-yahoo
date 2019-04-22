package workers;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class NormalizeURL {
	
	public static String execute(String url) {
		if (url.indexOf("://") != -1) {
			url = url.substring(url.indexOf("://") + 3);
		}
		
		if (url.indexOf(":") != -1) {
			url = url.substring(0, url.indexOf(":"));
		}
		
		if (url.indexOf("/") != -1) {
			url = url.substring(0, url.indexOf("/"));
		}
		
		if (url.indexOf("?") != -1) {
			url = url.substring(0, url.indexOf("?"));
		}
		
		boolean urlIsClean = false;
		while (!urlIsClean) {
			if (url.startsWith("www.")) {
				url = url.substring(4);
			} else if (url.startsWith("www2.") || url.startsWith("www3.")) {
				url = url.substring(5);
			} else {
				urlIsClean = true;
			}
		}
		
		Pattern pattern = Pattern.compile("[^a-zA-Z0-9\\.\\-]");
        Matcher matcher = pattern.matcher(url);
		if (matcher.find()) {
			return "";
		} else if (url.indexOf(".") == -1) {
			return "";
		} else {
			return url.toLowerCase();
		}
	}
}
