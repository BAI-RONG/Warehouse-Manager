package tool.warehouse.user.service.impl;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.common.utils.HttpClientUtil;
import tool.warehouse.user.pojo.SearchResult;
import tool.warehouse.user.service.SearchService;
@Service
public class SearchServiceImpl implements SearchService{

	@Value("${SEARCH_BASE_URL}")
	private String SEARCH_BASE_URL;
	
	@Override
	public SearchResult search(String keyword, int page, int rows) {
		//调用服务查询商品列表
		Map<String,String> param = new HashMap<>();
		param.put("keyword", keyword);
		param.put("page", page+"");
		param.put("rows", rows+"");
		//调用服务
		String json = HttpClientUtil.doGet(SEARCH_BASE_URL,param);
		//转换成java对象
		WarehouseResult warehouseResult = WarehouseResult.formatToPojo(json, SearchResult.class);
		//取返回的结果
		SearchResult searchResult = (SearchResult) warehouseResult.getData();
		
		return searchResult;
	}

}
