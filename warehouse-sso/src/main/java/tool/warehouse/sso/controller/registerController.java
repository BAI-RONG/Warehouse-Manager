package tool.warehouse.sso.controller;

import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.pojo.User;
import tool.warehouse.sso.service.RegisterService;

@Controller
@RequestMapping("/user")
public class registerController {
   @Autowired
   private RegisterService registerService;
   
   @RequestMapping("/check/{id}")
   @ResponseBody
   public WarehouseResult  checkData(@PathVariable String id){
	   WarehouseResult result = registerService.checkData(id);
	   return result;
   }
   @RequestMapping(value="/register",method=RequestMethod.POST)
   @ResponseBody
   public WarehouseResult register(User user){
	   System.out.println(user);
	   
	   WarehouseResult result = registerService.register(user);
	   return result;
   }
}
