package tool.warehouse.service;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.pojo.Item;

public interface ItemService {
	WarehouseResult createItem(Item item,String desc);
}
