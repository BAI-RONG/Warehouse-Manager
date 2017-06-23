package tool.warehouse.sso.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class pageController {
	@RequestMapping("/page/login")
	public String showLogin(){
		return "Login";
	}
	@RequestMapping("/page/register")
	public String showRegister(){
		return "Register";
	}
}
