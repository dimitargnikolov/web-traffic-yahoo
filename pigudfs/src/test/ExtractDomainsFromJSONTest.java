package test;

import java.util.HashMap;
import java.util.Map;

import junit.framework.Assert;

import org.junit.Test;

public class ExtractDomainsFromJSONTest {
	
	@Test
    public void test1() {
		String json = "{\"Links\": [{\"AnchorText\": [\"Test\"], \"Url\": \"www.test.com\"}, {\"AnchorText\": [\"Blub\"], \"Url\": \"www.blub.com\"}]}";
		Map<String, Integer> actual = workers.ExtractDomainsFromJSON.execute(json);
		Map<String, Integer> expected = new HashMap<String, Integer>();
		expected.put("test.com", 1);
		expected.put("blub.com", 1);
		Assert.assertEquals(
			actual, 
			expected
		);
    }
	
	@Test
    public void test2() {
		String json = "{\"Links\": [{\"AnchorText\": [\"Test\"], \"Url\": \"www.test.com\"}, {\"AnchorText\": [\"Blub\"], \"Url\": \"www.blub.com\"}, {\"AnchorText\": [\"Blub\"], \"Url\": \"www.blub.com/abc.html\"}]}";
		Map<String, Integer> actual = workers.ExtractDomainsFromJSON.execute(json);
		Map<String, Integer> expected = new HashMap<String, Integer>();
		expected.put("test.com", 1);
		expected.put("blub.com", 2);
		Assert.assertEquals(
			actual, 
			expected
		);
    }
	
	@Test
	public void test3() {
		String json = "{\"Links\": []}";
		Assert.assertEquals(
			workers.ExtractDomainsFromJSON.execute(json), 
			new HashMap<String, Integer>()
		);
	}
}
