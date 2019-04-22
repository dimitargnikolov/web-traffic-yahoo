package udfs;

import java.io.IOException;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.pig.EvalFunc;
import org.apache.pig.data.BagFactory;
import org.apache.pig.data.DataBag;
import org.apache.pig.data.Tuple;
import org.apache.pig.data.TupleFactory;

public class ExtractDomainsFromJSON extends EvalFunc<DataBag> {
	private static final TupleFactory tupleFactory = TupleFactory.getInstance();
	private static final BagFactory bagFactory = BagFactory.getInstance();
	
	public DataBag exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0 || input.get(0) == null)
			return null;
		
		String json = (String)input.get(0);
		Map<String, Integer> domains = workers.ExtractDomainsFromJSON.execute(json);
		Iterator<Entry<String, Integer>> it = domains.entrySet().iterator();
		DataBag bag = bagFactory.newDefaultBag();
	    while (it.hasNext()) {
	    	Entry<String, Integer> pair = it.next();
	    	Tuple t = tupleFactory.newTuple();
	    	t.append(pair.getKey());
	        bag.add(t);
	    }
	    return bag;
	}
}
