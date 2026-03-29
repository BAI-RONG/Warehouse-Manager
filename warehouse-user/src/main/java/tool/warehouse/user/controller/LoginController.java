package tool.warehouse.user.controller;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import tool.warehouse.user.component.JedisClient;
import tool.warehouse.user.service.UserService;

@Controller
public class LoginController {
	@Autowired
	private UserService userService;
	@RequestMapping("/logout")
	public void Logout(HttpServletRequest request,HttpServletResponse response){
		userService.Logout(request, response);
	}
	
}
