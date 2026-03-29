package tool.warehouse.search.service;

import tool.warehouse.search.pojo.SearchResult;

public interface SearchService {
	public SearchResult search(String queryString,int page,int rows) throws Exception;
}
