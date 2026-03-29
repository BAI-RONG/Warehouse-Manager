package tool.warehouse.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import tool.warehouse.common.pojo.EasyUITreeNode;
import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.service.CategoryService;

@Controller
@RequestMapping("/category")
public class CategoryController {
	@Autowired
	private CategoryService categoryService;
	@RequestMapping("/list")
	@ResponseBody
	private List<EasyUITreeNode> getCategoryList(@RequestParam(value="id",defaultValue="0")Long parentId){
		System.out.println("tree:"+parentId);
		List<EasyUITreeNode> list = categoryService.getCategoryList(parentId);
		return list;
	}
	
	@RequestMapping("/create")
	@ResponseBody
	public WarehouseResult createNode(Long id,String name){
		 WarehouseResult result=categoryService.insertCatgory(id, name);
		return result;
	}
	
	@RequestMapping("/update")
	@ResponseBody
	public WarehouseResult updateNode(Long id,String name){
		WarehouseResult result= categoryService.updateCategory(id, name);
		return result;
	}
	
	@RequestMapping("/delete")
	@ResponseBody
	public WarehouseResult deleteNode(Long id,Long parentId){
		WarehouseResult result=categoryService.deleteCategory(id,parentId);
		return result;
	}
	
}
