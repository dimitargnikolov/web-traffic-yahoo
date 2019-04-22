package udfs;


import java.io.IOException;

import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;

public class NthLevelDomain extends EvalFunc<String> {
	public String exec(Tuple input) throws IOException {
		if (input == null || input.size() != 2 || input.get(0) == null || input.get(1) == null)
			return null;
		
		String url = (String)input.get(0);
		int domainLevel = (Integer)input.get(1);
		
		return workers.NthLevelDomain.execute(url, domainLevel);
	}
}
