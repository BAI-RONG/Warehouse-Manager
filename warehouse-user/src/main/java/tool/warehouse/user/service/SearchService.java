package tool.warehouse.user.service;

import tool.warehouse.user.pojo.SearchResult;

public interface SearchService {
	public SearchResult search(String keyword,int page,int rows);
	
	
}
