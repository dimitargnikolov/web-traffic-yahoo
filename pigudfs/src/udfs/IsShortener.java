package udfs;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.pig.FilterFunc;
import org.apache.pig.data.Tuple;
import org.apache.pig.impl.util.UDFContext;

public class IsShortener extends FilterFunc {
	
	private String shortenersPath = null;
	private Set<String> shorteners = null;
	
	private Set<String> loadURLShorteners(FileSystem fs, String filePath) {
		Set<String> shorteners = new HashSet<String>();
		try {
			FSDataInputStream in = fs.open(new Path(filePath));
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			
			String line;
			while((line = br.readLine()) != null) {
				shorteners.add(line.trim());
			}
			br.close();
			return shorteners;
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	
	public IsShortener(String shortenersPath) {
		this.shortenersPath = shortenersPath;
	}
	
	public Boolean exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0 || input.get(0) == null)
			return null;
		
		if (shorteners == null) {
			FileSystem fs = FileSystem.get(UDFContext.getUDFContext().getJobConf());
			shorteners = loadURLShorteners(fs, shortenersPath);
		}
		return shorteners.contains(input.get(0));
	}
}
