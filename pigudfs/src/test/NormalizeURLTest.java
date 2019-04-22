package test;


import junit.framework.Assert;

import org.junit.Test;

public class NormalizeURLTest {
	@Test
    public void testNormalizeURL() {
		Assert.assertEquals(
			workers.NormalizeURL.execute("cess&holdingsbarcode=next available&holdingsnote=&inhonorof=&inmemoryof=&itemid=149441&kitinformation=&locationcode=1&numcopies=1&pagename=addeditholdingsrec.html&purchasedate=02"),
			"");
		Assert.assertEquals(
			workers.NormalizeURL.execute("ztfwhuf0zpalpp+ngf0dnavoc6j+o4z3k3vjwb5wyb6ygr9z7kuok6rhdcjj1psjr"),
			"");
		Assert.assertEquals(
			workers.NormalizeURL.execute("http://https://test.com"),
			"");
		Assert.assertEquals(
			workers.NormalizeURL.execute("http://test.com/index?test=1"),
			"test.com");
		Assert.assertEquals(
			workers.NormalizeURL.execute("http://indiana.facebook.com/dir1/page.html"),
			"indiana.facebook.com");
		Assert.assertEquals(
			workers.NormalizeURL.execute("http://test.com?site=https://other.com"),
			"test.com");
		Assert.assertEquals(
			workers.NormalizeURL.execute("https://facebook.com"),
			"facebook.com");
		Assert.assertEquals(
			workers.NormalizeURL.execute("http://www.facebook.com:80/"),
			"facebook.com");
		Assert.assertEquals(
			workers.NormalizeURL.execute("twitter.com"),
			"twitter.com");
    }
}
