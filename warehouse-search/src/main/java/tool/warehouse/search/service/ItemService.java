package tool.warehouse.search.service;

import java.io.IOException;

import org.apache.solr.client.solrj.SolrServerException;

import tool.warehouse.common.pojo.WarehouseResult;



public interface ItemService {
	public WarehouseResult importItems() throws SolrServerException, IOException;
}
