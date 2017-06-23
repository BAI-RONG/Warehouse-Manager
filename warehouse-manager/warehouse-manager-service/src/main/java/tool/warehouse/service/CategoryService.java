package tool.warehouse.service;

import java.util.List;

import tool.warehouse.common.pojo.EasyUITreeNode;
import tool.warehouse.common.pojo.WarehouseResult;

public interface CategoryService {
	public List<EasyUITreeNode> getCategoryList(Long parentId);
	public WarehouseResult insertCatgory(Long parentId, String name); 
	public WarehouseResult updateCategory(Long id,String name);
	public WarehouseResult deleteCategory(Long id,Long parentId);
}
