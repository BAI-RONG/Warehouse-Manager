package tool.warehouse.service.impl;

import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.mapper.ItemDescMapper;
import tool.warehouse.mapper.ItemMapper;
import tool.warehouse.pojo.Item;
import tool.warehouse.pojo.ItemDesc;
import tool.warehouse.service.ItemService;
@Service
public class ItemServiceImpl implements ItemService {

	@Autowired
	private ItemMapper itemMapper;
	@Autowired
	private ItemDescMapper itemDescMapper;
	@Override
	public WarehouseResult createItem(Item item, String desc) {
		item.setCreated(new Date());
		item.setUpdated(new Date());
		itemMapper.insert(item);
	Long id = item.getId();
	ItemDesc Desc = new ItemDesc();
	Desc.setItemDesc(desc);
	Desc.setId(id);
	Desc.setCreated(new Date());
	Desc.setUpdated(new Date());
	itemDescMapper.insert(Desc);
	
		return WarehouseResult.ok();
	}

}
