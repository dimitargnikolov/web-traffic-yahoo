package workers;

public class NthLevelDomain {
	public static String execute(String url, int domainLevel) {
		url = workers.NormalizeURL.execute(url);
		if (Common.isIPAddress(url)) {
			return url;
		} else {
			String[] parts = workers.Common.split(url, "\\.");
			if (parts.length <= domainLevel) {
				return workers.Common.joinStrings(parts, ".");
			} else {
				String newUrl = "";
				int count = 0;
				while (count != domainLevel) {
					newUrl = parts[parts.length - count - 1] + newUrl;
					count++;
					if (count != domainLevel) {
						newUrl = "." + newUrl;
					}
				}
				return newUrl;
			}
		}
	}
}
