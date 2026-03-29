package tool.warehouse.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.pojo.Item;
import tool.warehouse.service.ItemService;

@Controller
public class ItemController {
		@Autowired
		private ItemService itemService;
		@RequestMapping(value="/item/save",method=RequestMethod.POST)
		@ResponseBody
		public  WarehouseResult itemCreate(Item item,String desc){
			WarehouseResult result =itemService.createItem(item, desc);
			return result;
			
		} 
}
