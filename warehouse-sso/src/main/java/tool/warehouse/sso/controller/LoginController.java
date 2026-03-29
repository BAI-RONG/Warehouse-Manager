package tool.warehouse.sso.controller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.sso.service.LoginService;

@Controller
public class LoginController {
	@Autowired
	private LoginService loginService;
	
	@RequestMapping(value="/user/login",method=RequestMethod.POST)
	@ResponseBody
	public WarehouseResult Login(String id,String password,HttpServletRequest request,HttpServletResponse response){
		WarehouseResult result = loginService.Login(id, password, request, response);
		return result;
		
	}
	@RequestMapping(value="/user/token/{token}")
	@ResponseBody
	public WarehouseResult getUserBytoken(@PathVariable String token){
		WarehouseResult result =  loginService.getUserByToken(token);
		return result;
		
	}
	
}
