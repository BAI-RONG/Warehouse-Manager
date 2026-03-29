package tool.warehouse.common.utils;

import java.io.FileNotFoundException;
import java.io.IOException;

import org.csource.common.MyException;
import org.csource.common.NameValuePair;
import org.csource.fastdfs.ClientGlobal;
import org.csource.fastdfs.StorageClient;
import org.csource.fastdfs.StorageClient1;
import org.csource.fastdfs.StorageServer;
import org.csource.fastdfs.TrackerClient;
import org.csource.fastdfs.TrackerServer;

public class FastDFSClient {
	private TrackerClient trackerClient  = null;
	private TrackerServer trackerServer = null;
	private StorageServer storageServer = null;
	private StorageClient1 storageClient = null;
	
	public FastDFSClient(String conf) throws Exception, IOException, MyException{
		if(conf.contains("classpath:")){
			conf = conf.replace("classpath:", this.getClass().getResource("/").getPath());
		}
		ClientGlobal.init(conf);
		trackerClient = new TrackerClient();
		trackerServer = null;
		storageServer = null;
		storageClient = new StorageClient1(trackerServer,storageServer);
	}
	
	public String uploadFile(String fileName,String extName,NameValuePair[] metas) throws IOException, MyException{
		String result = storageClient.upload_file1(fileName, extName, metas);
		return result;
		
	}
	
	public String uploadFile(String fileName) throws IOException, MyException{
		return uploadFile(fileName,null,null);
	}
	
	public String uploadFile(String fileName,String extName) throws IOException, MyException{
		return uploadFile(fileName,extName,null);
	}
	
	public String uploadFile(byte[] fileContent,String extName,NameValuePair[] metas) throws IOException, MyException{
		String result = storageClient.upload_file1(fileContent,extName,metas);
		return result;
	}
	
	public String uploadFile(byte[] fileContent) throws IOException, MyException{
		return uploadFile(fileContent,null,null);
	}
	public String uploadFile(byte[] fileContent,String extName) throws IOException, MyException{
		return uploadFile(fileContent,extName,null);
	}
}
