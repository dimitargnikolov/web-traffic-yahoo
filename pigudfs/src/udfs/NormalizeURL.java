package udfs;

import java.io.IOException;

import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;

public class NormalizeURL extends EvalFunc<String> {
	public String exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0 || input.get(0) == null)
			return null;
		
		String url = (String)input.get(0);
		
		return workers.NormalizeURL.execute(url);
	}
}
