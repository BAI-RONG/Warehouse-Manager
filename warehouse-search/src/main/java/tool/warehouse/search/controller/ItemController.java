package tool.warehouse.search.controller;

import java.io.IOException;

import org.apache.solr.client.solrj.SolrServerException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.common.utils.ExceptionUtil;
import tool.warehouse.search.service.ItemService;
@Controller
public class ItemController {
	@Autowired
	private ItemService itemService;
	
	@RequestMapping("/importall")
	@ResponseBody
	public WarehouseResult importAll(){
		try {
			WarehouseResult result = itemService.importItems();
			return result;
		} catch (SolrServerException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return WarehouseResult.build(500, ExceptionUtil.getStackTrace(e));
		}
		
	}
}
