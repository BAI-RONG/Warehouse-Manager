package tool.warehouse.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import com.alibaba.druid.support.json.JSONUtils;

import tool.warehouse.common.pojo.PictureResult;
import tool.warehouse.common.utils.JsonUtils;
import tool.warehouse.service.PictureService;
import tool.warehouse.service.impl.PictureServiceImpl;


@Controller
public class pictureController {
		@Autowired
		private PictureService pictureService;
		
		@RequestMapping("/pic/upload")
		@ResponseBody
		public String uploadFile(MultipartFile uploadFile){
			PictureResult result = pictureService.uploadPic(uploadFile);
			System.out.println(result);
			String json = JsonUtils.objectToJson(result);
			return json;
		}
		
}
