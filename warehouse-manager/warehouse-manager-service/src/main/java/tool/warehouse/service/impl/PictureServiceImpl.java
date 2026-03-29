package tool.warehouse.service.impl;

import java.io.IOException;

import org.csource.common.MyException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import tool.warehouse.common.pojo.PictureResult;
import tool.warehouse.common.utils.FastDFSClient;
import tool.warehouse.service.PictureService;


@Service
public class PictureServiceImpl implements PictureService {

	@Value("${image_server_base_url}")
	private String prefixUrl;
	@Override
	public PictureResult uploadPic(MultipartFile picFile) {
		// TODO Auto-generated method stub
		PictureResult result = new PictureResult();
		//判断图片是否为空
		if(picFile.isEmpty()){
			result.setError(1);
			result.setMessage("the picture is null");
			return result;
		}
	
		
		try {
			//取图片的拓展名
			String originalFilename = picFile.getOriginalFilename();
			String extName = originalFilename.substring(originalFilename.lastIndexOf(".")+1);
			//上传到图片服务器
			 
			FastDFSClient client = new FastDFSClient("classpath:properties/client.conf");
			String url=client.uploadFile(picFile.getBytes(), extName);
			//拼接图片服务器的ip地址
			url = prefixUrl+url;
			
			result.setError(0);
			
			result.setUrl(url);
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			
			e.printStackTrace();
			result.setError(1);
			result.setMessage("fail to upload picture");
		} 
		return result;
	}

}
