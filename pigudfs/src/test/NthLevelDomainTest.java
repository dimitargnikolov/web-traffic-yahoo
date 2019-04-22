package test;


import junit.framework.Assert;

import org.junit.Test;

public class NthLevelDomainTest {
	@Test
    public void testNthLevelDomain() {
		Assert.assertEquals(
			workers.NthLevelDomain.execute("", 2),
			"");
		Assert.assertEquals(
			workers.NthLevelDomain.execute("facebook.com", 1),
			"com");
		Assert.assertEquals(
			workers.NthLevelDomain.execute("facebook.com", 2),
			"facebook.com");
		Assert.assertEquals(
			workers.NthLevelDomain.execute("facebook.com", 3),
			"facebook.com");
		Assert.assertEquals(
			workers.NthLevelDomain.execute("indiana.facebook.com", 2),
			"facebook.com");
    }
}
