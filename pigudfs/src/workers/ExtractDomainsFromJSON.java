package workers;

import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class ExtractDomainsFromJSON {
	
	public static Map<String, Integer> execute(String jsonString) {
		Map<String, Integer> domains = new HashMap<String, Integer>();
		JSONParser parser = new JSONParser();
		try {
			JSONObject json = (JSONObject)parser.parse(jsonString);
			JSONArray links = (JSONArray)json.get("Links");
			for (int i=0; i<links.size(); i++) {
				JSONObject link = (JSONObject)links.get(i);
				String domain = NormalizeURL.execute((String)link.get("Url"));
				if (domain != null && !domain.equals("")) {
					if (domains.containsKey(domain)) {
						domains.put(domain, domains.get(domain) + 1);
					} else {
						domains.put(domain, 1);
					}
				}
			}
		} catch (ParseException pe) {
		}
		return domains;
	}
}
