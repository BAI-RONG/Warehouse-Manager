package tool.warehouse.search.dao.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.SolrServer;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import tool.warehouse.search.dao.SearchDao;
import tool.warehouse.search.pojo.SearchItem;
import tool.warehouse.search.pojo.SearchResult;

@Repository
public class SearchDaoImpl implements SearchDao {
	@Autowired
	private SolrServer solrServer;
	
	
	@Override
	public SearchResult search(SolrQuery query) throws Exception {
		//执行查询
		QueryResponse response = solrServer.query(query);
		//取查询结果的列表
		SolrDocumentList solrDocumentList = response.getResults();
		List<SearchItem> itemList = new ArrayList<>();
		for(SolrDocument solrDocument:solrDocumentList){
			//创建一个SearchItem对象
			SearchItem item = new SearchItem();
			item.setCategory_name((String)solrDocument.get("tool_category_name"));
			item.setId((String)solrDocument.get("id"));
			item.setImage((String)solrDocument.get("tool_image"));
			item.setPrice((Long)solrDocument.get("tool_price"));
			//取高亮显示
			Map<String,Map<String,List<String>>> highlighting = response.getHighlighting();
			List<String> list = highlighting.get(solrDocument.get("id")).get("tool_name");
			String itemTitle = "";
			if(list != null && list.size()>0){
				//取高亮后的结果
				itemTitle = list.get(0);
			}else{
				itemTitle = (String)solrDocument.get("tool_name");
			}
			item.setName(itemTitle);
			//添加到列表
			itemList.add(item);
		}
		SearchResult result = new SearchResult();
		result.setItemList(itemList);
		//查询结果总数量
		result.setResordCount(solrDocumentList.getNumFound());
		return result;
	}

}
