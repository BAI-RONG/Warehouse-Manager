package tool.warehouse.search.service.impl;

import java.io.IOException;
import java.util.List;

import org.apache.solr.client.solrj.SolrServer;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrServer;
import org.apache.solr.common.SolrInputDocument;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.search.mapper.ItemMapper;
import tool.warehouse.search.pojo.SearchItem;
import tool.warehouse.search.service.ItemService;
@Service
public class ItemServiceImpl implements ItemService{

	@Autowired
	private SolrServer solrServer;
	@Autowired
	private ItemMapper itemMapper;
	@Override
	public WarehouseResult importItems() throws SolrServerException, IOException {
		System.out.println("coming in");
		//查询数据库获得列表
		List<SearchItem> itemList = itemMapper.getItemList();
		//遍历列表
		for(SearchItem item:itemList){
			//创建文档对象
			SolrInputDocument document = new SolrInputDocument();
			//添加域
			document.addField("id", item.getId());
			document.addField("tool_name", item.getName());
			document.addField("tool_price", item.getPrice());
			document.addField("tool_image", item.getImage());
			document.addField("tool_category_name", item.getCategory_name());	
			document.addField("tool_desc", item.getItem_desc());
			//写入索引库
			solrServer.add(document);

		}
		//提交
		solrServer.commit();
		
		return WarehouseResult.ok();
	}
	
}
