package tool.warehouse.search.dao;

import org.apache.solr.client.solrj.SolrQuery;

import tool.warehouse.search.pojo.SearchResult;

public interface SearchDao {
	public SearchResult search(SolrQuery query) throws Exception;
}
