package udfs;

import java.io.IOException;
import java.util.Map;

import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;

public class ExtractLinkCountFromJSON extends EvalFunc<Integer> {
	
	public Integer exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0 || input.get(0) == null)
			return null;
		
		String json = (String)input.get(0);
		Map<String, Integer> domains = workers.ExtractDomainsFromJSON.execute(json);
		return domains.size();
	}
}
