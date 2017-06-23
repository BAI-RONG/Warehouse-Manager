package tool.warehouse.service.impl;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import tool.warehouse.common.pojo.EasyUITreeNode;
import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.mapper.ItemCategoryMapper;
import tool.warehouse.pojo.ItemCategory;
import tool.warehouse.pojo.ItemCategoryExample;
import tool.warehouse.pojo.ItemCategoryExample.Criteria;
import tool.warehouse.service.CategoryService;
@Service
public class CategoryServiceImpl implements CategoryService{
	
	@Autowired
	private ItemCategoryMapper itemCategoryMapper;
	@Override
	public List<EasyUITreeNode> getCategoryList(Long parentId) {
		ItemCategoryExample example = new ItemCategoryExample();
		Criteria criteria = example.createCriteria();
		criteria.andParentIdEqualTo(parentId);
		List<ItemCategory> list = itemCategoryMapper.selectByExample(example);
		list.sort(new Comparator<ItemCategory>() {

			@Override
			public int compare(ItemCategory o1, ItemCategory o2) {
				if(o1.getSortOrder()<o2.getSortOrder()){
					return -1;
				}else{
					return 0;	
				}
				
			}
			
		});
		List<EasyUITreeNode> result = new ArrayList<EasyUITreeNode>();
		for(ItemCategory itemCategory:list){
			//创建一个EasyUITreeNode 节点
			EasyUITreeNode node = new EasyUITreeNode();
			node.setId(itemCategory.getId());
			node.setText(itemCategory.getName());
			node.setState(itemCategory.getIsParent()?"closed":"open");
			//添加到列表
			result.add(node);
		}
		
		
		return result;
	}
	
	@Override
	public WarehouseResult updateCategory(Long id, String name) {
		ItemCategoryExample example = new ItemCategoryExample();
		Criteria criteria = example.createCriteria();
		criteria.andIdEqualTo(id);
		ItemCategory item = new ItemCategory();
		item.setName(name);
		item.setUpdated(new Date());
		itemCategoryMapper.updateByExampleSelective(item, example);
		System.out.println(id+name);
		return WarehouseResult.ok();
	}
	@Override
	public WarehouseResult deleteCategory(Long id,Long parentId) {
		delete(id);
		ItemCategoryExample example = new ItemCategoryExample();
		Criteria criteria = example.createCriteria();
		criteria.andParentIdEqualTo(parentId);
		List<ItemCategory> list = itemCategoryMapper.selectByExample(example);
		if(list.isEmpty()){
			ItemCategory parent = itemCategoryMapper.selectByPrimaryKey(parentId);
			parent.setIsParent(false);
			itemCategoryMapper.updateByPrimaryKeySelective(parent);
			return WarehouseResult.ok(false);
		}
		return WarehouseResult.ok(true);
	}
	
	private void delete(Long id){
		ItemCategoryExample example = new ItemCategoryExample();
		Criteria criteria = example.createCriteria();
		criteria.andParentIdEqualTo(id);
		List<ItemCategory> list = itemCategoryMapper.selectByExample(example);
		if(list.isEmpty()){
			itemCategoryMapper.deleteByPrimaryKey(id);
			return;
		}
		for(ItemCategory item:list){
			if(item.getIsParent()){
				delete(item.getId());
			}else{
				itemCategoryMapper.deleteByPrimaryKey(item.getId());
			}
		}
		
		itemCategoryMapper.deleteByPrimaryKey(id);
		return  ;
	}

	@Override
	public WarehouseResult insertCatgory(Long parentId, String name) {
		ItemCategoryExample example = new ItemCategoryExample();
		Criteria criteria = example.createCriteria();
		criteria.andParentIdEqualTo(parentId);
		List<ItemCategory>  list=itemCategoryMapper.selectByExample(example);
		ItemCategory item = new ItemCategory();
		item.setIsParent(false);
		item.setParentId(parentId);
		item.setSortOrder(list.size()+1);
		item.setName(name);
		item.setCreated(new Date());
		item.setUpdated(new Date());
		 itemCategoryMapper.insert(item);
		 Long id = item.getId();
System.out.println("新:"+id);		
		
		criteria.andIdEqualTo(parentId);
		ItemCategory  parentNode= itemCategoryMapper.selectByPrimaryKey(parentId);
		if(!parentNode.getIsParent()){
			parentNode.setIsParent(true);
			//更新父节点
			itemCategoryMapper.updateByPrimaryKey(parentNode);
		}
			
		return WarehouseResult.ok(id);
	
	
	}
}

