package tool.warehouse.search.service.impl;

import org.apache.solr.client.solrj.SolrQuery;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.warehouse.search.dao.SearchDao;
import tool.warehouse.search.pojo.SearchResult;
import tool.warehouse.search.service.SearchService;
@Service
public class SearchServiceImpl implements SearchService {

	@Autowired
	private SearchDao searchDao;
	@Override
	public SearchResult search(String queryString, int page, int rows) throws Exception {
		//创建条件
		SolrQuery query = new SolrQuery();
		//设置查询条件
		query.setQuery(queryString);
		//设置分页条件
		query.setStart((page-1)*rows);
		query.setRows(rows);
		//设置默认搜索域
		query.set("df", "tool_name");
		//设置高亮
		query.setHighlight(true);
		query.addHighlightField("name");
		query.setHighlightSimplePre("<font class=\"skcolor_lig\">");
		query.setHighlightSimplePost("</font>");
		//执行查询
		SearchResult searchResult = searchDao.search(query);
		//计算总页数
		Long recordCount = searchResult.getResordCount();
		int pageCount = (int) (recordCount/rows);
		if(recordCount % rows >0 ){
			pageCount++;
		}
		searchResult.setPageCount(page);
		searchResult.setCurPage(page);
		return searchResult;
	}

}
